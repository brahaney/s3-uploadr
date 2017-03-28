# s3-uploadr
Simple docker S3 uploader

```
docker run --rm -v $(pwd):/data brahaney/s3-uploadr  \
--file my-file.jpg \
--name my-file-in-s3.jpg \
--bucket my-awesome-bucket \
--aws_access_key $AWS_ACCESS_KEY \
--aws_secret_key $AWS_SECRET_KEY \
--public
```