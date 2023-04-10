import time
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from anticaptchaofficial.hcaptchaproxyless import *
import aiofiles as aiof
import uuid


load_dotenv()

async def search_cnpj(cnpj):
    async with async_playwright() as p:
        filename = False
        
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(os.getenv('WEBSITE_URL'))
        site_key = await page.locator('//*[@id="frmConsulta"]/div[1]/div[2]/div').get_attribute('data-sitekey')
        await page.locator('//*[@id="cnpj"]').fill(cnpj)
        
        result = await solve_captcha(site_key)
        if (not result):
            await browser.close()
            return False

        await submit_page(page, result)

        content = await page.locator('//*[@id="principal"]').inner_html()
        filename = await make_html_response(content)

        time.sleep(5)

        await browser.close()
        return filename

async def solve_captcha(site_key):
    solver = hCaptchaProxyless()
    solver.set_verbose(1)
    key = os.getenv('APIKEY')
    solver.set_key(key)
    solver.set_website_url(os.getenv('WEBSITE_URL'))
    solver.set_website_key(site_key)
    result = solver.solve_and_return_solution()

    if result != 0:
        return result
    else:
        print(solver.err_string)
        return False


async def submit_page(page, result):
    await page.evaluate(f"""
            let captcha = document.getElementsByName('h-captcha-response')[0];
            console.log("captcha", captcha);
            captcha.innerHTML = '{result}' 
            console.log("inner", captcha);
            captcha.style.display = 'block';
            document.getElementById('frmConsulta').submit();""")

async def make_html_response(content):
    filename = uuid.uuid4().hex
    filename = filename+'.html'
    print(filename)
    async with aiof.open(filename, "w") as out:
        await out.write(content)
        await out.flush()
        return filename