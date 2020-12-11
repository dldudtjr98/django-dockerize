#!/bin/bash

list=(/backend/*/)
new_list=() # Not strictly necessary, but added for clarity
var1=/backend/backend/
var2=/backend/static/
for item in ${list[@]}
do
    if [[ "$item" != "$var1" && "$item" != "$var2" ]]
    then
        new_list+=(`basename $item`)
    fi
done
list=("${new_list[@]}")
unset new_list

echo "${list[@]}"

for app in ${list[@]}
do
    python manage.py makemigrations $app
done

python manage.py migrate
gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3