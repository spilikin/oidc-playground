from keycloak import KeycloakAdmin
from os import environ

keycloak = KeycloakAdmin(server_url=f"{environ.get('KEYCLOAK_BASE_URL')}/auth/",
                               username=environ.get('KEYCLOAK_USER'),
                               password=environ.get('KEYCLOAK_PASSWORD'),
                               verify=True)

REALM_NAME='healthid'

for realm in keycloak.get_realms():
    if realm['realm'] == REALM_NAME:
        keycloak.delete_realm(REALM_NAME)

# https://www.keycloak.org/docs-api/11.0/rest-api/index.html#_realmrepresentation
keycloak.create_realm({
    'realm': REALM_NAME,
    'enabled': True,
}, skip_exists=True)

keycloak.realm_name = REALM_NAME

#  https://www.keycloak.org/docs-api/11.0/rest-api/index.html#_clientrepresentation
keycloak.create_client({
    'id': "public-client",
    'publicClient': True,
    'redirectUris': ["https://localhost/*"],
    'protocolMappers': [
        {
          "name": "Username to Subject Mapper",
          "protocol": "openid-connect",
          "protocolMapper": "oidc-usermodel-attribute-mapper",
          "consentRequired": False,
          "config": {
            "user.attribute": "username",
            "id.token.claim": True,
            "access.token.claim": True,
            "claim.name": "sub",
            "userinfo.token.claim": True
          }
        }
    ],
})

# https://www.keycloak.org/docs-api/11.0/rest-api/index.html#_userrepresentation
keycloak.create_user({
    "id": "99775533@healthid.life",
    "email": "99775533@healthid.life",
    "username": "99775533@healthid.life",
    "enabled": True,
    "firstName": "Firstname",
    "lastName": "Lastname",
    "credentials": [{"value": "99775533","type": "password",}]
})

