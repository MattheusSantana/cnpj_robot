from fastapi import FastAPI
from playwright.async_api import async_playwright
from solve_captcha import solve_captcha

app = FastAPI()

@app.get("/")
def home():
    return "Hello World!"

@app.get("/cnpj/{cnpj}")
async def get_cnpj(cnpj):

    if(len(cnpj) != 14 or not cnpj.isdigit()):
        return 'cnpj inválido'
    
    await solve_captcha(cnpj)

    return cnpj
