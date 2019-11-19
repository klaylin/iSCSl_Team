
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, make_response
import json
from flask_cors import *
import IblockCreate as IC

app = Flask(__name__)  # 实例化app对象
CORS(app, resources=r'/*')  
message_get_ll = None

@app.route('/send_message', methods=['GET'])
def send_message():
    global message_get_ll
    global message
    
    name = request.args['name']
    password = request.args['password']

    if name and password:
      message_get_ll = IC.iblock_create(name,password)
      if message_get_ll:
  	      message = "successful"
      else:
          message = "please see the fail.log"
            #return message_get_ll
        return message
    else:
        pass

@app.route('/data', methods=['GET', 'POST'])  # 路由
def test_post():
    global message_get_ll
    response = make_response(jsonify(message_get_ll))
    # 这里是解决Flask文件数据跨域问题，重要包导入 pip install flask_cors
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response



@app.route('/', methods=['GET', 'POST'])
def INDEX():
    return render_template("index.html")

  
@app.route('/create', methods=['GET', 'POST'])
def CREATE():
        return render_template("create.html")
   
    
@app.route('/show', methods=['GET', 'POST'])
def SHOW():
        return render_template("show.html")


@app.route('/delete', methods=['GET', 'POST'])
def Delete():
        return render_template("delete.html")
  
  
if __name__ == '__main__':
  app.run(host='0.0.0.0',  # 任何ip都可以访问
      port=7777,  # 端口
      debug=True
      )
