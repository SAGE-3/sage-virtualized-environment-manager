#!/bin/bash

# Check if XPI path is provided
if [ $# -eq 0 ]; then
  echo "Error: Please provide the path to the XPI file as an argument."
  exit 1
fi

XPI_PATH="$1"

# Extract the add-on ID from the XPI (WebExtensions)
ADDON_ID=$(unzip -p "$XPI_PATH" manifest.json | grep -oP '(?<="id": ")[^"]+')

# Exit if ID extraction fails
if [ -z "$ADDON_ID" ]; then
  echo "Failed to extract add-on ID. Check if the XPI contains a valid manifest.json."
  exit 1
fi

# Find all default-release profiles (Linux/macOS/Windows WSL)
for PROFILE_DIR in \
  "$HOME/.mozilla/firefox/"*".default-esr"
#   "$HOME/Library/Application Support/Firefox/Profiles/"*".default-release" \
#   "/mnt/c/Users/$USER/AppData/Roaming/Mozilla/Firefox/Profiles/"*".default-release"
do
  if [ -d "$PROFILE_DIR" ]; then
    # Create extensions directory if missing
    mkdir -p "$PROFILE_DIR/extensions"
    # Copy the XPI with the addon ID as the filename
    cp "$XPI_PATH" "$PROFILE_DIR/extensions/${ADDON_ID}.xpi"
    echo "Installed to: $PROFILE_DIR/extensions/"
  fi
done

echo "Done! Restart Firefox to see the add-on."