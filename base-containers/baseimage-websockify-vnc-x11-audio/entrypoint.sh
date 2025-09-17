#!/bin/bash
DESKTOP_WIDTH=1024
DESKTOP_HEIGHT=768
VNC_PORT=5900

mkdir -p ~/.config/openbox
cat > ~/.config/openbox/rc.xml <<EOL
<?xml version="1.0" encoding="UTF-8"?>
<openbox_config xmlns="http://openbox.org/3.4/rc" xmlns:xi="http://www.w3.org/2001/XInclude">
  <applications>
    <application class="*"> <decor>no</decor> </application>
  </applications>
</openbox_config>
EOL

# echo 'dbus-launch --autolaunch=$(cat /var/lib/dbus/machine-id) --exit-with-session' > ~/.config/openbox/autostart
# chmod 777 ~/.config/openbox/autostart

# Start Virtual Frame Buffer and VNC
echo "Starting Virtual Frame Buffer and VNC..."
/opt/TurboVNC/bin/vncserver :99 -geometry ${DESKTOP_WIDTH}x${DESKTOP_HEIGHT} -depth 16 -localhost -rfbport ${VNC_PORT} -SecurityTypes None -noxstartup

export DISPLAY=:99

# Start Desktop Enviroment
echo "Starting DE..."
# export $(dbus-launch)
/etc/init.d/dbus start

# /etc/init.d/pulseaudio-enable-autospawn start

# Configure PulseAudio
mkdir -p /etc/pulse/default.pa.d
echo "load-module module-null-sink sink_name=virtual_output" > /etc/pulse/default.pa.d/virtual-sink.pa
echo "set-default-sink virtual_output" >> /etc/pulse/default.pa.d/virtual-sink.pa

# Start PulseAudio
pulseaudio --start --exit-idle-time=-1 &


# pulseaudio &
# /etc/init.d/dbus status
# dbus-launch openbox &
openbox &
# pulseaudio --system &
# ffmpeg -loglevel debug -re -f alsa -i pulse -acodec libmp3lame -b:a 128k -f mp3 -content_type audio/mpeg -tune zerolatency -listen 1 -http_persistent 1 http://0.0.0.0:7772 &


# ffmpeg -f alsa -i pulse -f mpegts -codec:a mp2 udp://localhost:7773 &
# websockify 0.0.0.0:7772 localhost:7773 &


# pulseaudio --start --exit-idle-time=-1 && \
#   ffmpeg -loglevel debug -re -f alsa -i pulse -acodec libmp3lame -b:a 128k -f mp3 -content_type audio/mpeg -listen 1 -http_persistent 1 http://0.0.0.0:7772 &
# ffmpeg -loglevel debug -re -f alsa -i pulse -acodec libmp3lame -b:a 128k -f mp3 -content_type audio/mpeg -method GET http://localhost:7772 &
# openbox &

# while ! xdpyinfo -display :99 >/dev/null 2>&1; do
#     sleep 0.1
# done

echo "Starting Audio Service..."
python3 /audio_websocket_server.py &
# python3 /audio_http_server.py &



echo "Starting User App..."
$1 &

echo "DONE"
./websockify_proxy.sh
./screenshot_callback.sh

$2
