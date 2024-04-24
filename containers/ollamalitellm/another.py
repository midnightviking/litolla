# import requests as req

m_list = [
    'llama2',
    'mistral',
    'codellama',
    'llama2-uncensored',
    'dolphin-mistral',
    'zephyr',
    'samantha-mistral',
    'openchat',
    'neural-chat',
    'wizardcoder',
    'mixtral',
]
availableModels = []

class LLMAvailability:
    model_list = []
    def __init__(self, name, prefix):
        self.status = 0
        self.size = '--'
        self.valid = 0
        self.name = name
        self.prefix = prefix
        LLMAvailability.model_list.append(name)

    def __str__(self):
        return f"{self.name} - {self.status} - {self.size} - {self.valid}"
    def set_size(self, size):
        self.size = size
    def set_status(self, status):
        self.status = status
    def set_valid(self, valid):
        self.valid = valid

    def get_name(self):
        return self.name
    def get_status(self):
        return self.status
    def get_size(self):
        return self.size

    def get_retrevable_name(self):
        return self.prefix + "/" + self.name

    def get_model(model):
        if model in LLMAvailability.model_list:
            return model
        else:
            return None


for model in m_list:
    availableModels.append(LLMAvailability(model, "ollama_chat"))



data = {
    "availableModels": availableModels,
    "selectedModel"  : None,
    "ollamaStatus"   : None,
    "liteLLMStatus"  : None,
    "ollamaAvailableModels": {} ,
}

def checkModelStatus():
    ollamaModelsInstalled = {"models":[{"name":"llama2:latest","model":"llama2:latest","modified_at":"2024-03-25T18:03:18-04:00","size":3826793677,"digest":"78e26419b4469263f75331927a00a0284ef6544c1975b826b15abdaef17bb962","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama"],"parameter_size":"7B","quantization_level":"Q4_0"}},{"name":"mistral:latest","model":"mistral:latest","modified_at":"2024-03-25T17:55:15-04:00","size":4109865159,"digest":"61e88e884507ba5e06c49b40e6226884b2a16e872382c2b44a42f2d119d804a5","details":{"parent_model":"","format":"gguf","family":"llama","families":["llama"],"parameter_size":"7B","quantization_level":"Q4_0"}}]}
    for model in data["availableModels"]:
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

checkModelStatus()
for model in data["availableModels"]:
    print(model)