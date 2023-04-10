from fastapi import FastAPI, Response , status
from search_cnpj_robot import search_cnpj
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder



app = FastAPI()

@app.get("/")
def home():
    return "Hello World!"

@app.get("/cnpj/{cnpj}")
async def get_cnpj(cnpj):

    if(len(cnpj) != 14 or not cnpj.isdigit()):
        return cnpj_error()
    try:
        filename = await search_cnpj(cnpj)
        if (filename):
            with open(filename) as fh:
                data = fh.read()
                return Response(content=data, media_type="text/html")
    except:
        return cnpj_error()


def cnpj_error():
    return JSONResponse(content=jsonable_encoder({"204": "NÃO FORAM ENCONTRADAS INFORMAÇÕES PARA O CNPJ INFORMADO"}))