import tinys3
import sys
import argparse

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("--file", required=True)
arg_parser.add_argument("--name", required=True)
arg_parser.add_argument("--bucket", required=True)
arg_parser.add_argument("--aws_access_key", required=True)
arg_parser.add_argument("--aws_secret_key", required=True)
arg_parser.add_argument("--public", action="store_true", default=False)

args = arg_parser.parse_args()

src_filename = sys.argv[1]
dest_filename = sys.argv[2]

conn = tinys3.Connection(args.aws_access_key,
                         args.aws_secret_key,
                         tls=True)

with open("/data/" + args.file, 'rb') as f:
    r = conn.upload(args.name, f, args.bucket, public=args.public)
    if r.status_code != 200:
        raise ConnectionError("{} - {}".format(r.status_code, r.reason))
    print("Uploaded file to: " + r.url)
