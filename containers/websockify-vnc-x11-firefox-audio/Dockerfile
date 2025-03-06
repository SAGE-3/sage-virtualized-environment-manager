FROM vnc-x11-audio-baseimage:latest

RUN apt-get -y install --no-install-recommends firefox-esr

ENV FIREFOX_THEME=0
ENV FIREFOX_STARTPAGE="about:home"

WORKDIR /

COPY configs/vnc.js /lib/firefox-esr/defaults/pref/
COPY configs/vnc.cfg /lib/firefox-esr/


COPY app.sh .
COPY app_safe_shutdown.sh .
RUN chmod +x *.sh

CMD ["./app.sh", "./app_safe_shutdown.sh"]