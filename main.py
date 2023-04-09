from fastapi import FastAPI, Response
from search_cnpj_robot import search_cnpj
from fastapi.responses import JSONResponse


app = FastAPI()

@app.get("/")
def home():
    return "Hello World!"

@app.get("/cnpj/{cnpj}")
async def get_cnpj(cnpj):

    if(len(cnpj) != 14 or not cnpj.isdigit()):
        return 'cnpj inválido'
    
    filename = await search_cnpj(cnpj)
    if (filename):
        with open(filename) as fh:
            data = fh.read()
            return Response(content=data, media_type="text/html")
    
    else:
        return JSONResponse(content={"204": "NÃO FORAM ENCONTRADAS INFORMAÇÕES PARA O CNPJ INFORMADO"}, status_code=401)