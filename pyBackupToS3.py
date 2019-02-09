import boto3
import tarfile
import time
import os
import configparser

# Reading ConfigFile
config = configparser.ConfigParser()
config.read('settings.conf')
baseFileName = str(config['DEFAULT']['baseFileName'])
baseDir = str(config['DEFAULT']['baseDir'])
tempFolder = str(config['DEFAULT']['tempFolder'])
AK = str(config['DEFAULT']['AK'])
Secret = str(config['DEFAULT']['Secret'])
bucket = str(config['DEFAULT']['bucket'])

if not (baseDir.endswith('/')):
    baseDir = baseDir + "/"
if not (tempFolder.endswith('/')):
    tempFolder = tempFolder + "/"


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


timestr = time.strftime("%Y%m%d-%H%M%S")
filename = baseFileName + timestr + ".tgz"

make_tarfile(tempFolder + filename, baseDir)

s3 = boto3.client('s3', aws_access_key_id=AK, aws_secret_access_key=Secret)
s3.upload_file(tempFolder + filename, bucket, filename)