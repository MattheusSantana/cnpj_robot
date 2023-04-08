from fastapi import FastAPI, Response
from playwright.async_api import async_playwright
from search_cnpj_robot import search_cnpj

app = FastAPI()

@app.get("/")
def home():
    return "Hello World!"

@app.get("/cnpj/{cnpj}")
async def get_cnpj(cnpj):

    if(len(cnpj) != 14 or not cnpj.isdigit()):
        return 'cnpj inválido'
    
    request = await search_cnpj(cnpj)
    if (request):
        with open('page.html') as fh:
            data = fh.read()
            return Response(content=data, media_type="text/html")
    
