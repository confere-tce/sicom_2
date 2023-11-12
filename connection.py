import psycopg2

conn = psycopg2.connect(
    #Local
    dbname="socorrpm",
    user="socorrpm",
    password="SICSADM",
    host="localhost"

    # Uberaba
    # dbname="uberabpm",
    # user="uberabpm",
    # password="SICSADM",
    # host="34.86.191.201"

    #Elephant
    # dbname="jsmcfbqq",
    # user="jsmcfbqq",
    # password="dzYLD0UV56ksursrQrP4fHMi_f1X116e",
    # host="silly.db.elephantsql.com"
)