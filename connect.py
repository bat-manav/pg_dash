import psycopg2
def connect1():
    connection = psycopg2.connect(user="enterprisedb",
                                                                  password="######",
                                                                  host="54.91.***.**",
                                                                  port="5432",
                                                                  database="postgres")
    cursor = connection.cursor()
    return connection,cursor
