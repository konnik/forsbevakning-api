from fastapi import FastAPI, Header, Response
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
async def prognos(subid, response: Response):
    prognos = smhi.fetch_data(subid)

    if prognos is None:
        response.status_code = 404
        return "Id finns inte."
    
    return prognos 



@app.get("/secure")
async def secure( authorization: str = Header(None)):
    token = authorization.split()[1]
    a = auth.authenticate(token)

    return a


@app.get("/apa")
async def apa():

    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        cur = conn.cursor()
        cur.execute("select * from apa")
        rows = cur.fetchall()

        result = []
        for row in rows:
            result.append(row)
        
        return result
