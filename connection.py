import psycopg2
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

conn = psycopg2.connect(
    dbname=config['conection']['dbname'],
    user=config['conection']['user'],
    password=config['conection']['password'],
    host=config['conection']['host']
)