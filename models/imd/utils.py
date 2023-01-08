import psycopg2
import logging
import os
import requests
import json
import pk2loc

def conn():
    '''
    It opens connection to tfm database
    parameters:
    returns:
        the connection
    '''
    global connect
    try:

        connect = psycopg2.connect(f"dbname='{os.environ['POSTGRES_DATABASE']}' user='{os.environ['POSTGRES_USER']}' host='{os.environ['POSTGRES_HOST']}' port='{os.environ['POSTGRES_PORT']}' password='{os.environ['POSTGRES_PASSWORD']}'")
        logging.info("Connected to database")
        return connect
    except Exception as e:
        logging.error('Trying to connecto to BD' + str(e))
        return None

def close():
    '''
    It closes connection to tfm database
    parameters:
    returns:
    '''
    global connect
    connect.close()

def query_imdfromdb(sql):
    '''
    It gets imd_total from location
    parameters:
        sql: str
    returns:
        int: imd_total value or 0 if not found
    '''
    global connect
    try:
        cur= connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        ret = rows[0][0]
        return ret
    except Exception as e:
        logging.error(f'cannot get imd from db {e}')	
        return 0

def get_imd_fromdb(lon, lat, carretera, anyo):
    '''
    It gets imd_total from location
    parameters:
        lon: float
        lat: float
        carretera: str
        anyo: int
    returns:
        int: imd_total value or 0 if not found
    '''
    global connect
    try:
        sql= f"""
                select imd_total
                from 
                    imds i 
                where geom is not null
                and nombre = '{carretera}'
                and year = {anyo}
                order by st_distance(ST_SetSRID(ST_Point({lon}, {lat}),4326), geom)
                limit 1
        """
        imd = query_imdfromdb(sql)
        if imd == 0:
            sql= f"""
                select imd_total
                from 
                    imds i 
                where geom is not null
                and year = {anyo}
                order by st_distance(ST_SetSRID(ST_Point({lon}, {lat}),4326), geom)
                limit 1
             """
            imd = query_imdfromdb(sql)
        
        return imd

    except Exception as e:
        logging.error(f'cannot get incidencies {e}')	
        return 0