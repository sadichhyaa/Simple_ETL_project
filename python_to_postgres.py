import psycopg2
import config
import pandas as pd

data=pd.read_csv('tmdb_genres.csv')
df=pd.DataFrame(data)





hostname=config.hostname
database=config.database
username=config.username
pwd=config.pwd
port_id=config.port_id

conn=None
cur=None

try:
    conn=psycopg2.connect(host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

    cur=conn.cursor()

    create_script='''CREATE TABLE IF NOT EXISTS Genre (
                     id int PRIMARY KEY,
                     name varchar(40) NOT NULL)'''
    cur.execute(create_script)

    for row in df.itertuples():
        insert_script='''INSERT INTO Genre (id,name)
                        VALUES(%s,%s)'''
        insert_value=(row.id,row.name)
        cur.execute(insert_script,insert_value)
   
    conn.commit()




except Exception as error:
    print(error)
finally: 
    if cur is not None:
        cur.close()
    if cur is not None:
        conn.close()
