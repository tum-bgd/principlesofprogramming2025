"""
This source code implements a minimal TODO list. 

Each todo is represented with only a 
- string (what to do), 
- a deadline (when)
- a timestamp when done (when_done)

It is implemented in a way such that it directly provides
- a Python ORM through SQLAlchemy if modules need to be implemented
- a command line interface using Fire and Python decorators
- a RESTful microservice based on flask (flask.py)
- and a web application (JavaScript) 
"""
import fire

from datetime import datetime
from dateutil import parser


from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy import String, ForeignKey,create_engine, text, select

from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData

############ Section 0: Configuration
class cfg:
    dbengine = "sqlite+pysqlite:///teamtodo.db"


############ Section 1: Database and Data Model (could be in db.py)
###
class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(primary_key=True)
    todo: Mapped[str] = mapped_column(String(180))
    when: Mapped[Optional[datetime]]
    when_done: Mapped[Optional[datetime]]
    answer: Mapped[Optional[str]] = mapped_column(String(180))
    def __repr__(self) -> str:
        return f"Todo(id={self.id!r}, when={self.when!r},when_done={self.when_done!r}, todo={self.todo!r}, answer={self.answer!r})"

def connect_engine():
    engine = create_engine(cfg.dbengine, echo=True) # a database engine showing all queries
    Base.metadata.create_all(engine) # This uses the DeclarativeBase to find all mapped tablesengine
    return engine

#### Section 2: Exposed Functions
##
### Decorator for global function list
FIRE_FUNCTIONS={}
def api(fn):
    FIRE_FUNCTIONS[fn.__name__]=fn
    return fn


@api
def list():
    print("Listing")
    engine = connect_engine()
    session = Session(engine)
    res = session.execute(select(Todo))
    for r in res:
        print(r)

import datetime

@api
def listcomingweek(number=1):
    current_time = datetime.datetime.now()
    weeks_future = current_time + datetime.timedelta(weeks=number)
    session = Session(connect_engine())
    result = session.query(Todo).filter(Todo.when < weeks_future).all()
    print(result)

@api
def listnotdone():
    session = Session(connect_engine())
    result = session.query(Todo).filter(Todo.when_done == None).all()
    print(result)


@api
def done(id, answer="No Answer"):
    session = Session(connect_engine())
    result = session.query(Todo).filter(Todo.id==id).all()
    assert len(result)==1, "ID does not fit a todo or fits more than one"
    result=result[0]
    result.when_done = datetime.datetime.now()
    result.answer=answer
    session.flush()
    session.commit()
    
    
    
        

@api
def add(todo, when=None):
    if when is not None:
        when = parser.parse(when)
    engine = connect_engine()
    with Session (engine) as session:
        session.add(Todo(todo=todo, when=when))
        session.flush()
        session.commit()




@api
def prune(logfile="pruning.log"):
    # all undone in the past are selected and deleted
    # all done are removed
    with open(logfile, "a") as f:
        current_time = datetime.datetime.now()
        session = Session(connect_engine())
        result = session.query(Todo).filter(Todo.when < current_time).filter(Todo.when_done == None).all()
        for r in result:
            print("UndonePast: %s" % (str(r)), file=f)
            session.delete(r)
        result = session.query(Todo).filter(Todo.when_done != None).all()
        for r in result:
            print("Done: %s" % (str(r)), file=f)
            session.delete(r)
    session.commit()
    
        
        
if __name__=="__main__":
    fire.Fire(FIRE_FUNCTIONS)    
