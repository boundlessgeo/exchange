#!/bin/bash

set -e

find /code -type f -name '*pyc' -exec rm {} +
manage='python /code/manage.py'
setup='python /code/setup.py'
maploom_static='/code/exchange/maploom/static/maploom'
maploom_templates='/code/exchange/maploom/templates'
# let the db intialize
if [[ $MAPLOOM_DEV == True ]]; then
  rm -r $maploom_static
  ln -s /code/vendor/maploom/build $maploom_static
  if [[ -f $maploom_templates/maps/maploom.html ]]; then
    rm $maploom_templates/maps/maploom.html
  fi
  ln -s /code/vendor/maploom/build/maploom.html $maploom_templates/maps/maploom.html
fi
sleep 15
$setup build_sphinx
# app integration
plugins=()
# worm integration
if [[ -f /code/vendor/services/setup.py ]]; then
  pip install /code/vendor/services
  plugins=("${plugins[@]}" "worm")
fi
if [ "$plugins" ]; then
  export ADDITIONAL_APPS=$(IFS=,; echo "${plugins[*]}")
fi

$manage migrate --noinput
$manage collectstatic --noinput
$manage loaddata default_users
$manage loaddata base_resources
$manage loaddata /code/docker/exchange/docker_oauth_apps.json
$manage loaddata /code/docker/exchange/anywhere.json
$manage rebuild_index
#if [[ $DEV == True ]]; then
#  $manage importservice http://data-test.boundlessgeo.io/geoserver/wms bcs-hosted-data WMS I
#fi
$manage makemigrations --dry-run --verbosity 3
pip freeze
echo "Dev is set to $DEV"
supervisord -c /code/docker/exchange/supervisor.conf
