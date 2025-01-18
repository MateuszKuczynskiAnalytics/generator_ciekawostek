from flask import Flask
import redis
import time

app = Flask(__name__)
cache = redis.Redis(host="redis", port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr("hit")
        except redis.exceptions.ConnectionError() as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(1)


@app.route("/")
def hello():
    counter = get_hit_count()
    return f"Hello World! I have been seen {counter} times. \n"
