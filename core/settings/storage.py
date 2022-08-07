import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env()

# Boto3
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS
AWS_ACCESS_KEY_ID='AKIAZCYHPGBE6FJD7H5Q'
AWS_SECRET_ACCESS_KEY='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'
AWS_STORAGE_BUCKET_NAME='django-sentiment'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# A path prefix that will be prepended to all uploads
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

# Django Static Files Directory
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
