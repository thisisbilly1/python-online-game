import sqlite3

db = sqlite3.connect('playerdata.db',check_same_thread=False)
dbc= db.cursor()

def sql(sql,args=()):
    global db, dbc
    try:
        if sql=="COMMIT":
            db.commit()
        else:
            res = dbc.execute(sql,args)
            if "SELECT" in sql:
                result=res.fetchall()
                if len(result)==1:
                    return result[0]
                elif len(result)==0:
                    return None
                else:
                    return result
                
            elif "INSERT INTO" in sql:
                db.commit()
    except Exception as e:
        print(e)

result = sql("SELECT * FROM Players")
print(result)

    
