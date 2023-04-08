import time
import os 
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from anticaptchaofficial.hcaptchaproxyless import *
import aiofiles as aiof

async def search_cnpj(cnpj):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp')
        site_key = await page.locator('//*[@id="frmConsulta"]/div[1]/div[2]/div').get_attribute('data-sitekey')
        await page.locator('//*[@id="cnpj"]').fill(cnpj)
        
        result = await solve_captcha(site_key) 
        print('result', result)
        await page.evaluate(f"""
            let captcha = document.getElementsByName('h-captcha-response')[0];
            console.log('{result}')
            captcha.innerHTML = '{result}' 
            captcha.style.display = 'block';
            document.getElementById('frmConsulta').submit();
            """)

        content = await page.locator('//*[@id="principal"]').inner_html()    
        print('content',content)
        await good(content)


        time.sleep(5)
        
        await browser.close()
        return True

async def good(content):
    async with aiof.open('page.html', "w") as out:
        await out.write(content)
        await out.flush()
        print("done")        
        return content


def handle_response(response):
    print("response body", response.body)
    return response.body

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

