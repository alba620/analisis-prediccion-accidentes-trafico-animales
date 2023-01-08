#!/bin/python

'''
Update table accidentes_animales_final with geom data using provincia, carretera, pk information and corporative GIS REST API service
'''
import psycopg2
import logging
import os
import pk2loc
from models import Incidence


# Update db geom using provincia, carretera, pk information and corporative GIS REST API service
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
    logging.info("Connection to database closed")

def read():
    '''
    It returns array with data to get location
    parameters:
    returns:
        array: Incidence
    '''
    try:
        sql= f"""
                select 
                    id_num, provincia_1f, carretera, km
                from  
                    accidentes_animales_final aaf 
                where 
                    carretera != 'No inventariada'
                    and geom is null
        """

        cur= connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        ret = []
        if len(rows) > 0:
            for row in rows:
                inci = []
                inci.append(row[0])
                inci.append(row[1])
                inci.append(row[2])
                inci.append(row[3])
                ret.append(inci)
        return ret

    except Exception as e:
        logging.error(f'cannot get incidencies {e}')	
        return None

def update_record(inci, lon, lat):
    '''
    It updates incidence records
    parameters:
        inci: Incidence
    returns:
        True
    '''
    global connect

    geom = f"ST_SetSRID(ST_Point({lon}, {lat}),4326)"

    try:
        sql= f"""
            update accidentes_animales_final set geom = {geom}, longitud = {lon}, latitud = {lat} where id_num = {inci[0]}
        """
        cur= connect.cursor()
        cur.execute(sql)
        connect.commit()
    except Exception as e:
        logging.error(f'cannot update incidence \n{sql} \{e}')	
        connect.rollback()
        return False

    return True

def process_incidences(incidences):
    '''
    It processes incidence records
    parameters:
        incidences: Incidence
    returns:
    '''
    for inci in incidences: 
        # get location
        loc = pk2loc.get_xy(inci[1], inci[2], inci[3])
        if loc != None:
            # update record with location
            update_record(inci, loc[0], loc[1])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("----------------- Starting process ----------------- ")
    connect = ''
    conn()
    incidences = read()
    process_incidences(incidences)
    close()
    logging.info("-----------------  End process ----------------- ")    