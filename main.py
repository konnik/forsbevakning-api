from fastapi import FastAPI, Header
import smhi
import auth

app = FastAPI()

@app.get("/")
async def root():
    return { "message" : "Välkommen till Forsbevaknings API." }


@app.get("/prognos/{subid}")
async def prognos(subid):
    return smhi.fetch_data(subid)



@app.get("/secure")
async def secure( authorization: str = Header(None)):
    token = authorization.split()[1]
    a = auth.authenticate(token)

    return a

