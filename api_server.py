from flask import Flask, make_response
from flask_restx import Api, Resource
from dateutil.parser import parse as date_parse
import subprocess
import datetime
import os
import json
from pytz import timezone

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
api = Api(app)


@api.route("/bob")
class Bob(Resource):
    def get(self):
        today = datetime.datetime.now(timezone('Asia/Seoul'))
        today -= datetime.timedelta(days=today.weekday())
       
        if not os.path.exists("datas/" + today.strftime("%m-%d") + ".json"):
            subprocess.call(["python", "parser_date.py", today.strftime("%Y%m%d")])
            print('called subprocess')
        with open(
            "datas/" + today.strftime("%m-%d") + ".json", "r", encoding="utf-8"
        ) as f:
            result = json.loads(f.read())
            result = json.dumps(result, ensure_ascii=False, indent=4)
            res = make_response(result)
            return res


@api.route("/bob/<date>")
class Bob_date(Resource):
    def get(self, date):
        today = date_parse(date)
        temp_day = today - datetime.timedelta(days=today.weekday())
        if not os.path.exists("datas/" + temp_day.strftime("%m-%d") + ".json"):
            subprocess.call(["python", "parser_date.py", date])

        with open(
            "datas/" + temp_day.strftime("%m-%d") + ".json", "r", encoding="utf-8"
        ) as f:
            res = ""
            result = json.loads(f.read())
            for meal in result["meals"]:
                if meal["date"] == today.strftime("%Y-%m-%d"):
                    res = json.dumps(meal, ensure_ascii=False, indent=4)
            if res == "":
                res = make_response(
                    json.dumps({"error": "No data"}, ensure_ascii=False, indent=4)
                )
                f.close()
                os.remove("datas/" + temp_day.strftime("%m-%d") + ".json")
            else:
                res = make_response(res)

            return res


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
