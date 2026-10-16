import os, json, hashlib, psycopg
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from pydantic import BaseModel

app = FastAPI(title="QueueGuard API", version="1.0.0")
security = HTTPBearer()

def get_current_owner(credentials = Depends(security)):
    token_map = {"fixture-a": "owner-a", "fixture-b": "owner-b"}
    user = token_map.get(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais de API inválidas.")
    return user

class EnqueuePayload(BaseModel):
    queue_name: str
    idempotency_key: str
    payload: str

@app.post("/api/messages")
def enqueue_message(body: EnqueuePayload, user: str = Depends(get_current_owner)):
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise HTTPException(status_code=500, detail="DATABASE_URL ausente.")
    
    payload_hash = hashlib.sha256(body.payload.encode("utf-8")).hexdigest()
    lease_expiry = datetime.utcnow() + timedelta(seconds=60)

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            # Verifica chave de idempotência existente para o mesmo owner
            cur.execute(
                "SELECT status, result_json FROM idempotent_keys WHERE key = %s AND owner = %s",
                (body.idempotency_key, user)
            )
            existing = cur.fetchone()

            if existing:
                status, cached_json = existing
                cached_data = json.loads(cached_json) if cached_json else {}
                cached_data["is_duplicate"] = True
                return cached_data

            # Registro da chave e da mensagem em transação atômica
            res_obj = {
                "queue_name": body.queue_name,
                "idempotency_key": body.idempotency_key,
                "status": "COMPLETED",
                "is_duplicate": False
            }

            cur.execute(
                """INSERT INTO idempotent_keys (key, owner, payload_hash, status, lease_until, result_json)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (body.idempotency_key, user, payload_hash, "COMPLETED", lease_expiry, json.dumps(res_obj))
            )

            cur.execute(
                """INSERT INTO queue_messages (queue_name, idempotency_key, owner, payload, status)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                (body.queue_name, body.idempotency_key, user, body.payload, "PROCESSED")
            )
            msg_id = cur.fetchone()[0]

            cur.execute(
                """INSERT INTO audit_events (idempotency_key, action, owner, detail)
                   VALUES (%s, %s, %s, %s)""",
                (body.idempotency_key, "ENQUEUED_ATOMIC", user, f"Queue: {body.queue_name}")
            )

            conn.commit()
            res_obj["id"] = msg_id
            return res_obj

@app.get("/api/messages")
def list_messages(user: str = Depends(get_current_owner)):
    db_url = os.environ.get("DATABASE_URL")
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, queue_name, idempotency_key, payload, status, created_at
                   FROM queue_messages WHERE owner = %s ORDER BY id DESC""",
                (user,)
            )
            rows = cur.fetchall()
            return [
                {
                    "id": r[0],
                    "queue_name": r[1],
                    "idempotency_key": r[2],
                    "payload": r[3],
                    "status": r[4],
                    "created_at": r[5].isoformat() if r[5] else None
                }
                for r in rows
            ]
