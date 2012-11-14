#!/bin/bash

python manage.py syncdb --noinput
python cache_pics.py
