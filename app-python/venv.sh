#!/bin/bash
if [ ! -f ./requirements.txt ] 
    then
        echo "ERROR: requirements.txt not found"
        return
fi
if [ ! -f ~/.virtualenv/oidc-app-python/bin/activate ]
    then
        pip install virtualenv 2> /dev/null
        python3 -m virtualenv --python=python3.7 ~/.virtualenv/oidc-app-python
fi
echo Activating virtualenv
source ~/.virtualenv/oidc-app-python/bin/activate
pip install -r ./requirements.txt