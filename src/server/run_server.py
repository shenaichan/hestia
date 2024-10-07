from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    print(request.args.get('code'))
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)