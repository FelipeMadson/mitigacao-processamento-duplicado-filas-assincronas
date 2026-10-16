import { Component, signal, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'product-app',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <main>
      <header>
        <h1>QueueGuard · Plataforma de Desduplicação Idempotente</h1>
        <p class="subtitle">Garantia determinística de execução única em filas distribuídas</p>
      </header>

      <section class="card">
        <label for="keyInput">Chave de Idempotência</label>
        <input id="keyInput" #keyInput placeholder="Ex: evt_994821a">

        <label for="queueInput">Fila de Destino</label>
        <input id="queueInput" #queueInput placeholder="Ex: payments-stream">

        <label for="payloadInput">Conteúdo da Mensagem</label>
        <input id="payloadInput" #payloadInput placeholder="Ex: {'amount': 150.00}">

        <div class="actions">
          <button (click)="enqueue(keyInput.value, queueInput.value, payloadInput.value)">
            Enfileirar Mensagem
          </button>
          <button (click)="load()" class="secondary">
            Carregar Mensagens
          </button>
        </div>

        <p role="status" class="status-badge" [class.duplicate]="isDuplicate()">
          {{ status() }}
        </p>
      </section>

      <section class="messages-list">
        <h2>Mensagens Processadas</h2>
        <ul>
          @for (msg of messages(); track msg.id) {
            <li>
              <strong>#{{ msg.id }} [{{ msg.queue_name }}]</strong>: {{ msg.payload }}
              <span class="key-tag">chave: {{ msg.idempotency_key }}</span>
            </li>
          }
        </ul>
      </section>
    </main>
  `
})
export class App {
  messages = signal<Array<{ id: number; queue_name: string; idempotency_key: string; payload: string }>>([]);
  status = signal<string>('Pronto para enfileirar');
  isDuplicate = signal<boolean>(false);

  async load() {
    const response = await fetch('/api/messages', {
      headers: { Authorization: 'Bearer fixture-a' }
    });
    if (!response.ok) throw new Error('Falha ao carregar mensagens.');
    const data = await response.json();
    this.messages.set(data);
  }

  async enqueue(key: string, queue: string, payload: string) {
    if (!key || !queue) {
      this.status.set('Chave e fila são obrigatórios.');
      return;
    }

    const response = await fetch('/api/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer fixture-a'
      },
      body: JSON.stringify({
        queue_name: queue,
        idempotency_key: key,
        payload: payload || '{}'
      })
    });

    if (!response.ok) throw new Error('Falha ao enfileirar mensagem.');
    const result = await response.json();

    if (result.is_duplicate) {
      this.isDuplicate.set(true);
      this.status.set('Mensagem duplicada prevenida (Idempotente)');
    } else {
      this.isDuplicate.set(false);
      this.status.set('Mensagem processada (Nova)');
    }

    await this.load();
  }
}
