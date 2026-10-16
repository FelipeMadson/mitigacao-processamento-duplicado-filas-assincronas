import os, socket, uuid, psycopg, pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
token_a = {"Authorization": "Bearer fixture-a"}
token_b = {"Authorization": "Bearer fixture-b"}

def test_before_restart_api_and_database():
    # 1. Rejeita anônimo
    assert client.get("/api/messages").status_code == 401
    assert client.post("/api/messages", json={"queue_name": "q", "idempotency_key": "k", "payload": "p"}).status_code == 401

    # 2. Enfileira nova mensagem com sucesso
    key = "key-" + uuid.uuid4().hex
    body_data = {"queue_name": "orders-v1", "idempotency_key": key, "payload": "order-content-1"}
    r1 = client.post("/api/messages", json=body_data, headers=token_a)
    assert r1.status_code == 200
    res1 = r1.json()
    assert res1["is_duplicate"] is False
    assert res1["status"] == "COMPLETED"

    # 3. Re-enfileiramento com a mesma chave: Idempotência garantida (retorno cacheado sem duplicação)
    r2 = client.post("/api/messages", json=body_data, headers=token_a)
    assert r2.status_code == 200
    res2 = r2.json()
    assert res2["is_duplicate"] is True

    # 4. Verifica no PostgreSQL: exatamente 1 linha gravada na tabela de mensagens
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        count = conn.execute("SELECT count(*) FROM queue_messages WHERE idempotency_key = %s", (key,)).fetchone()[0]
        assert count == 1

    # 5. Isolamento Multi-Tenant: Tenant B não enxerga mensagens do Tenant A
    messages_b = client.get("/api/messages", headers=token_b).json()
    assert len(messages_b) == 0

    # 6. Sem rede externa
    with pytest.raises(OSError):
        socket.create_connection(("1.1.1.1", 443), timeout=1)

def test_after_restart_data_survives():
    # Após reinício do banco de dados PostgreSQL, os dados persistem perfeitamente
    messages_a = client.get("/api/messages", headers=token_a).json()
    assert len(messages_a) >= 1
    assert messages_a[0]["queue_name"] == "orders-v1"
