from flask import Flask, make_response
from flask_restx import Api, Resource
import datetime
import os
import json

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
api = Api(app)

@api.route('/bob')
class Bob(Resource):
  def get(self):
    today = datetime.date.today()
    today -= datetime.timedelta(days=today.weekday())
    if(not os.path.exists('datas/'+ today.strftime('%m-%d') + '.json')):
      exec(open('parser.py', encoding='utf-8').read())
    with open('datas/'+ today.strftime('%m-%d') + '.json', 'r', encoding='utf-8') as f:
      result = json.loads(f.read())
      result = json.dumps(result, ensure_ascii=False, indent=4)
      res = make_response(result)
      return res

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
  
