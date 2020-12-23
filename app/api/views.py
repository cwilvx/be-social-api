from . import api

@api.route('/')
def index():
    return {'message':'success!'}
