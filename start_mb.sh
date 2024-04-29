#sript to start metabase via jar file and connect with local db 
#!/bin/sh
export MB_DB_TYPE=postgres
export MB_DB_DBNAME=metabase_db
export MB_DB_PORT=5432
export MB_DB_USER=user
export MB_DB_PASS=password
export MB_DB_HOST=localhost
java -jar metabase_new.jar
