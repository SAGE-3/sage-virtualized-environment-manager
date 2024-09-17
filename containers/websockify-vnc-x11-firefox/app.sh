#!/bin/bash

# 0:dark, 1:light, or 2:auto
echo 'lockPref("browser.theme.content-theme", '$FIREFOX_THEME');' >> /lib/firefox-esr/vnc.cfg
echo 'lockPref("browser.theme.toolbar-theme", '$FIREFOX_THEME');' >> /lib/firefox-esr/vnc.cfg
echo 'lockPref("startup.homepage_welcome_url", "'$FIREFOX_STARTPAGE'");' >> /lib/firefox-esr/vnc.cfg

urls_string="${FIREFOX_URLS//[\[\]\'\"]}"  # Remove square brackets and quotes
urls_string="$(echo $urls_string | xargs)"  # Trim any extra spaces
IFS=',' read -r -a urls <<< "$urls_string" # Split the string into an array using commas as the delimiter

./callback.sh &

while true; do
    firefox "${urls[@]}"
    sleep 0.1
done;