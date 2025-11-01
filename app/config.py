import os

from bcrypt import gensalt


class Config:
    SECRET_KEY = gensalt().decode('utf8')
