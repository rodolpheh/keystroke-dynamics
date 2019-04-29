FROM alpine:latest

RUN mkdir /root/project
WORKDIR /root/project
COPY keylogger.c ./
COPY keylogger.h ./
COPY Makefile ./
COPY requirements.txt ./

RUN apk --no-cache add linux-headers g++ make \
 && make dll \
 && apk del make g++ linux-headers

COPY requirements.txt ./
RUN apk --no-cache add python3 python3-dev openblas-dev openblas gfortran g++ make libstdc++ \
 && pip3 install --no-cache-dir --upgrade pip \
 && pip3 install --no-cache-dir --only-binary all --prefer-binary -r requirements.txt \
 && apk del openblas-dev gfortran python3-dev make g++

COPY . /root/project

ENTRYPOINT [ "python3", "hello.py" ]
