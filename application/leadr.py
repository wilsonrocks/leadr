from flask import Flask

app = Flask(__name__)

import views

@app.route('/yo/')
def what():
    return "YO"
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5678,debug=True)
