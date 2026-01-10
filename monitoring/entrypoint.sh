#!/bin/sh
set -e

echo "Substituting env variables..."
envsubst < /etc/alertmanager/alertmanager.yml.template > /etc/alertmanager/alertmanager.yml

exec /bin/alertmanager --config.file=/etc/alertmanager/alertmanager.yml
