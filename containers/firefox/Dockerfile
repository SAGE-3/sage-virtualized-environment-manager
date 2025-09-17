FROM vnc-x11-audio-baseimage

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
COPY configs/install_plugin.sh .

# Plugins
# RUN firefox -CreateProfile "default-esr" --headless
RUN wget --no-check-certificate https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi -O ublock-origin.xpi && ./install_plugin.sh ublock-origin.xpi

# These have startup pages, not sure how to disable the startup pages for now
# RUN wget --no-check-certificate https://addons.mozilla.org/firefox/downloads/latest/sponsorblock/latest.xpi -O sponsorblock.xpi && ./install_plugin.sh sponsorblock.xpi
# RUN wget --no-check-certificate https://addons.mozilla.org/firefox/downloads/latest/return-youtube-dislikes/latest.xpi -O return-youtube-dislikes.xpi && ./install_plugin.sh return-youtube-dislikes.xpi

# # Use Firefox's built-in installer
# RUN timeout 30 xvfb-run -a firefox-esr -install-global-extension /ublock-origin.xpi --new-instance --no-remote || true && \
#     rm ublock-origin.xpi

COPY app.sh .
COPY callback.sh .
COPY app_safe_shutdown.sh .
RUN chmod +x *.sh

# RUN apt-get -y install --no-install-recommends iputils-ping

CMD ["./app.sh", "./app_safe_shutdown.sh"]