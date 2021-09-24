#!/bin/bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
export PATH=$PATH:/usr/local/bin/aws
echo "=============================="
echo "Zaktualizuj NTP server!!!!!!"
echo "'aws s3 cp nazwapliku s3://bucket_name --storage-class DEEP_ARCHIVE'"
echo "'aws s3api list-objects-v2 --bucket bucket_name'"
