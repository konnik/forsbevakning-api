from fastapi import FastAPI, Header
import smhi
import auth
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

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


@app.get("/apa"):
async def apa():

    with conn = psycopg2.connect(DATABASE_URL, sslmode='require'):
        cur = conn.cursor()
        cur.execute("select * from apa")
        rows = cur.fetchall()

        result = []
        for row in rows:
            result.append(row)
        
        return result
