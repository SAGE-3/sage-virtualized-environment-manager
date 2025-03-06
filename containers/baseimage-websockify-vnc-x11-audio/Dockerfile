FROM websockify-baseimage-audio:latest

# xvfb + x11vnc seems to lack extended desktop size support
# RUN apt-get -y install --no-install-recommends xvfb openbox x11vnc
# RUN apt-get -y install --no-install-recommends tigervnc-standalone-server tigervnc-tools
RUN apt-get update
RUN apt-get -y install --no-install-recommends x11-utils dbus-x11 xauth x11-xkb-utils xkb-data ffmpeg pulseaudio dbus

WORKDIR /
COPY apps/turbovnc_3.1.1_amd64.deb .

RUN dpkg -i turbovnc*.deb
RUN apt install -f

RUN apt-get -y install --no-install-recommends openbox


# ENV WS_PORT=2222
ENV TARGET_IP=localhost
ENV TARGET_PORT=5900

COPY stream_audio.py .
COPY entrypoint.sh .

RUN chmod +x *.sh

ENTRYPOINT [ "./entrypoint.sh" ]