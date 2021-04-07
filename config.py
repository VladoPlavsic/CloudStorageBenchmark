from dotenv import dotenv_values

config = dotenv_values(".env")

# s3
ACCESS_KEY_ID=config['ACCESS_KEY_ID']
SECRET_ACCESS_KEY=config['SECRET_ACCESS_KEY']
YANDEX_S3_ENDPOINT=config['YANDEX_S3_ENDPOINT']
BUCKET=config['BUCKET']

# dropbox
OAUTHTOKEN=config['OAUTHTOKEN']
