#!/bin/bash

set -e

if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /path/to/extension.xpi"
    exit 1
fi

XPI_FILE="$1"

if [ ! -f "$XPI_FILE" ]; then
    echo "Error: File not found at $XPI_FILE"
    exit 1
fi

# Extract the add-on ID from the manifest.json
ADDON_ID=$(unzip -p "$XPI_FILE" manifest.json | grep '"id":' | cut -d '"' -f 4)

if [ -z "$ADDON_ID" ]; then
    echo "Error: Could not extract add-on ID from $XPI_FILE"
    exit 1
fi

# Common Firefox installation directories
FIREFOX_DIRS=("/usr/lib/firefox-esr" "/usr/lib/firefox" "/opt/firefox")
FIREFOX_INSTALL_DIR=""

for DIR in "${FIREFOX_DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        FIREFOX_INSTALL_DIR="$DIR"
        break
    fi
done

if [ -z "$FIREFOX_INSTALL_DIR" ]; then
    echo "Error: Could not find Firefox installation directory."
    exit 1
fi

EXTENSIONS_DIR="$FIREFOX_INSTALL_DIR/distribution/extensions"

mkdir -p "$EXTENSIONS_DIR"

cp "$XPI_FILE" "$EXTENSIONS_DIR/$ADDON_ID.xpi"

echo "Extension successfully installed. It will be available on the next Firefox launch."

exit 0
