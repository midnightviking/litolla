import os
import yaml
import requests

class LLMAvailability:
    model_list = []
    running_list = []
    def __init__(self, name, prefix, port):
        self.status = 0
        self.size   = ''
        self.valid  = 0
        self.name   = name if name else ""
        self.prefix = prefix if prefix else ""
        self.port   = port if port else 4200
        self.isRunning = False
        LLMAvailability.model_list.append(name)

    def __str__(self):
        return f"{self.name} - {self.status} - {self.size} - {self.valid}"
    def set_size(self, size):
        self.size = size
    def set_status(self, status):
        self.status = status
    def set_valid(self, valid):
        self.valid = valid
    def set_port(self, port):
        self.port = port
    def set_running(self, running):
        self.isRunning = running
        if(running):
            LLMAvailability.running_list.append(self.name)
        else:
            LLMAvailability.running_list.remove(self.name)

    def get_name(self):
        return self.name
    def get_status(self):
        return self.status
    def get_size(self):
        return self.size
    def get_port(self):
        return self.port
    def get_valid(self): 
        return self.valid
    def get_running(self):
        return self.isRunning

    def get_retrevable_name(self):
        return self.prefix + "/" + self.name

    def get_model(model):
        if model in LLMAvailability.model_list:
            return model
        else:
            return None


available_models = []

def load_available_models():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_and_prefix_path = os.path.join(current_dir, 'models_and_prefix.yaml')
    try:
        with open(models_and_prefix_path, 'r') as file:
            data = yaml.safe_load(file)

            for m in data['models']:
                available_models.append(LLMAvailability(m['name'], m['prefix'], m['port']))
    except Exception as e:
        print(f"Error loading available models: {e}")

    return LLMAvailability.model_list

def get_available_models():
    if(len(available_models) == 0):
        load_available_models()
        get_download_status() # also get the size and status of the models, only Ollama for the moment
    return available_models

def get_model(model_name):
    if(len(available_models) == 0):
        load_available_models()
    for model in available_models:
        if model.get_name() == model_name:
            return model
    return None

def get_download_status():
    if(len(available_models) == 0):
        load_available_models()

    req = requests.get("http://localhost:11434/api/tags")
    if(req.status_code == 200):
        ollamaModelsInstalled = req.json()
    if not ollamaModelsInstalled:
        return available_models

    for model in available_models:
        for installed_model in ollamaModelsInstalled["models"]:
            nicename = installed_model["name"].split(":")[0]
            if model.get_name() == nicename:
                model.set_status(1)
                size = installed_model["size"]
                if size >= 1024**3:
                    model.set_size(f"{size / 1024**3:.2f} GB")
                elif size >= 1024**2:
                    model.set_size(f"{size / 1024**2:.2f} MB")
                elif size >= 1024:
                    model.set_size(f"{size / 1024:.2f} KB")
                else:
                    model.set_size(f"{size} B")
                break
    return available_models

def get_models_json():
    models = []
    try:
        # update current status of the models
        get_available_models()
        get_download_status()
        for model in available_models:
            models.append({"name": model.get_name(), "status": model.get_status(),"size": model.get_size(), "port": model.get_port(), "running": model.get_running()})
    except Exception as e:
        print(f"Error getting models JSON: {e}")
    return models