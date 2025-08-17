from flask import Flask
import redis

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.route('/')
def hello():
    count = r.incr("hits")
    return f"<h1>hi! this is a simple flask app</h1><p>Visited {count} times.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)