import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_DATABASE']
}

cnx = mysql.connector.connect(pool_name = "pool",
                              pool_size = 5,
                              **config)

# TODO try
def attraction_query(keyword, page):
    try:
        cnx = mysql.connector.connect(pool_name = "pool")
        cursor = cnx.cursor()
        if keyword == None:
            keyword = '%'
        attraction_query = ("select * from attractions "
                            "where name like concat('%', %s, '%') "
                            "limit %s, 12")
        page_data = (keyword, page)
        cursor.execute(attraction_query, page_data)
        return cursor.fetchall()
    except:
        cnx.rollback()
    finally:
        cursor.close()
        cnx.close()

def attraction_query_by_id(id):
    try:
        cnx = mysql.connector.connect(pool_name = "pool")
        cursor = cnx.cursor()
        attraction_query = ("select * from attractions "
                            "where id = %s")
        id_data = (id,)
        cursor.execute(attraction_query, id_data)
        return cursor.fetchone()
    except:
        cnx.rollback()
    finally:
        cursor.close()
        cnx.close()
