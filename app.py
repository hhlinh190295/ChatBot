# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import aiml

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)
CORS(app, resource=r'/ask/*')
# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Hello(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # Corresponds to POST request
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str)
        args = parser.parse_args()
        text = format(args['text'])

        kernel = aiml.Kernel()


        if os.path.isfile("Model/model.brn"):
            kernel.bootstrap(brainFile = "Model/model.brn")
        else:
            kernel.bootstrap(learnFiles = os.path.abspath("AIML_Files/startup.xml"), commands = "load aiml")
            kernel.saveBrain("Model/model.brn")

        # kernel now ready for use
        while True:
            if text == "quit":
                exit()
            elif text == "save":
                kernel.saveBrain("Model/model.brn")
            else:
                bot_response = kernel.respond(text)
                # print bot_response
                return jsonify({'status':'OK','answer':bot_response})

            # data = request.get_json()     # status code
            # print('Text: ' + text)
            # return jsonify({'data': text})


class GetTest(Resource):
        def get(self):
            return jsonify({'status':'OK','answer': 'haha'}

# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/ask/')
api.add_resource(GetTest, '/ask/')


# driver function
if __name__ == '__main__':

    app.run(debug = True)
