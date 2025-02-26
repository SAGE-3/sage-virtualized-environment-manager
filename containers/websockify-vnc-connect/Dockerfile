FROM websockify-baseimage

WORKDIR /

COPY entrypoint.sh .

RUN chmod +x *.sh

ENTRYPOINT [ "./entrypoint.sh" ]