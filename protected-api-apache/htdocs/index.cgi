#!/bin/bash

echo "Content-type: text/html"
echo ""

echo '<html>'
echo '<head>'
echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
echo '<title>Protected API</title>'
echo '</head>'
echo '<body>'
echo '<h1>Protected API</h1>'
echo '<h2>Environment Variables:</h2>'
echo '<pre>'
/usr/bin/env
echo '</pre>'

echo '</body>'
echo '</html>'

exit 0