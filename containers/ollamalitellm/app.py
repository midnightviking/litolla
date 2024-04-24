import json
import os
from flask import Flask, render_template
import requests as req
import subprocess
import model_objectify
from flask_socketio import SocketIO

from litellm import completion
from litellm import utils as litellm_utils
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


mongoURI = os.environ["MONGO_CONNSTRING"] or "mongodb://mongo:27017" # get the connection string from the environment

app = Flask(__name__)
socketio = SocketIO(app)

# get the models setup
model_objectify.get_available_models()
availableModels = model_objectify.get_models_json()
mport = 4200 # just port for models that are missing a port in the config file
data = {
    "models": availableModels,
    "model_list": model_objectify.get_available_models(),
    "selectedModel"  : None,
    "ollamaStatus"   : None,
    "liteLLMStatus"  : None,
    "ollamaAvailableModels": {} ,
}

async def getOllamaStatus():
    res = req.get("http://localhost:11434/")
    status = 0
    if res.status_code == 200:
        status = 1
    data["ollamaStatus"] = status
    # grab the status of the models too
    model_objectify.get_download_status()
    return status

async def getLiteLMSStatus():
    res =  req.get("http://localhost:4000/health/liveliness")
    status = 0
    if res.status_code == 200:
        status = 1
    data["liteLLMStatus"] = status
    return status

#interface
# Index
@app.route("/")
def index():
    return render_template('index.html', data=data)

# This route will be used to get the models
@app.route("/models", methods=['GET'])
def models():
    data["models"] = model_objectify.get_models_json()
    # see if models are being served on liteLLM
    
    return  {"models": data["models"], "selectedModel": data["selectedModel"]}

# This route will be used to select the model
@app.route("/model/<model_name>", methods=['GET','POST'])
def model(model_name):
    model = None
    valid = False
    if model_name in model_objectify.LLMAvailability.model_list:
        model = model_objectify.get_model(model_name)
        if model is not None:
            data["selectedModel"] = model_name
            completed = "0%"
            _data = {
                "model": model_name
            }
            datam = json.dumps(_data)
            res = req.post("http://0.0.0.0:11434/api/pull",data=datam, stream=True)
            #stream to socketio
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    j = json.loads(chunk.decode('utf-8'))
                    if(j["status"] == "success"):
                        valid = True
                    if("completed" in j and "total" in j ):
                        completed = str(round((j["completed"] / j["total"])*100)) + "%"
                    socketio.emit('model-download', {'data': j, "progress": completed, "model": model_name})

        else:
            data["selectedModel"] = None
            return False

    else:
        data["selectedModel"] = None
        return False
    if(valid):
        # check if the model has a port
        if(model.get_port() == None):
            global mport
            model.set_port(str(mport))
            mport += 1
        # start the model proxy
        model.set_running(True)
        subprocess.Popen(["litellm", "--model", model.get_retrevable_name(), "--port", model.get_port(), "--api_base", "http://localhost:11434"])

    return {"name": model.get_name(), "valid": valid, "size": model.get_size(), "port": model.get_port(), "running": model.get_running()}

@app.route("/service-request", methods=['GET'])
async def status():
    ollama = await getOllamaStatus()
    liteLLM = await getLiteLMSStatus()
    return {
        "ollama"  : ollama,
        "liteLLM" : liteLLM,
        "model"   : data["selectedModel"],
    }

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('connect')
def test_connect():
    print('Client connected')

@app.route("/test-mongo", methods=['GET'])
def test_mongo():
    try:
        client = MongoClient(mongoURI)
        db = client['test']
        collection = db['notes']
        collection.insert_one({"note":"A note yet again"})
        client.close()
        return {"message": "success", "mongoURI": mongoURI}
    except Exception as err:
            return {"message": str(err), "error": "Failed to save data to MongoDB", "mongoURI": mongoURI}
        # return {"message": "no connection", "error": "ConnectionFailure " + str(ConnectionFailure)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, )
    socketio.run(app)