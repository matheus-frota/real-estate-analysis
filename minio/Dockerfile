FROM minio/minio

COPY create_bucket.sh .

RUN chmod +x ./create_bucket.sh

ENTRYPOINT [ "./create_bucket.sh" ]