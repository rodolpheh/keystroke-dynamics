FROM ubuntu:latest

RUN apt update && apt upgrade -y
RUN apt install -y python3-venv python3-dev build-essential python3-pip

RUN mkdir /root/project
WORKDIR /root/project

COPY requirements.txt /root/project

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /root/project
RUN make dll


ENTRYPOINT [ "python3", "hello.py" ]