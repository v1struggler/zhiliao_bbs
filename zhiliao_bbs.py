# 在主配置文件中我们不任何视图，将所有的视图都分类到app当中

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello"

if __name__ == '__main__':
    app.run()
