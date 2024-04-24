# Ollama/Litellm with Autogen Studio UI and MongoDB backend.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description
Containerized Agent UI. Quick way to seperate everything and serve out various LLMs to interface with.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
	- [Setup and download the models](#setup-and-download-the-models)
	- [Using the database](#using-the-database)	
	- [Autogen Studios UI](#autogen-studios-ui)

## Installation

- To get started, make sure you have Docker installed on your machine. If you're using Windows, you can install Docker Desktop.
- Open the file `containers/ollamalitellm/models_and_prefix.yaml` and add the models you want to include in the interface. This file allows you to configure the available models.
- If you want to include chatGPT or other openAI services, you can modify the `containers/ollamalitellm/litellm-config.yaml` file. This file allows you to configure additional services.
- Lastly, add an `.env` file in the root directory and include the following variables to access the mongo database.
	```yaml
	MONGOADMIN_USER=root
	MONGOADMIN_PASS=example
	MONGOUSER = root #udate to whatever user you setup in mongo express
	MONGOPASS = example #udate to whatever pass you setup in mongo express
	```

The compose will automatically create 3 different persistent volumes.
```py
# So you don't have to redownload the LLMs each time, but they are seperate from your machine
projectname_LLMS 
#the database
project_name_mongodb 
# so your agents persist
project_name_AGS 

```

## Usage

After completing the above steps, you can start using the project. Here are some important details:

- The model download and proxy activation will be available at [`localhost:5000`](http://localhost:5000).
- Autogen Studio will be accessible at [`localhost:8081`](http://localhost:8081).
- Mongo Express Admin will be accessible at [`localhost:8082`](http://localhost:8082).
- Agents can use the network `ollamalitellm:port` as their URL to access the proxy. For example, llama3 can be accessed by using `http://ollamalitellm:4101` in the agent URL.
- You can also see the LiteLLM fastAPI interface at [`localhost:4000`](http://localhost:4000)

If you need to customize the project further, you can edit the `containers/ollamalitellm/app.py` file. It is running Flask in dev mode, so any changes you make will automatically refresh without needing to restart the service.

### Setup and download the models
Visit [`localhost:5000`](http://localhost:5000)
Select the model you want to download and start up. If its already downloaded it'll verify the installation and start serving it on the proxy. You will need to select them each time you restart the container in order to serve them until I get a persistent solution, probably a default serve in the compose file. Maybe another yaml autoload?


### Using the database
The exposed connection string is `os.environ['MONGO_CONNSTRING']`
I don't know why, but at the moment I cannot get autogen studios to recognize the OS variables. So I'm hardcoding the connection in the skill which is equivilant to : `mongodb://root:example@mongo:27017/`

For example, a note saving skill in Autogen Studios:
```py
## 1. Imports
from pymongo import MongoClient

## 2. Function definition
def save_dbnote(data:str):
	"""
	Save a note to a MongoDB collection

	Parameters:
	note (str): The note to be saved

	"""
	## 3. Function body
	connString = "mongodb://root:example@mongo:27017/" # os.environ["MONGO_CONNSTRING"] doesnt work
	try:
		#connect to the MongoDB server
		client = MongoClient(connString)
		#connect to the database
		db = client['test']
		#connect to the collection
		collection = db['notes']
		#insert the note into the collection
		x = collection.insert_one({"note":data})
		#close the connection
		client.close()
		#return a success message
		return "Succeeded"
	except Exception as e:
		#return an error message
		return f"Failed to save data to MongoDB : " + str(e)

```
Manage the DB at [`localhost:8082`](http://localhost:8082).

### Autogen Studios UI
Found at [`localhost:8081`](http://localhost:8081)


