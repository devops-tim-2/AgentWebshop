#!/bin/bash

# 1 - ${{ steps.tag_version.outputs.new_tag }}
# 2 - nistagramtim2@gmail.com 
# 3 - ${{ secrets.HEROKU_API_KEY_STAGE }} 
# 4 - stage-agent-backend-postgres 
# 5 - ${{ secrets.SQL_PASSWORD_STAGE }} 
# 6 - ${{ secrets.KEY }} = 2p7G1QIMWqD9HG8cJHLxadxt8pzTVFs9
# 7 - dfthxqat 
# 8 - dfthxqat 
# 9 - stage
# 10 - radojcin
# 11 - agent
# 12 - JWT_ALGORITHM=HS256
# 13 - JWT_SECRET=ZHuZfCCUw58Nmkk5yBypmq55zvgjf9hk
# 14 - WTF_CSRF_SECRET_KEY=SSOFRgQIofphwhlPGxJCCfMYaRKMlyqG
# 15 - ENABLE_CSRF=0

#!/bin/bash
echo "START"

VTAG=${1}
HEROKU_EMAIL=${2}
HEROKU_API_KEY=${3}
TERRAFORM_PG_BACKEND=${4}
SQL_PASSWORD=${5}
FLASK_SECRET_KEY=${6}
SQL_DB_NAME=${7}
SQL_USERNAME=${8}
STAGE=${9}
DOCKERHUB_USERNAME=${10}
CONTAINER_NAME=${11}
JWT_ALGORITHM=${12}
JWT_SECRET=${13}
WTF_CSRF_SECRET_KEY=${14}
ENABLE_CSRF=${15}
FLASK_ENV=${16:-development}

echo $CONTAINER_NAME

FLASK_RUN_HOST=0.0.0.0
DB_TYPE=postgresql
DB_DRIVER=psycopg2
DB_USER=test
DB_PASSWORD=test
DB_HOST=post_db
DB_NAME=main
TEST_DATABASE_URI=postgres://ybepsuwt:MGotIkC9LeFqFqxY8jUjKDqQwvCunIe3@tai.db.elephantsql.com/ybepsuwt
DEV_DATABASE_URI=postgres://ybepsuwt:MGotIkC9LeFqFqxY8jUjKDqQwvCunIe3@tai.db.elephantsql.com/ybepsuwt
SQLALCHEMY_DATABASE_URI=postgres://ybepsuwt:MGotIkC9LeFqFqxY8jUjKDqQwvCunIe3@tai.db.elephantsql.com/ybepsuwt
RABBITMQ_URI=amqps://qilglokd:nlmVctERVcA7th3VCE1-UL_uij-BCXyj@roedeer.rmq.cloudamqp.com/qilglokd
SQL_HOST=ella.db.elephantsql.com
SQL_PORT=5432
DATABASE=postgres
POSTGRES_PASSWORD=${SQL_PASSWORD}
POSTGRES_USER=${SQL_USERNAME}
POSTGRES_DB=${SQL_DB_NAME}
KEY=${FLASK_SECRET_KEY}

BACKEND_IMAGE=${DOCKERHUB_USERNAME}/agent

docker create \
  --workdir /deployment \
  --entrypoint sh \
  --env HEROKU_EMAIL="${HEROKU_EMAIL}" \
  --env VTAG="${VTAG}" \
  --env HEROKU_API_KEY="${HEROKU_API_KEY}" \
  --env TERRAFORM_PG_BACKEND="${TERRAFORM_PG_BACKEND}" \
  --env SQL_PASSWORD="${SQL_PASSWORD}" \
  --env FLASK_SECRET_KEY="${FLASK_SECRET_KEY}" \
  --env SQL_DB_NAME="${SQL_DB_NAME}" \
  --env SQL_USERNAME="${SQL_USERNAME}" \
  --env STAGE="${STAGE}" \
  --env DOCKERHUB_USERNAME="${DOCKERHUB_USERNAME}" \
  --env CONTAINER_NAME="${CONTAINER_NAME}" \
  --env JWT_ALGORITHM="${JWT_ALGORITHM}" \
  --env JWT_SECRET="${JWT_SECRET}" \
  --env WTF_CSRF_SECRET_KEY="${WTF_CSRF_SECRET_KEY}" \
  --env ENABLE_CSRF="${ENABLE_CSRF}" \
  --env FLASK_ENV="${FLASK_ENV}" \
  --env FLASK_RUN_HOST="${FLASK_RUN_HOST}" \
  --env DB_TYPE="${DB_TYPE}" \
  --env DB_DRIVER="${DB_DRIVER}" \
  --env DB_USER="${DB_USER}" \
  --env DB_PASSWORD="${DB_PASSWORD}" \
  --env DB_HOST="${DB_HOST}" \
  --env DB_NAME="${DB_NAME}" \
  --env TEST_DATABASE_URI="${TEST_DATABASE_URI}" \
  --env DEV_DATABASE_URI="${DEV_DATABASE_URI}" \
  --env SQLALCHEMY_DATABASE_URI="${SQLALCHEMY_DATABASE_URI}" \
  --env RABBITMQ_URI="${RABBITMQ_URI}" \
  --env SQL_HOST="${SQL_HOST}" \
  --env SQL_PORT="${SQL_PORT}" \
  --env DATABASE="${DATABASE}" \
  --env POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
  --env POSTGRES_USER="${POSTGRES_USER}" \
  --env POSTGRES_DB="${POSTGRES_DB}" \
  --env KEY="${KEY}" \
  --env FLASK_SECRET_KEY="${FLASK_SECRET_KEY}" \
  --env JWT_ALGORITHM="${JWT_ALGORITHM}" \
  --env JWT_SECRET="${JWT_SECRET}" \
  --name "${CONTAINER_NAME}" \
  danijelradakovic/heroku-terraform \
  deploy.sh

docker cp deployment/. ${CONTAINER_NAME}:/deployment/
docker start -i ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}
