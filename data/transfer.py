import os
from dotenv import load_dotenv
import json
import mysql.connector

with open('taipei-attractions.json') as jsonfile:
    data = json.load(jsonfile)

load_dotenv()
config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'database': os.environ['DB_DATABASE']
}


def remain_png_img(urls):
    # split url
    urls_list = urls.split('http')
    urls_list.pop(0)
    result_list = [url.lstrip("s://") for url in urls_list]
    # remain png, jpg
    remain_list = ["https://"+url for url in result_list if ".png" in url.lower() or ".jpg" in url.lower()]
    remain_str = ",".join(remain_list)
    return remain_str

for results_item in data["result"]["results"]:
    name = results_item["stitle"]
    category = results_item["CAT2"]
    description = results_item["xbody"]
    address = results_item["address"]
    transport = results_item["info"]
    mrt = results_item["MRT"]
    latitude = results_item["latitude"]
    longitude = results_item["longitude"]
    images = remain_png_img(results_item["file"])

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    add_attraction = ("INSERT INTO attractions "
                "(name, category, description, address, transport, mrt, latitude, longitude, images) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data_attraction = (name, category, description, address, transport, mrt, latitude, longitude, images)

    cursor.execute(add_attraction, data_attraction)
    cnx.commit()
    cursor.close()
    cnx.close()

