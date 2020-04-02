import requests
import jwt
import json
import dotenv
import os

dotenv.load_dotenv()

# Läs detta:
# https://renzo.lucioni.xyz/verifying-jwts-with-jwks-and-pyjwt/

AUTH0_DOMAIN = 'forsbevakning.eu.auth0.com'
API_AUDIENCE = "korv"
ALGORITHMS = ["RS256"]
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

jwks = requests.get("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json").json()
public_keys = {}
for jwk in jwks['keys']:
    kid = jwk['kid']
    public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

#print(jwks)

def login():
    data = { 
        "grant_type":"client_credentials",
        "client_id":CLIENT_ID,
        "client_secret":CLIENT_SECRET,
        "audience":API_AUDIENCE
    }

    j = requests.post("https://" + AUTH0_DOMAIN + "/oauth/token", headers = {"content-type":"application/x-www-form-urlencoded"}, data=data).json()
    return j["access_token"]

def user_info(token):
    headers = {
        "Authorization" : "Bearer " + token,
        "Content-Type": "application/json"
    }
    r = requests.get("https://" + AUTH0_DOMAIN + "/userinfo", headers = headers) 
    return r.text

def authenticate(token):
    header = jwt.get_unverified_header(token)
    kid = header["kid"]
    key = public_keys[kid]

    payload = jwt.decode(
                    token,
                    key=key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
    return payload

t = login()
print("TOKEN: ", t)
u = authenticate(t)
print(u)