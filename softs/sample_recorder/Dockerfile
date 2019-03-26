FROM ubuntu:latest

RUN apt update && apt upgrade -y
RUN apt install -y python3-venv python3-dev build-essential python3-pip

RUN mkdir /root/project
COPY . /root/project

WORKDIR /root/project
RUN make dll
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "sample_recorder.py" ]