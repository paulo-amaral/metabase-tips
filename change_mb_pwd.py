#!/usr/bin/env python3
# You can run this as a standalone script, without Django. Requires the bcrypt and psycopg2 packages.

#sintax is /usr/bin/python3 /opt/projects/metabase/set_password.py postgres:///metabase_db [user@domain] [password]

from sys import argv, stderr
from uuid import uuid4

try:
    from bcrypt import gensalt, hashpw
    from psycopg2 import connect
except ImportError:
    if __name__ == '__main__':
        exit('You need to have the bcrypt and psycopg2 packages installed.\nTry running "pip install [--require-virtualenv/--user] bcrypt psycopg2".')
    raise

BCRYPT_ROUNDS = 10


def bcrypt_metabase_password(password):
    the_uuid = str(uuid4())
    return the_uuid, hashpw((the_uuid + password).encode('utf-8'), gensalt(rounds=BCRYPT_ROUNDS, prefix=b'2a')).decode('utf-8')


def set_bcrypt_metabase_password(dbconn, user_email, new_password):
    with dbconn.cursor() as cur:
        cur.execute("""
            UPDATE core_user
            SET
            password_salt = %s,
            password = %s
            WHERE email = %s
            RETURNING 1
            """,
                    [*bcrypt_metabase_password(new_password), user_email]
                    )
        dbconn.commit()
        return bool(cur.fetchone())


def halp():
    exit(f'''
Usage: {argv[0]} dbconn_url useremail newpassword
       OR
       {argv[0]} newpassword

where `dbconn_url` is a PostgreSQL connection URI (in the trivial case,
that could be as simple as "postgresql:///metabase_db").
''')


if __name__ == '__main__':
    try:
        dbconn_url, user_email, new_password = argv[1:]
    except ValueError:
        try:
            new_password, *whevs = argv[1:]
            if whevs:
                halp()
            print("Salt: %s\nPassword: %s" % bcrypt_metabase_password(new_password))
            exit()
        except ValueError:
            halp()
    # Connect to the local PostgreSQL database on localhost with port 5433
    dbconn = connect(dbconn_url, port=5433)
    if set_bcrypt_metabase_password(dbconn, user_email, new_password):
        print(f'Password set for user with email "{user_email}".', file=stderr)
    else:
        exit(f'No user with email "{user_email}".')
