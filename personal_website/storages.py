# TODO CAN DELETE THIS FILE IF NOT USING S3 FOR STATIC FILES
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStore(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
