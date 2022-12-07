import psycopg2
def connect1():
    connection = psycopg2.connect(user="enterprisedb",
                                                                  password="edb#123",
                                                                  host="54.91.137.21",
                                                                  port="5432",
                                                                  database="postgres")
    cursor = connection.cursor()
    return connection,cursor
