#!/bin/bash
echo "Starting the app";
python3 app.py &\
ollama serve & litellm;


