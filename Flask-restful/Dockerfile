FROM python:3.6.5
RUN mkdir -p /flask-restful
COPY . /flask-restful
RUN pip install -r /flask-restful/requirements.txt
WORKDIR /flask-restful
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
