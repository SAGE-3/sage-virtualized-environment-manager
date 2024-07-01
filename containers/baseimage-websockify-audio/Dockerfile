FROM debian:bookworm-slim

RUN apt-get update
RUN apt-get -y install --no-install-recommends websockify nginx nginx-extras
# RUN rm -rf /var/lib/apt/lists/*

# https://github.com/novnc/websockify
# openssl req -new -x509 -days 365 -nodes -out self.pem -keyout self.pem

WORKDIR /
COPY configs/nginx.conf /etc/nginx/nginx.conf
COPY websockify_proxy.sh .
RUN chmod +x websockify_proxy.sh