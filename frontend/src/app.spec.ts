import { describe, it, expect } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('QueueGuard Angular Component', () => {
  it('renders accessible form controls and labels', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('QueueGuard');
    expect(compiled.querySelector('label[for="keyInput"]')?.textContent).toBe('Chave de Idempotência');
    expect(compiled.querySelector('label[for="queueInput"]')?.textContent).toBe('Fila de Destino');
  });
});
