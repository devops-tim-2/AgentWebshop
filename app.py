from common.config import setup_config

app, db = setup_config('dev')


@app.route('/echo')
def echo():
    return 'If you see this message, it means the Product server is running :)'


if __name__ == '__main__':
    app.run()
