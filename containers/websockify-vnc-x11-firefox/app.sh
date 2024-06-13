#!/bin/bash

# 0:dark, 1:light, or 2:auto
echo 'lockPref("browser.theme.content-theme", '$FIREFOX_THEME');' >> /lib/firefox-esr/vnc.cfg
echo 'lockPref("browser.theme.toolbar-theme", '$FIREFOX_THEME');' >> /lib/firefox-esr/vnc.cfg
echo 'lockPref("startup.homepage_welcome_url", "'$FIREFOX_STARTPAGE'");' >> /lib/firefox-esr/vnc.cfg

while true; do
    firefox
    sleep 0.1
done;