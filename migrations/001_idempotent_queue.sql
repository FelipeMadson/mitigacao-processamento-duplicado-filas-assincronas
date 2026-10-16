CREATE TABLE IF NOT EXISTS idempotent_keys (
  key text PRIMARY KEY,
  owner text NOT NULL,
  payload_hash text NOT NULL,
  status text NOT NULL,
  lease_until timestamp NOT NULL,
  result_json text,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS queue_messages (
  id bigserial PRIMARY KEY,
  queue_name text NOT NULL,
  idempotency_key text NOT NULL REFERENCES idempotent_keys(key) ON DELETE CASCADE,
  owner text NOT NULL,
  payload text NOT NULL,
  status text NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_events (
  id bigserial PRIMARY KEY,
  idempotency_key text NOT NULL,
  action text NOT NULL,
  owner text NOT NULL,
  detail text,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_keys_owner ON idempotent_keys(owner);
CREATE INDEX IF NOT EXISTS idx_messages_queue ON queue_messages(queue_name);
