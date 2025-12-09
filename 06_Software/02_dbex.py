"""
Basic Database Playground

With this thing, we should try to repeat SQL
- Create a table
- Add data
- Modify data
- select data
- delete data
- drop table

If something goes weird, just delete 02_dbex.db...
"""
import fire

from sqlalchemy import create_engine, text


def connect_engine():
    engine = create_engine("sqlite+pysqlite:///users.db", echo=True) # a database engine showing all queries
    return engine

def sql(query):
    engine = connect_engine()
    with engine.connect() as conn:
        result = conn.execute(text(query))
        print("Results:")
        print(result)
        try:
            for r in result:
                print(r)
        except:
            print("No Results")
        conn.commit()
    
if __name__=="__main__":
    fire.Fire()    
