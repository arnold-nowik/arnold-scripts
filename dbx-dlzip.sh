#!/bin/bash
echo "======================================="
echo "        Dropbox Zip Download API       "
echo "======================================="
echo "Please set a valid Oauth Token:"
read -r TOKEN
echo "Target folder (with preceding slash):"
read -r "FOLDER"
echo ""
curl -X POST --output ./${FOLDER}.zip https://content.dropboxapi.com/2/files/download_zip \
--header "Authorization: Bearer $TOKEN" \
--header "Dropbox-API-Arg: {\"path\":\"$FOLDER\"}"
