FROM python:3.10.14-bullseye

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y install nginx

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN chmod 777 *.sh

COPY nginx/nginx.conf.template /etc/nginx/nginx.conf.template
COPY nginx/nginx.conf /etc/nginx/nginx.conf

CMD ["./run.sh"]