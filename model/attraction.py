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

cnx = mysql.connector.connect(pool_name="attraction",
                              pool_size=5,
                              **config)


def get_attractions(keyword, page):
    try:
        cnx = mysql.connector.connect(pool_name="attraction")
        cursor = cnx.cursor()
        attraction_query = ("select * from attractions "
                            "where name like concat('%', %s, '%') "
                            "limit %s, 13")
        page_data = (keyword, int(page)*12)
        cursor.execute(attraction_query, page_data)
        attractions = cursor.fetchall()
        if attractions:
            data = []
            for attraction in attractions[:12]:
                data.append({"id": attraction[0],
                            "name": attraction[1],
                             "category": attraction[2],
                             "description": attraction[3],
                             "address": attraction[4],
                             "transport": attraction[5],
                             "mrt": attraction[6],
                             "latitude": attraction[7],
                             "longitude": attraction[8],
                             "images": attraction[9].split(",")})
        else:
            data = None
        if len(attractions) > 12:
            next_page = int(page)+1
        else:
            next_page = None
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
        return (data, next_page)


def get_attraction_by_id(id):
    try:
        cnx = mysql.connector.connect(pool_name="attraction")
        cursor = cnx.cursor()
        attraction_query = ("select * from attractions "
                            "where id = %s")
        id_data = (int(id),)
        cursor.execute(attraction_query, id_data)
        attraction = cursor.fetchone()
        if attraction:
            data = {"id": attraction[0],
                    "name": attraction[1],
                    "category": attraction[2],
                    "description": attraction[3],
                    "address": attraction[4],
                    "transport": attraction[5],
                    "mrt": attraction[6],
                    "latitude": attraction[7],
                    "longitude": attraction[8],
                    "images": attraction[9].split(",")}
        else:
            data = None
        return {"data": data}
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
