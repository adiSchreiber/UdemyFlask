from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


def check_posted_data(postedData, functionName):
    if functionName in ["add", "subtract", "multiply", "divide"]:
        if 'x' not in postedData or 'y' not in postedData:
            return 301 #Missing paramater
        elif type(postedData['x']) !=int and type(postedData['y']) != int:
            return 415
        elif functionName == "divide" and postedData["y"] == 0:
            return 302
        return 200


def error_response_json(status_code):
    json = {
        "Message": "An Error happened",
        "status_code": status_code
    }
    return json


def get_response_by_function_name(function_name, x, y) -> int:
    if function_name == "add":
        return x+y
    if function_name == "subtract":
        return x-y
    if function_name == "multiply":
        return x*y
    if function_name == "divide":
        return x/y


def post_request(function_name: str):
    postedData = request.get_json()
    status_code = check_posted_data(postedData, function_name)
    if status_code != 200:
        return jsonify(error_response_json(status_code))
    x = postedData['x']
    y = postedData['y']
    x = int(x)
    y = int(y)
    result = get_response_by_function_name(function_name, x, y)
    retMap = {
        'Message': result,
        'Status Code': status_code
    }
    return jsonify(retMap)


class Add(Resource):
    def post(self):
        return post_request("add")


class Subtract(Resource):
    def post(self):
        return post_request("subtract")


class Multiply(Resource):
    def post(self):
        return post_request("multiply")


class Divide(Resource):
    def post(self):
        return post_request("divide")


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")


@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/hithere")
def hi_there():
    return "saying hi!"


@app.route("/add_two_nums", methods=["POST"])
def add_two_nums():
    dataDict = request.get_json()
    if "x" not in dataDict:
        return "ERROR", 305
    x = dataDict["x"]
    y = dataDict["y"]
    z = x + y

    retJSON = {
        "z": z
    }
    return jsonify(retJSON), 200


@app.route("/bye")
def bye():
    name = "Adi"
    json = {
        "name": name,
        "Age": "21",
        "phones": [
            {
                "phoneName": "iphone8",
                "phoneNumber": "0000"
            },
            {
                "phoneName": "Nokia",
                "phoneNumber": "1111"
            }
        ]
    }
    return jsonify(json)


if __name__ == "__main__":
    app.run()
