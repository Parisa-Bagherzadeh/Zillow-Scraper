# build docker image with python 3.9
FROM ubuntu:20.04
ENV TZ=America/New_York
RUN apt update && \
    apt install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app
RUN apt install libgl1-mesa-glx -y
RUN apt install -y ca-certificates curl gnupg lsb-release
RUN  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt update
RUN apt-get update -y
RUN apt install -y iputils-ping
RUN apt install -y jq
RUN apt install -y docker-ce-cli
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y nano
RUN apt-get install ffmpeg libsm6 libxext6  -y

# install the requirements
RUN pip install --upgrade pip

RUN pip install selenium
RUN pip install beautifulsoup4
RUN pip install easydict


# copy file from local to docker
# COPY . /app

