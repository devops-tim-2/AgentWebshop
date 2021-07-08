terraform {
  required_providers {
    heroku = {
      source  = "heroku/heroku"
      version = "~> 4.0"
    }
  }
  backend "pg" {
  }
}

provider "heroku" {}

variable "heroku_email" {
  description = "I dont care!!!!"
}
variable "vtag" {
  description = "I dont care!!!!"
}
variable "heroku_api_key" {
  description = "I dont care!!!!"
}
variable "terraform_pg_backend" {
  description = "I dont care!!!!"
}
variable "sql_password" {
  description = "I dont care!!!!"
}
variable "flask_secret_key" {
  description = "I dont care!!!!"
}
variable "sql_db_name" {
  description = "I dont care!!!!"
}
variable "sql_username" {
  description = "I dont care!!!!"
}
variable "stage" {
  description = "I dont care!!!!"
}
variable "dockerhub_username" {
  description = "I dont care!!!!"
}
variable "container_name" {
  description = "I dont care!!!!"
}
variable "jwt_algorithm" {
  description = "I dont care!!!!"
}
variable "jwt_secret" {
  description = "I dont care!!!!"
}
variable "wtf_csrf_secret_key" {
  description = "I dont care!!!!"
}
variable "enable_csrf" {
  description = "I dont care!!!!"
}
variable "flask_env" {
  description = "I dont care!!!!"
}
variable "flask_run_host" {
  description = "I dont care!!!!"
}
variable "db_type" {
  description = "I dont care!!!!"
}
variable "db_driver" {
  description = "I dont care!!!!"
}
variable "db_user" {
  description = "I dont care!!!!"
}
variable "db_password" {
  description = "I dont care!!!!"
}
variable "db_host" {
  description = "I dont care!!!!"
}
variable "db_name" {
  description = "I dont care!!!!"
}
variable "test_database_uri" {
  description = "I dont care!!!!"
}
variable "dev_database_uri" {
  description = "I dont care!!!!"
}
variable "sqlalchemy_database_uri" {
  description = "I dont care!!!!"
}
variable "rabbitmq_uri" {
  description = "I dont care!!!!"
}
variable "sql_host" {
  description = "I dont care!!!!"
}
variable "sql_port" {
  description = "I dont care!!!!"
}
variable "database" {
  description = "I dont care!!!!"
}
variable "postgres_password" {
  description = "I dont care!!!!"
}
variable "postgres_user" {
  description = "I dont care!!!!"
}
variable "postgres_db" {
  description = "I dont care!!!!"
}
variable "key" {
  description = "I dont care!!!!"
}

## backend
resource "heroku_app" "nistagram" {
  name = "nistagram-tim2"
  stack = "container"
  region = "eu"

  config_vars = {
    HEROKU_EMAIL = var.heroku_email
    VTAAG = var.vtag
    HEROKU_API_KEY = var.heroku_api_key
    TERRAFORM_PG_BACKEND = var.terraform_pg_backend
    SQL_PASSWORD = var.sql_password
    FLASK_SECRET_KEY = var.flask_secret_key
    SQL_DB_NAME = var.sql_db_name
    SQL_USERNAME = var.sql_username
    STAGE = var.stage
    DOCKERHUB_USERNAME = var.dockerhub_username
    CONTAINER_NAME = var.container_name
    JWT_ALGORITHM = var.jwt_algorithm
    JWT_SECRET = var.jwt_secret
    WTF_CSRF_SECRET_KEY = var.wtf_csrf_secret_key
    ENABLE_CSRF = var.enable_csrf
    FLASK_ENV = var.flask_env
    FLASK_RUN_HOST = var.flask_run_host
    DB_TYPE = var.db_type
    DB_DRIVER = var.db_driver
    DB_USER = var.db_user
    DB_PASSWORD = var.db_password
    DB_HOST = var.db_host
    DB_NAME = var.db_name
    TEST_DATABASE_URI = var.test_database_uri
    DEV_DATABASE_URI = var.dev_database_uri
    SQLALCHEMY_DATABASE_URI = var.sqlalchemy_database_uri
    RABBITMQ_URI = var.rabbitmq_uri
    SQL_HOST = var.sql_host
    SQL_PORT = var.sql_port
    DATABASE = var.database
    POSTGRES_PASSWORD = var.postgres_password
    POSTGRES_USER = var.postgres_user
    POSTGRES_DB = var.postgres_db
    KEY = var.key
  }
}

resource "heroku_addon" "postgres" {
  app = heroku_app.nistagram.id
  plan = "heroku-postgresql:hobby-dev"
}

resource "heroku_build" "nistagram-build" {
  app = heroku_app.nistagram.id
  source {
    path = "nistagram"
  }
}