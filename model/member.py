import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

load_dotenv()
config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'database': os.environ['DB_DATABASE']
}

cnx = mysql.connector.connect(pool_name="user",
                              pool_size=5,
                              **config)


def get_current_user(email):
    try:
        cnx = mysql.connector.connect(pool_name="user")
        cursor = cnx.cursor()

        query_user = ("select id, name, email from users "
                      "where email = %s")
        data_user = (email,)

        cursor.execute(query_user, data_user)
        data = cursor.fetchone()
        result = {"id": data[0], "name": data[1],
                  "email": data[2]} if data else None
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
        return {"data": result}


def signup_user(name, email, password):
    try:
        cnx = mysql.connector.connect(pool_name="user")
        cursor = cnx.cursor()

        add_user = ("INSERT INTO users "
                    "(name, email, password) "
                    "VALUES (%s, %s, %s)")
        data_user = (name, email, password)

        cursor.execute(add_user, data_user)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            return False
        else:
            raise err
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
        return True


def signin_user(email, password):
    try:
        cnx = mysql.connector.connect(pool_name="user")
        cursor = cnx.cursor()

        query_user = ("select email from users "
                      "where email = %s and password = %s")
        data_user = (email, password)

        cursor.execute(query_user, data_user)
        data = cursor.fetchone()
        result = data[0] if data else None
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
        return result
