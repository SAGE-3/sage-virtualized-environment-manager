FROM websockify-baseimage:latest

WORKDIR /

COPY entrypoint.sh .

RUN chmod +x *.sh

ENTRYPOINT [ "./entrypoint.sh" ]