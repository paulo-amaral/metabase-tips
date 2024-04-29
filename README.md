# Metabase tips
## Running localy instance of metabase and postgres without docker
#### Dump your db to localhost
create a new postgresql server in that app(mac uses postgres.app) - https://postgresapp.com/

create a database in that server : `create database your_db` 

restore this dump into that db `pg_restore -Ox -d your_db ./your_db.custom ` where your db custom is the latest dump to restore

If you want to run the actual metabase database (with all the questions built already). 
Just need to run the metabase executable with environment vars that tell it to use that db

create a database in that server `create database your_metabase_db`

restore this dump into that db `pg_restore -Ox -d your_metabase_db ./your_metabase_db.custom`

I run outside of docker, just using java and use a script like this:
```
#!/bin/sh
export MB_DB_TYPE=postgres
export MB_DB_DBNAME=my_mb_db
export MB_DB_PORT=5432
export MB_DB_USER=username
export MB_DB_PASS=
export MB_DB_HOST=localhost
java -jar ~/Downloads/metabase.jar
telling metabase to use postgres on localhost:5432 and the db my_mb_db
```

