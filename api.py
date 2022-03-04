from flask import Blueprint, request, jsonify
from mysql_connector import attraction_query, attraction_query_by_id
import json

api = Blueprint('api', __name__)

@api.route("/attractions/")
def get_attractions_json():
    page = request.args.get("page", 0)
    keyword = request.args.get("keyword", '%')

    try:
        attractions = attraction_query(keyword, int(page)*12)
        if attractions:
            data = []
            for attr in attractions:
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
                
            if attraction_query(keyword, (int(page)+1)*12):
                next_page = int(page)+1
            else:
                next_page = None
                
            return jsonify({"nextPage": next_page, "data":data})
        else:
            return jsonify({"error":True, "message":"無資料"}), 500
    except:
        return jsonify({"error":True, "message":"錯誤"}), 500

@api.route("/attraction/<id>")
def get_attraction_json_by_id(id):
    try:
        attr = attraction_query_by_id(id)
        if attr:
            data = [{"id": attr[0],
                        "name": attr[1],
                        "category": attr[2],
                        "description": attr[3],
                        "address": attr[4],
                        "transport": attr[5],
                        "mrt": attr[6],
                        "latitude": attr[7],
                        "longitude": attr[8],
                        "images": attr[9].split(",")}]
            return jsonify({"data":data})
        else:
            return jsonify({"error":True,"message":"景點標號不正確"}), 400
    except:
        return jsonify({"error":True,"message":"錯誤"}), 500