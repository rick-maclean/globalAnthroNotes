from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# we want to run the app
#change something
if __name__ == "__main__":
    app.run(debug=True)