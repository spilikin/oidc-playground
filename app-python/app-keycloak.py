from keycloak import KeycloakOpenID

# Configure client
keycloak_openid = KeycloakOpenID(server_url="http://localhost:7501/auth/",
                    client_id="oidc-native-app-client",
                    realm_name="realm0")

# Get WellKnow
config_well_know = keycloak_openid.well_know()

# Get Token
token = keycloak_openid.token("user0", "password0")
print (token['access_token'])

# Get Userinfo
userinfo = keycloak_openid.userinfo(token['access_token'])

print(userinfo)

# Refresh token
token = keycloak_openid.refresh_token(token['refresh_token'])

# Logout
keycloak_openid.logout(token['refresh_token'])
