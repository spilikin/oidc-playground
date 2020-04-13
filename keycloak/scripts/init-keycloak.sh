#!/bin/bash
# Login into admin API
docker-compose exec keycloak sh -c '/opt/jboss/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080/auth --realm master --user ${KEYCLOAK_USER} --password ${KEYCLOAK_PASSWORD}'
# create realm
docker-compose exec keycloak /opt/jboss/keycloak/bin/kcadm.sh create realms -s realm=realm0 -s enabled=true
# create gatekeeper client
#CID=$(docker-compose exec keycloak /opt/jboss/keycloak/bin/kcadm.sh create clients -r realm0 -s clientId=oidc-gatekeeper-client -s 'redirectUris=["http://localhost:7500/*"]' -i|tr -d '\n'|tr -d '\r')
#docker-compose exec keycloak /opt/jboss/keycloak/bin/kcadm.sh update clients/$CID -r realm0 -s clientAuthenticatorType=client-secret -s secret=aa802860-dbef-4be6-a6fe-dbd8a141350e
docker-compose exec keycloak /opt/jboss/keycloak/bin/kcadm.sh create clients -r realm0 -s clientId=oidc-gatekeeper-client -s clientAuthenticatorType=client-secret -s secret=aa802860-dbef-4be6-a6fe-dbd8a141350e -s 'redirectUris=["http://localhost:7500/*"]'
docker-compose exec keycloak /opt/jboss/keycloak/bin/kcadm.sh create clients -r realm0 -s clientId=oidc-native-app-client -s publicClient=true -s 'redirectUris=["http://localhost:7500/*"]'
#docker-compose exec keycloak /opt/jboss/keycloak/bin/kcadm.sh get clients/$CID/installation/providers/keycloak-oidc-keycloak-json > config/public-client.keycloak.json -r realm0
# create gatekeeper-client
# TODO
# create users
docker-compose exec keycloak /opt/jboss/keycloak/bin/kcadm.sh create users -r realm0 -s username=user0 -s enabled=true -s email="user0@example.com" -s emailVerified=true 
docker-compose exec keycloak /opt/jboss/keycloak/bin/kcadm.sh set-password -r realm0 --username user0 --new-password password0 
