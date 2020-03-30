from fastapi import FastAPI
import smhi
app = FastAPI()

@app.get("/")
async def root():
    return { "message" : "Välkommen till Forsbevaknings API." }


@app.get("/prognos/{subid}")
async def prognos(subid):
    return smhi.fetch_data(subid)


