from playwright.async_api import async_playwright
import time

async def solve_captcha(cnpj):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp")
        time.sleep(5)
        
        await browser.close()