FROM vnc-x11-baseimage

RUN apt-get -y install --no-install-recommends blender


WORKDIR /

COPY app.sh .
COPY app_safe_shutdown.sh .
RUN chmod +x *.sh

CMD ["./app.sh", "./app_safe_shutdown.sh"]
