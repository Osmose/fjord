#!/bin/bash
# pwd is the git repo.
set -e

python manage.py check
echo 'Booyahkasha!'
