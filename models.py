import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres",
                                  password="1234",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")

    cursor = connection.cursor()
    # SQL query to create a new table
    create_table_query = '''CREATE TABLE bank_app
          (ID INT PRIMARY KEY     NOT NULL,
          ACCOUNT           INTEGER    NOT NULL,
          DATE         VARCHAR(20),
          TRANSACTION_DETAILS VARCHAR(50),
          VALUE_DATE VARCHAR(20),
          WITHDRAW_AMT DECIMAL(12,2),
          DEPOSIT_AMT DECIMAL(12,2),
          BALANCE_AMT  DECIMAL(12,2)
          ); '''
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")