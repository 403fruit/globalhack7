#!/bin/bash

# Extract strings from the source code
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
# Extract strings from the database
./manage.py strings --potfile messages.pot --update

if [ $# -eq 0 ]
    then
        # Use the .pot file to update the existing locales
        pybabel update -i messages.pot -d translations
        echo "Updated languages with new strings"
    else
        # Add a new locale, then update all locales w/ the .pot file
        pybabel init -i messages.pot -d translations -l $1
        pybabel update -i messages.pot -d translations
fi
