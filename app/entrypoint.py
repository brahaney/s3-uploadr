import tinys3
import sys
import argparse
import glob

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("files", nargs="*")
arg_parser.add_argument("--s3_subdir", default=None)
arg_parser.add_argument("--bucket", required=True)
arg_parser.add_argument("--aws_access_key", required=True)
arg_parser.add_argument("--aws_secret_key", required=True)
arg_parser.add_argument("--public", action="store_true", default=False)

args = arg_parser.parse_args()

conn = tinys3.Connection(args.aws_access_key,
                         args.aws_secret_key,
                         tls=True)

files = []
for x in args.files:
    files += glob.glob(x)

if len(files) < 1:
    raise SystemError("Files not found.")

# add subdirectory to s3 file "key"
s3_key_format = "{}".format
print("starting")

if args.s3_subdir is not None:
    s3_key_format = (args.s3_subdir + "/{}").format

for fname in files:  # for each filename in files list
    with open(fname, 'rb') as f:
        r = conn.upload(s3_key_format(fname), f, args.bucket, public=args.public)
        if r.status_code != 200:
            raise ConnectionError("{} - {}".format(r.status_code, r.reason))
        print("Uploaded file to: " + r.url)
