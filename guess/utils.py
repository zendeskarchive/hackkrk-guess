import os
import base64
import hashlib

import boto
from boto.s3.key import Key

BUCKET_NAME = 'guess'
AWS_URL_TEMPLATE = 'https://guess.s3.amazonaws.com/%s'

def upload_photo(username, photo):
    data = base64.b64decode(photo)
    s3 = boto.connect_s3()
    bucket = s3.get_bucket(BUCKET_NAME)
    key = Key(bucket)
    key.content_type = 'image/jpg'
    key.key = 'photos/%s/%s.jpg' % (username, random_hex())
    key.set_contents_from_string(data)
    key.close()
    key.make_public()
    return AWS_URL_TEMPLATE % key.key

def random_hex(bytes=64):
    return hashlib.md5(os.urandom(bytes)).hexdigest()

class Pager(object):
    def __init__(self, total, page, per_page):
        self.total = total
        self.page = page
        self.per_page = per_page

    @property
    def start(self):
        return ((self.page - 1) * self.per_page)

    @property
    def stop(self):
        return self.page * self.per_page

    @property
    def slice(self):
        return self.start, self.stop

    @property
    def page_count(self):
        import math
        return int(math.ceil(float(self.total) / self.per_page))
