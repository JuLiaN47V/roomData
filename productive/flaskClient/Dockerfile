FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y telnet python3.7 python3-pip python3.7-dev
RUN python3.7 -m pip install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3.7" ]

CMD [ "app.py" ]
