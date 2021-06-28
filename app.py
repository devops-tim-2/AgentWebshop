from flask import Flask

app = Flask(__name__)


@app.route('/echo')
def echo():
    return 'If you see this message, it means the Agent server is running :)'


if __name__ == '__main__':
    app.run()
