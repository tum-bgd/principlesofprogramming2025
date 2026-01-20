from flask import Flask
import json


app = Flask(__name__)

@app.route("/")
def mainpage():
    print("Someone is asking for the main page");
    return """
<html><head></head><body>
<h1>Hello!</h1><p><a href="/greet/martin">Greet martin</a>
</p>
</body>
</html>
""";

@app.route("/greet/<name>")
def hello_world(name):
    print("I was called with a name of %s" % (name))
    return f"<p>Hello, World! {name}We can change !</p>"


@app.route("/data")
def data():
    return "<h1>Hello</h1>";

if __name__=="__main__":
    app.run();
