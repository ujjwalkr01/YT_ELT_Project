from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor

table = "yt_api"

def get_conn_cursor():
    #Get a connection and cursor to the Postgres database using Airflow's PostgresHook.    
    # Returns:
    #     conn: A connection object to the Postgres database.
    #     cursor: A cursor object for executing SQL queries.
    
    # Create a PostgresHook instance
    hook=PostgresHook(postgres_conn_id="postgres_db_yt_elt", database="elt_db")
    
    # Get a connection from the hook
    conn=hook.get_conn()
    
    # Create a cursor with RealDictCursor to get results as dictionaries
    cur=conn.cursor(cursor_factory=RealDictCursor)
    
    return conn,cur

def close_conn_cursor(conn,cur):
    #Close the cursor
    cur.close()
    
    # Close the connection
    conn.close()
    
def create_schema(schema):
    
    conn,cur=get_conn_cursor()
    
    schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema};"
    
    cur.execute(schema_sql)
    
    conn.commit()
    
    close_conn_cursor(conn,cur)
    
def create_table(schema):
    
    conn,cur=get_conn_cursor()
    
    if schema == 'staging':
        table_sql = f"""
                      CREATE TABLE IF NOT EXISTS {schema}.{table}(
                          "Video_ID" varchar(11) primary key not null,
                          "Video_Title" text not null,
                          "Upload_Date"  timestamp not null,
                          "Duration" varchar(20) not null,
                          "Video_Views" int,
                          "Likes_Count" int,
                          "Comments_Count" int                       
                          );
                     """
    else:
         table_sql = f"""
                        CREATE TABLE IF NOT EXISTS {schema}.{table}(
                                   "Video_ID" varchar(11) primary key not null,
                                   "Video_Title" text not null,
                                   "Upload_Date"  timestamp not null,
                                   "Duration" time not null,
                                   "Video_Type" varchar(10) not null,
                                   "Video_Views" int,
                                   "Likes_Count" int,
                                   "Comments_Count" int                          
                                   );
                       """   
    cur.execute(table_sql)
    
    conn.commit()
    
    close_conn_cursor(conn,cur) 
    

def get_video_ids(cur,schema):
    
    cur.execute(f"""SELECT "Video_ID" from {schema}.{table};""")
    ids=cur.fetchall()
    
    #alternate way to store video_IDS in the listvideo_ids= [row["Video_ID"] for row in ids]
    
    video_ids=[]
    
    for row in ids:
        video_ids.append(row["Video_ID"])
        
    return video_ids