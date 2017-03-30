import tinys3
import os
import argparse
import glob

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("files", nargs="*")
arg_parser.add_argument("--s3_subdir", default=None)
arg_parser.add_argument("--bucket", required=True)
arg_parser.add_argument("--aws_access_key", default=None)
arg_parser.add_argument("--aws_secret_key", default=None)
arg_parser.add_argument("--public", action="store_true", default=False)

args = arg_parser.parse_args()

# Get from env vars if they are not in args
if args.aws_access_key is None:
    args.aws_access_key = os.environ["S3_UPLOADR_AWS_ACCESS_KEY"]
if args.aws_secret_key is None:
    args.aws_secret_key = os.environ["S3_UPLOADR_AWS_SECRET_KEY"]

conn = tinys3.Connection(args.aws_access_key,
                         args.aws_secret_key,
                         tls=True)

# parse globs if there are any
files = []
for x in args.files:
    files += glob.glob(x)

# if no files are found (like if globs have no matches)
if len(files) < 1:
    raise SystemError("Files not found.")

# add subdirectory to s3 file "key"
s3_key_format = "{}".format

if args.s3_subdir is not None:
    s3_key_format = (args.s3_subdir + "/{}").format

for fname in files:  # for each filename in files list
    with open(fname, 'rb') as f:
        r = conn.upload(s3_key_format(fname), f, args.bucket, public=args.public)
        if r.status_code != 200:
            raise ConnectionError("{} - {}".format(r.status_code, r.reason))
        print("Uploaded file to: " + r.url)
