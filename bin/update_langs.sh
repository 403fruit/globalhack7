#!/bin/bash

pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
if [ $# -eq 0 ]
    then
        pybabel update -i messages.pot -d translations
        echo "Updated languages with new strings"
    else
        pybabel init -i messages.pot -d translations -l $1
        pybabel update -i messages.pot -d translations
fi
