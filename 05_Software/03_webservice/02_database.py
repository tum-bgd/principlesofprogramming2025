from flask import Flask
import json
#from .teamtodo import get_list (not allowed as we are not in a package)
from database import get_list,web_done

#
#  In order to really do this for complex cases, explore
#    - [bronze] extend what we have,
#    - [silver] either a template engine (part of flask),
#    - [gold] get rid of HTML altogether: instead provide an API
#             directly used from JavaScript. look at gold()
 


app = Flask(__name__)

@app.route("/")
def mainpage():
    print("Someone is asking for the main page");
    data = get_list();
    ### Split todos in todo and done todos
    def render_todo(x):
        return f"<li><b>{x["when"]}:</b>&nbsp;{x["todo"]}<a href=\"/todos/{x["id"]}/done\">Done...</a></li>";
    todos_done = [render_todo(x) for x in data if x["when_done"] is not None]
    todos_open = [render_todo(x) for x in data if x["when_done"] is None]
    todo_section = "<h2>Open</h2>"+ "<p><ul>"+"\n".join(todos_open) + "</ul></p>"+"<h2>Done</h2>"+"<p><ul>"+"\n".join(todos_done) + "</ul></p>"
    

    return f"""
<html><head></head><body>
{todo_section}
</body>
</html>
""";



@app.route("/greet/<name>")
def hello_world(name):
    print("I was called with a name of %s" % (name))
    return f"<p>Hello, World! {name}We can change !</p>"

@app.route("/todos/<id>/done")
def todo_done(id):
    ## todo: mark the record with id as done
    ## then: relocate to /
    web_done(int(id));
    
    return f"<p>I am supposed to mark the TODO {id} as done</p><a href=\"/\">Back...</a>";

@app.route("/gold")
def gold():
    data = get_list();
    return data; # retuning python objects supported by json sends them to browser

@app.route("/page")
def page():
    return open("page.html","r").read();


if __name__=="__main__":
    print(get_list())
    app.run();
