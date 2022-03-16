from flask import *
from controller import api, pages
app=Flask(__name__)

app.config["JSON_AS_ASCII"]=False
app.config["JSON_SORT_KEYS"] = False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
app.register_blueprint(pages.app)
# api
app.register_blueprint(api.attraction, url_prefix="/api/")

if __name__ == '__main__':
    app.run(debug=True, port=3000)