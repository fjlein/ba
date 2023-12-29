from pymongo import MongoClient
import argparse
import subprocess
import json
import logging
from ffprobe import FFProbe
import hashlib
from pprint import pprint


def md5(path):
    logging.info('Generating MD5 Checksum')

    def file_as_bytes(file):
        with file:
            return file.read()

    result = hashlib.md5(file_as_bytes(open(path, 'rb'))).hexdigest()

    logging.info("checksum=" + result)


def mediainfo(path):
    logging.info('Running mediainfo')

    result = subprocess.run(['mediainfo', path, "--Output=JSON"],
                            capture_output=True, text=True)

    logging.info("ran " + " ".join(result.args))

    result_json = json.loads(result.stdout)
    logging.info("result=" + str(result_json["media"]["track"]))


def ffprobe(path):
    logging.info('Running ffprobe')
    metadata = FFProbe(path)

    logging.info("Ran ffprobe")

    for stream in metadata.streams:
        logging.info("response=" + str(stream.__dict__))


def mongodb():
    # removed user and password from this call for security reasons
    client = MongoClient(
        "mongodb+srv://#####:#####@cluster0.p7qlqab.mongodb.net/?retryWrites=true&w=majority")

    db = client['sample_mflix']

    collections = db.list_collection_names()
    for collection in collections:
        print(collection)

    movies = db["movies"]

    pprint(movies.find_one())


def main():
    parser = argparse.ArgumentParser(
        description='Handle mediainfo output! :D')

    parser.add_argument('--path', help="Path", nargs="?", type=str,
                        const="/Users/felix/Documents/DavidAndGoliath.avi", default="/Users/felix/Documents/DavidAndGoliath.avi")

    parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        logging.info('Logging Level set to INFO')

    md5(path=args.path)
    mediainfo(path=args.path)
    ffprobe(path=args.path)

    # mongodb()


if __name__ == "__main__":
    main()
