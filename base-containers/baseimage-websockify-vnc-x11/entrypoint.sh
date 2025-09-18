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

# Start Virtual Frame Buffer and VNC
echo "Starting Virtual Frame Buffer and VNC..."
/opt/TurboVNC/bin/vncserver :99 -geometry ${DESKTOP_WIDTH}x${DESKTOP_HEIGHT} -depth 16 -localhost -rfbport ${VNC_PORT} -SecurityTypes None -noxstartup

export DISPLAY=:99

# Start Desktop Enviroment
echo "Starting DE..."
openbox &

# while ! xdpyinfo -display :99 >/dev/null 2>&1; do
#     sleep 0.1
# done

echo "Starting User App..."
$1 &

echo "DONE"
./websockify_proxy.sh
./screenshot_callback.sh

$2
