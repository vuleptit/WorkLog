from os.path import dirname, abspath, normpath, join

PROJECT_ROOT = dirname(dirname(abspath(__file__)))
SECRET_FILE = normpath(join(PROJECT_ROOT, 'SECRET.key'))
SECRET_KEY = open(SECRET_FILE).read().strip()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class MESSAGE:
    SUCCESFUL = "Successful"
    Exception = "Something went wrong"