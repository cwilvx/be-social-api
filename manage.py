import os
from app import create_app

app = create_app("{mode}".format(
    mode = os.environ.get('MODE')
))

if __name__ == '__main__':
    app.run()
