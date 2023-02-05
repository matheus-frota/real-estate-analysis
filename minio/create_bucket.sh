#!/bin/sh

echo "Creating bucket $DEFAULT_BUCKET"

mkdir -p /data/$DEFAULT_BUCKET \
    && minio server /data