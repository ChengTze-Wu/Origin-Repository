from flask import Blueprint, request, Response
from model.attraction_query import get_attractions, get_attraction_by_id
import json

attraction = Blueprint('attraction', __name__)

@attraction.route("/attractions")
def attractions():
    response = Response()
    response.headers.add("Content-Type", "application/json; charset=utf-8")
    response.headers.add('Access-Control-Allow-Origin', '*')
    page = request.args.get("page", 0)
    keyword = request.args.get("keyword", '%')
    try:
        data, next_page = get_attractions(keyword, page)
        if data:
            result = json.dumps({"nextPage": next_page, "data":data}, ensure_ascii=False)
            status = 200
        else:
            result = json.dumps({"error":True, "message":"無資料"}, ensure_ascii=False)
            status = 500
    except Exception as e:
        result = json.dumps({"error":True, "message":str(e)}, ensure_ascii=False)
        status = 500
    response.set_data(result)
    response.status_code = status
    return response

@attraction.route("/attraction/<id>")
def attraction_by_id(id):
    response = Response()
    response.headers.add("Content-Type", "application/json; charset=utf-8")
    response.headers.add('Access-Control-Allow-Origin', '*')
    try:
        data = get_attraction_by_id(id)
        if data:
            result = json.dumps({"data":data})
            status = 200
        else:
            result = json.dumps({"error":True,"message":"景點標號不正確"}, ensure_ascii=False)
            status = 400
    except Exception as e:
        result = json.dumps({"error":True,"message":str(e)}, ensure_ascii=False)
        status = 500
    response.set_data(result)
    response.status_code = status
    return response
