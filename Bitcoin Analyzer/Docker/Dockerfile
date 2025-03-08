FROM python:3.8
RUN apt-get update && mkdir temp/

COPY ./requirements.txt /temp/requirements.txt
RUN pip3 install -r /temp/requirements.txt

COPY ./live.py /temp/live.py
WORKDIR /temp

ENV PYTHONUNBUFFERED=1

CMD ["python3","live.py"]
