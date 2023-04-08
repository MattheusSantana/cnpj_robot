from fastapi import FastAPI
from playwright.async_api import async_playwright
from busca_cnpj import busca_cnpj

app = FastAPI()

@app.get("/")
def home():
    return "Hello World!"

@app.get("/cnpj/{cnpj}")
async def get_cnpj(cnpj):

    if(len(cnpj) != 14 or not cnpj.isdigit()):
        return 'cnpj inválido'
    
    await busca_cnpj(cnpj)

    return cnpj
