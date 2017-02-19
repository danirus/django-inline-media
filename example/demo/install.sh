#!/bin/bash

pushd `dirname $0` > /dev/null
PRJPATH=`pwd`
popd > /dev/null
FIXTURESPATH=${PRJPATH}/fixtures

check_ret() {
    [[ $? -ne 0 ]] && echo "Failed." && exit 1
}

cd ${PRJPATH}

#------------------------------
printf "Checking Django version... "
# Retrieve 1.7 as 1.07, so that they can be compared as decimal numbers.
version=`python -c 'import django; print("%d.%02d" % django.VERSION[:2])'`
printf "${version}\n"

if [[ ${version} < "1.07" ]]; then
    python manage.py syncdb --noinput || check_ret
    python manage.py migrate inline_media || check_ret
else
    python manage.py migrate || check_ret
    python manage.py migrate inline_media || check_ret
fi

#------------------------------
printf "Loading fixture files... "
fixtures=(auth taggit inline_media articles)
for file in ${fixtures[@]}; do
    python manage.py loaddata ${FIXTURESPATH}/${file}.json || check_ret
done

printf "Add pictures... "
python add_pictures.py
printf "Done\n"
