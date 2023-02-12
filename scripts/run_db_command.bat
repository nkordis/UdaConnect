@echo off

REM Usage: pass in the DB container ID as the argument

REM Set database configurations
set CT_DB_USERNAME=ct_admin
set CT_DB_NAME=geoconnections

type .\db\2020-08-15_init-db.sql | kubectl exec -i %1 -- bash -c "psql -U %CT_DB_USERNAME% -d %CT_DB_NAME%"

type .\db\udaconnect_public_person.sql | kubectl exec -i %1 -- bash -c "psql -U %CT_DB_USERNAME% -d %CT_DB_NAME%"

type .\db\udaconnect_public_location.sql | kubectl exec -i %1 -- bash -c "psql -U %CT_DB_USERNAME% -d %CT_DB_NAME%"
