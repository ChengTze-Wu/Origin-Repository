from flask import Blueprint, request, Response
from mysql_connector import attraction_query, attraction_query_by_id
import json

api = Blueprint('api', __name__)

@api.route("/attractions")
def get_attractions_json():
    resp = Response()
    resp.headers.add("Content-Type", "application/json; charset=utf-8")
    resp.headers.add('Access-Control-Allow-Origin', '*')
    page = request.args.get("page", 0)
    keyword = request.args.get("keyword", '%')
    try:
        attractions = attraction_query(keyword, int(page)*12)
        if attractions:
            data = []
            for attr in attractions[:12]:
                data.append({"id": attr[0],
                            "name": attr[1],
                            "category": attr[2],
                            "description": attr[3],
                            "address": attr[4],
                            "transport": attr[5],
                            "mrt": attr[6],
                            "latitude": attr[7],
                            "longitude": attr[8],
                            "images": attr[9].split(",")})
            if len(attractions) > 12:
                next_page = int(page)+1
            else:
                next_page = None
            
            result = json.dumps({"nextPage": next_page, "data":data}, ensure_ascii=False)
            status = 200
        else:
            result = json.dumps({"error":True, "message":"無資料"}, ensure_ascii=False)
            status = 500
        resp.set_data(result)
        resp.status_code = status;
        return resp
    except:
        result = json.dumps({"error":True, "message":"錯誤"}, ensure_ascii=False)
        resp.set_data(result)
        resp.status_code = 500;
        return resp

@api.route("/attraction/<id>")
def get_attraction_json_by_id(id):
    resp = Response()
    resp.headers.add("Content-Type", "application/json; charset=utf-8")
    resp.headers.add('Access-Control-Allow-Origin', '*')
    try:
        attr = attraction_query_by_id(id)
        if attr:
            data = {"id": attr[0],
                        "name": attr[1],
                        "category": attr[2],
                        "description": attr[3],
                        "address": attr[4],
                        "transport": attr[5],
                        "mrt": attr[6],
                        "latitude": attr[7],
                        "longitude": attr[8],
                        "images": attr[9].split(",")}
            result = json.dumps({"data":data})
            status = 200
        else:
            result = json.dumps({"error":True,"message":"景點標號不正確"}, ensure_ascii=False)
            status = 400
        resp.set_data(result)
        resp.status_code = status;
        return resp
    except:
        result = json.dumps({"error":True,"message":"錯誤"}, ensure_ascii=False)
        resp.set_data(result)
        resp.status_code = 500;
        return resp