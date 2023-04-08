import time
import os 
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from anticaptchaofficial.hcaptchaproxyless import *


async def search_cnpj(cnpj):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp')
        site_key = await page.locator('//*[@id="frmConsulta"]/div[1]/div[2]/div').get_attribute('data-sitekey')
        await page.locator('//*[@id="cnpj"]').fill(cnpj)
        result = await solve_captcha(site_key) 
        # result = 'teste'
        print('result', result)
        await page.evaluate(f"""
            document.getElementsByName('h-captcha-response')[0].innerHTML= '{result}'; 
            document.getElementById('frmConsulta').submit();
            """)

        page.on("request", handle_response)

        time.sleep(50)
        
        await browser.close()

def handle_response(request_event):
    print("request_event", request_event)
    return request_event

async def solve_captcha(site_key):
    load_dotenv()
    solver = hCaptchaProxyless()
    solver.set_verbose(1)
    key = os.getenv('APIKEY')
    solver.set_key(key)
    solver.set_website_url('https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp')
    solver.set_website_key(site_key)
    result =  solver.solve_and_return_solution()

    if result !=0 :
        return result
    else:
        print(solver.err_string)

