# coding: utf-8
"""
Loads datas from the Tenoli's Database

"""
import psycopg2
import pandas as pd
from datetime import datetime, date
import math

# Conexion a base
db='tenoli'
user='tenoli'
pw='7pvDcyXMiD1YyEIT'
host='tenoli.celgsgsshoum.us-east-1.rds.amazonaws.com'
port='5432'
db = f'dbname={db} user={user} password={pw} host={host} port={port}'
conn = psycopg2.connect(db)

def sql_select(name_of_table, columns=['*']):
    """ Returns a pandas frame from the database. """
    columns = ", ".join(columns)
    table = name_of_table
    query = f"SELECT {columns} FROM {table};"
    return pd.read_sql_query(query, conn)

def sql_query(query):
    """ Returns a pandas frame from the database directly from an explicit query. """
    return pd.read_sql_query(query, conn)

# ----------------------------
# STORES DATAFRAME
# ----------------------------
def load_stores_data():
    ''' Returns a clean stores dataframe. '''
    # We load the stores data
    col = ['name', 'code', 'position', 'type', 'center_id', 'created_date']
    df_stores = sql_select('public.stores_store', columns=col)
    # We set the store id column as index
    df_stores = df_stores.set_index('code')
    # We set the position
    df_stores = df_stores[df_stores['position'] != 'None']
    df_stores['lat'] = df_stores['position'].apply(lambda x: float(x.split(",")[0]))
    df_stores['lon'] = df_stores['position'].apply(lambda x: float(x.split(",")[1]))
    df_stores = df_stores.drop(['position'], axis=1)
    # We set the level of the store
    level = {1: 'Candidato', 2: 'Hormiga', 3: 'Quetzal',
             4: 'Oso', 5: 'Aguila', 6: 'Jaguar'}
    df_stores['level'] = df_stores['type'].apply(lambda x: level[x])
    df_stores = df_stores.drop(['type'], axis=1)
    # We load the centers data
    col = ['id', 'name']
    df_centers = sql_select('public.centers_center', columns=col)
    name_centers = df_centers[['id', 'name']].set_index('id')['name']
    name_centers = name_centers.apply(lambda x: x.split('Centro ')[1])
    # We set the name of the centers
    df_stores['center'] = df_stores['center_id'].apply(lambda x: name_centers[x])
    df_stores = df_stores.drop(['center_id'], axis=1)
    # We set the entry date in the Tenoli Club
    df_stores['entry_date'] = df_stores['created_date'].apply(lambda x: x.date())
    df_stores['entry_date'] = pd.to_datetime(df_stores['entry_date'])
    df_stores = df_stores.drop(['created_date'], axis=1)
    return df_stores

if __name__ == '__main__':
    df_stores = load_stores_data()