#!/bin/sh

ALL_HEROKU_APPS=$(heroku apps) && export ALL_HEROKU_APPS

case $ALL_HEROKU_APPS in (*"$TERRAFORM_PG_BACKEND"*)
    echo "EXISTING BACKEND FOUND"
    ;;
(*)
   heroku create $TERRAFORM_PG_BACKEND
   heroku addons:create heroku-postgresql:hobby-dev --app $TERRAFORM_PG_BACKEND
   ;;
esac

cd terraform || exit

rm -rf ./nistagram/Dockerfile

echo "FROM radojcin/agent:$VTAG" >> ./nistagram/Dockerfile
echo "CMD python consume.py & python main.py" >> ./nistagram/Dockerfile
cat ./nistagram/Dockerfile

DATABASE_URL=$(heroku config:get DATABASE_URL --app "$TERRAFORM_PG_BACKEND") && export DATABASE_URL
terraform init -backend-config="conn_str=$DATABASE_URL"
terraform apply -auto-approve --var heroku_email="${HEROKU_EMAIL}" \
                                --var vtag="${VTAG}" \
                                --var heroku_api_key="${HEROKU_API_KEY}" \
                                --var terraform_pg_backend="${TERRAFORM_PG_BACKEND}" \
                                --var sql_password="${SQL_PASSWORD}" \
                                --var flask_secret_key="${FLASK_SECRET_KEY}" \
                                --var sql_db_name="${SQL_DB_NAME}" \
                                --var sql_username="${SQL_USERNAME}" \
                                --var stage="${STAGE}" \
                                --var dockerhub_username="${DOCKERHUB_USERNAME}" \
                                --var container_name="${CONTAINER_NAME}" \
                                --var jwt_algorithm="${JWT_ALGORITHM}" \
                                --var jwt_secret="${JWT_SECRET}" \
                                --var wtf_csrf_secret_key="${WTF_CSRF_SECRET_KEY}" \
                                --var enable_csrf="${ENABLE_CSRF}" \
                                --var flask_env="${FLASK_ENV}" \
                                --var flask_run_host="${FLASK_RUN_HOST}" \
                                --var db_type="${DB_TYPE}" \
                                --var db_driver="${DB_DRIVER}" \
                                --var db_user="${DB_USER}" \
                                --var db_password="${DB_PASSWORD}" \
                                --var db_host="${DB_HOST}" \
                                --var db_name="${DB_NAME}" \
                                --var test_database_uri="${TEST_DATABASE_URI}" \
                                --var dev_database_uri="${DEV_DATABASE_URI}" \
                                --var sqlalchemy_database_uri="${SQLALCHEMY_DATABASE_URI}" \
                                --var rabbitmq_uri="${RABBITMQ_URI}" \
                                --var sql_host="${SQL_HOST}" \
                                --var sql_port="${SQL_PORT}" \
                                --var database="${DATABASE}" \
                                --var postgres_password="${POSTGRES_PASSWORD}" \
                                --var postgres_user="${POSTGRES_USER}" \
                                --var postgres_db="${POSTGRES_DB}" \
                                --var key="${KEY}" 
                              

