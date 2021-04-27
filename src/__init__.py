def patch_time():
    return
import gevent.monkey
gevent.monkey.patch_time = patch_time  
from flask import Flask 
import uuid

app = Flask(__name__)
SECRET = uuid.uuid4().hex
app.config['SECRET_KEY'] = SECRET

from src import controller