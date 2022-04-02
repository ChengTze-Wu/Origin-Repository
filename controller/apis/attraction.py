from flask import Blueprint, request, Response
import model
import json

attraction = Blueprint('attraction', __name__)

@attraction.route("/attractions", methods=["GET"])
def attractions():
    response = Response()
    response.headers.add("Content-Type", "application/json; charset=utf-8")
    response.headers.add('Access-Control-Allow-Origin', '*')
    page = request.args.get("page", 0)
    keyword = request.args.get("keyword", '%')
    try:
        data, next_page = model.get_attractions(keyword, page)
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

@attraction.route("/attraction/<id>", methods=["GET"])
def attraction_by_id(id):
    response = Response()
    response.headers.add("Content-Type", "application/json; charset=utf-8")
    response.headers.add('Access-Control-Allow-Origin', '*')
    try:
        data = model.get_attraction_by_id(id)
        if data:
            result = json.dumps(data)
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
