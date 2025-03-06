FROM vnc-x11-baseimage:latest

RUN apt-get -y install --no-install-recommends firefox-esr wget unzip build-essential jq curl

ENV FIREFOX_THEME=0
ENV FIREFOX_STARTPAGE="about:home"
ENV FIREFOX_URLS=[]

WORKDIR /

# RUN git https://github.com/avih/dejsonlz4.git
RUN wget --no-check-certificate https://github.com/avih/dejsonlz4/archive/refs/heads/master.zip
RUN unzip master.zip
RUN gcc -Wall -o dejsonlz4 dejsonlz4-master/src/dejsonlz4.c dejsonlz4-master/src/lz4.c

COPY configs/vnc.js /lib/firefox-esr/defaults/pref/
COPY configs/vnc.cfg /lib/firefox-esr/

# Plugins
# RUN wget --no-check-certificate https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi -O ublock-origin.xpi \
#     && mkdir -p /lib/firefox-esr/browser/extensions \
#     && cp ublock-origin.xpi /lib/firefox-esr/browser/extensions/ublock@raymondhill.net.xpi \
#     && rm ublock-origin.xpi
# # Install uBlock Origin extension system-wide
# RUN mkdir -p /lib/firefox-esr/distribution/extensions && \
#     wget -O /lib/firefox-esr/distribution/extensions/ublock0@raymondhill.net.xpi \
#     --no-check-certificate https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi

COPY configs/install_plugin.sh .
RUN chmod +x install_plugin.sh
RUN wget --no-check-certificate https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi -O ublock-origin.xpi \
    && ./install_plugin.sh ublock-origin.xpi


COPY app.sh .
COPY callback.sh .
COPY app_safe_shutdown.sh .
RUN chmod +x *.sh

# RUN apt-get -y install --no-install-recommends iputils-ping

CMD ["./app.sh", "./app_safe_shutdown.sh"]