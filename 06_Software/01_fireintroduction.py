import fire

#### Functions not for the user

def invisible():
    print("THis is not visible on the CLI")


#### Exposed Functions
##

### Decorator for global function list
FIRE_FUNCTIONS={}
def api(fn):
    FIRE_FUNCTIONS[fn.__name__]=fn
    return fn

@api
def hello(name=""):
    print("The given name is %s" %(name))

if __name__=="__main__":
    fire.Fire(FIRE_FUNCTIONS)    
