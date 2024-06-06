#!/bin/bash

printXLSXApps(){
# Directory containing .desktop files
local dir=$1
# Check if directory exists
if [ -d "$dir" ]; then
  # Find .desktop files
  local files=$(find "$dir" -name "*.desktop")

  # Check each .desktop file
  for file in $files; do
    # Extract 'Name', 'MimeType', 'Categories', and 'Keywords' parameters
    local name=$(awk -F= '/\[Desktop Entry\]/,/Name=/ { if ($1 == "Name") print $2 }' "$file")
    local mime_type=$(grep -E '^MimeType=' "$file" | cut -d'=' -f2)
    local categories=$(grep -E '^Categories=' "$file" | cut -d'=' -f2)

    # Check if 'MimeType' supports OpenDocument SPREADSHEET and Microsoft EXCEL formats
    if [[ $mime_type == *"application/vnd.oasis.opendocument.spreadsheet"* || $mime_type == *"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"* ]] && [[ $categories == *"Office"* ]]; then
        echo "$name||$file"
        echo ";"
    fi
  done
else
    # if directory not found then print nothing and exit function
  :
fi
}

# Call the function with the provided directories
printXLSXApps "$HOME/.local/share/flatpak/exports/share/applications/"
printXLSXApps "/usr/share/applications/"
printXLSXApps "/var/lib/flatpak/exports/share/applications/"

echo EOS

