# Code is based on this tutorial:
#    - https://www.stefaanlippens.net/oauth-code-flow-pkce.html
#
import base64
import hashlib
import html
import json
import os
import re
import urllib.parse
import requests

verify=False
provider = "https://localhost/auth/realms/healthid"
client_id = "public-client"
username = "99775533@healthid.life"
password = "99775533"
redirect_uri = "https://localhost"

code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
print(code_verifier, len(code_verifier) )

code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
code_challenge = code_challenge.replace('=', '')
print (code_challenge, len(code_challenge))

state = base64.urlsafe_b64encode(os.urandom(40))
resp = requests.get(
    url=provider + "/protocol/openid-connect/auth",
    params={
        "response_type": "code",
        "client_id": client_id,
        "scope": "openid",
        "redirect_uri": redirect_uri,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    },
    allow_redirects=False,
    verify=verify
)

if resp.status_code >= 400:
    exit (resp.text)

cookie = resp.headers['Set-Cookie']
cookie = '; '.join(c.split(';')[0] for c in cookie.split(', '))
print(cookie)

page = resp.text
form_action = html.unescape(re.search('<form\s+.*?\s+action="(.*?)"', page, re.DOTALL).group(1))
print(form_action)

resp = requests.post(
    url=form_action, 
    data={
        "username": username,
        "password": password,
    }, 
    headers={"Cookie": cookie},
    allow_redirects=False,
    verify=verify
)
print(resp.status_code)

if not 'Location' in resp.headers:
    exit(resp.text)

redirect = resp.headers['Location']
print(redirect)

assert redirect.startswith(redirect_uri)

query = urllib.parse.urlparse(redirect).query
redirect_params = urllib.parse.parse_qs(query)
print(redirect_params)

auth_code = redirect_params['code'][0]
print(auth_code)

resp = requests.post(
    url=provider + "/protocol/openid-connect/token",
    data={
        "grant_type": "authorization_code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code": auth_code,
        "code_verifier": code_verifier,
    },
    allow_redirects=False,
    verify=verify
)
print(resp.status_code)

result = resp.json()
print(result)

def _b64_decode(data):
    data += '=' * (4 - len(data) % 4)
    return base64.b64decode(data).decode('utf-8')

def jwt_payload_decode(jwt):
    _, payload, _ = jwt.split('.')
    return json.dumps(json.loads(_b64_decode(payload)), indent=2)

print(jwt_payload_decode(result['access_token']))

print(jwt_payload_decode(result['id_token']))