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

cnx = mysql.connector.connect(pool_name = "booking",
                              pool_size = 5,
                              **config)

def get_booking_by_user_id(user_id):
    try:
        cnx = mysql.connector.connect(pool_name = "booking")
        cursor = cnx.cursor()
        
        query = ("SELECT attractions.id, attractions.name, attractions.address, attractions.images, "
                 "bookings.id, bookings.date, bookings.time, bookings.price "
                 "FROM((bookings INNER JOIN users ON bookings.user_id = users.id) "
                 "INNER JOIN attractions ON bookings.attraction_id = attractions.id) "
                 "WHERE users.id = %s")
        value = (user_id,)
        
        cursor.execute(query, value)
        data = cursor.fetchall()
        if data:
            data = data[-1]
            result = { "data":{
                "attraction": {
                    "id": data[0],
                    "name": data[1],
                    "address": data[2],
                    "image": data[3].split(",")[0]
                },
                "date": str(data[5]),
                "time": data[6],
                "price": data[7]}}
            booking_id = data[4]
        else:
            result = {"data":None}
            booking_id = None
        return (result, booking_id)
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
        
        
def create_booking(date, time, price, attraction_id, user_id):
    try:
        cnx = mysql.connector.connect(pool_name = "booking")
        cursor = cnx.cursor()
        
        query = ("INSERT INTO bookings (date, time, price, attraction_id, user_id) "
                     "values (%s, %s, %s, %s, %s)")
        value = (date, time, price, attraction_id, user_id)
            
        cursor.execute(query, value)
        cnx.commit()
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()
        
def delete_booking(id):
    try:
        cnx = mysql.connector.connect(pool_name = "booking")
        cursor = cnx.cursor()
        
        query = ("DELETE FROM bookings "
                 "WHERE id = %s")
        value = (id,)

        cursor.execute(query, value)
        cnx.commit()
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()