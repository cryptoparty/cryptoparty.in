#!/usr/bin/env python
#notes: http://zetcode.com/db/postgresqlpythontutorial/
import psycopg2
import sys
 
def main():
    conn_string = "host='localhost' dbname='test' user='test' password='test'"

    print ("Connecting to database\n ->%s" % (conn_string))

    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor()
    print ("Connected!\n")

    #cursor.execute('SELECT * from "Parties"')
    #here is some code to help manually trigger confirmation in order to build custom urls: 
    # http://localhost:5001/party/confirm/<token>
    cursor.execute('SELECT confirmation_token from "Parties"')

    rows = cursor.fetchall()

    for row in rows:
        print (row)

    if conn:
        conn.close()

if __name__ == "__main__":
    main()
