FROM ollama/ollama as ollama

RUN apt-get update && apt-get install -y curl gpg
RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
	&& curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
	sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
	tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

RUN apt-get update
#python
RUN apt-get install -y python3 python3-pip
#install nvidia-container-toolkit for gpu pass through
RUN apt-get install -y nvidia-container-toolkit
#jump to dir, set in compose though
WORKDIR /app

#copy files
COPY . .

#install requirements
RUN pip install -r requirements.txt

#litellm expose
EXPOSE 4000

#admin expose
EXPOSE 5000
ENTRYPOINT [ "/bin/bash", "start.sh" ]