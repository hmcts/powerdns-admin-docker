#!/bin/sh

set -o errexit
set -o pipefail

# == Vars
#
DB_MIGRATION_DIR='/powerdns-admin/migrations'
if [[ -z ${PDNS_PROTO} ]];
 then PDNS_PROTO="http"
fi

if [[ -z ${PDNS_PORT} ]];
 then PDNS_PORT=8081
fi

echo "===> Waiting for $PDA_DB_HOST"
until nc -zv \
  $PDA_DB_HOST \
  $PDA_DB_PORT;
do
  echo "($PDA_DB_HOST) is unavailable - sleeping"
  sleep 1
done


echo "===> DB management"
# Go in Workdir
cd /powerdns-admin

if [ ! -d "${DB_MIGRATION_DIR}" ]; then
  echo "---> Running DB Init"
  flask db init --directory ${DB_MIGRATION_DIR}
  flask db migrate -m "Init DB" --directory ${DB_MIGRATION_DIR}
  flask db upgrade --directory ${DB_MIGRATION_DIR}
  ./init_data.py

else
  echo "---> Running DB Migration"
  set +e
  flask db migrate -m "Upgrade DB Schema" --directory ${DB_MIGRATION_DIR}
  flask db upgrade --directory ${DB_MIGRATION_DIR}
  set -e
fi

echo "===> Update configuration"
export PGPASSWORD="${PDA_DB_PASSWORD}"

# there's no constraint on name so this is a bit hacky
function add_or_update_setting() {
  name="${1}"
  echo "Updating config for key: ${name}"
  value="${2}"
  set -f # prevents '*'' from being expanded
  insert_sql="INSERT INTO setting (name, value) SELECT * FROM (SELECT '${name}', '${value}') AS tmp WHERE NOT EXISTS (SELECT name FROM setting WHERE name = '${name}') LIMIT 1;"
  update_sql="UPDATE setting SET value='${value}' WHERE name = '${name}';"
  psql -h ${PDA_DB_HOST} -U ${PDA_DB_USER} -p ${PDA_DB_PORT} -d ${PDA_DB_NAME} -c "${insert_sql}"
  psql -h ${PDA_DB_HOST} -U ${PDA_DB_USER} -p ${PDA_DB_PORT} -d ${PDA_DB_NAME} -c "${update_sql}"
  set +f
}

add_or_update_setting 'pdns_api_url' "${PDNS_PROTO}://${PDNS_HOST}:${PDNS_PORT}"
add_or_update_setting 'pdns_api_key' "${PDNS_API_KEY}"
add_or_update_setting 'signup_enabled' "${PDA_SIGNUP_ENABLED:-False}"
add_or_update_setting 'local_db_enabled' "${PDA_LOCAL_DB_ENABLED:-False}"
add_or_update_setting 'site_name' "${PDA_SITE_NAME}"

echo "===> Starting app"
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app
