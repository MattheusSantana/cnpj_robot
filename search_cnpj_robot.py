from playwright.async_api import async_playwright
import time

async def search_cnpj(cnpj):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp")
        time.sleep(5)
        
        await browser.close()


def solve_captcha():
    solver = hCaptchaProxyon()
