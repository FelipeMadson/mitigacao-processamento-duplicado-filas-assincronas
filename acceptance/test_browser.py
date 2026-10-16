import os, pathlib, uuid, psycopg
from playwright.sync_api import sync_playwright, expect

def browser_phase(write_mode):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(os.environ["GI_BROWSER_URL"])

        # Validação do cabeçalho acessível
        expect(page.get_by_role("heading", name="QueueGuard · Plataforma de Desduplicação Idempotente")).to_be_visible()

        if write_mode:
            key = "key-" + uuid.uuid4().hex
            page.get_by_label("Chave de Idempotência").fill(key)
            page.get_by_label("Fila de Destino").fill("payments-stream")
            page.get_by_label("Conteúdo da Mensagem").fill("invoice-9988-amount-500")

            # 1. Primeiro Envio
            page.get_by_role("button", name="Enfileirar Mensagem", exact=True).click()
            expect(page.get_by_role("status")).to_have_text("Mensagem processada (Nova)")

            # 2. Segundo Envio (Duplicado)
            page.get_by_role("button", name="Enfileirar Mensagem", exact=True).click()
            expect(page.get_by_role("status")).to_have_text("Mensagem duplicada prevenida (Idempotente)")

            # Validação no PostgreSQL: exatamente 1 mensagem inserida
            with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
                count = conn.execute("SELECT count(*) FROM queue_messages WHERE idempotency_key = %s", (key,)).fetchone()[0]
                assert count == 1
        else:
            page.get_by_role("button", name="Carregar Mensagens", exact=True).click()

        # Validação da contagem de linhas na tabela
        expect(page.locator("li")).to_have_count(1)

        # Validação de Responsividade e Captura de Telas (390px, 768px, 1440px)
        for width in [390, 768, 1440]:
            page.set_viewport_size({"width": width, "height": 900})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            folder = pathlib.Path("/tmp/screenshots")
            folder.mkdir(exist_ok=True)
            page.screenshot(path=str(folder / (os.environ["GI_TEST_PHASE"] + "-" + str(width) + ".png")))

        browser.close()

def test_before_restart_browser_api_database():
    browser_phase(True)

def test_after_restart_browser_persistence():
    browser_phase(False)
