FROM frolvlad/alpine-python3
COPY requirements.txt .
RUN apk add --update --no-cache g++ gcc libxslt-dev python3-dev
RUN pip3 install -r requirements.txt --upgrade
COPY src /usr/local/qasimodo/
CMD python3 /usr/local/qasimodo/qasimodo.py
