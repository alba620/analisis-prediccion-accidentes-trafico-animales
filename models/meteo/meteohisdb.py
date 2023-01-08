#!/bin/python

'''
Update table accidentes_no with meteo data from tables
'''
import logging
import psycopg2
import os 
import requests
import json 
from models import aemet_data
import utils

def get_aemestation(fecha, lon, lat):
    '''
    Returns aemet station id
    parameters:
        lon: float longitude
        lat: float latitude
    returns:
        aemet_data: 
    '''

    global connect

    try:
        sql = f"""
                SELECT 
                    m.indicativo
                    , ae.geom <-> ST_SetSRID(ST_Point({lon},{lat}),4326) AS dist
                FROM
                aemet_estaciones ae 
                inner join meteohis m on m.indicativo = ae.indicativo
                where fecha = '{fecha}'
                ORDER BY
                dist
                LIMIT 1;
        """
        cur = connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) > 0:
            emaid = rows[0][0]
        else:
            emaid = None
            logging.warning(f"EMAID not found {lon},{lat}")
    except Exception as e:
        logging.error(f'cannot get emaid {e}')
    
    return emaid

def get_aemet_data(fecha, stationid):

    '''
    parameters:
        fecha: str observation date (AAAA-MM-DD)
        stationid: str 
    returns:
        tmax: 
    '''
    
    global connect
    tmax = -9999
    ret = []
    try:
        sql = f"""
                select tmax , tmin, tmedia, sol, precipitacion
            from meteohis m 
            where indicativo = '{stationid}'
            and fecha = '{fecha}'
            and tmax > 0
        """
        cur = connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) > 0:

            ret.append(rows[0][0])
            ret.append(rows[0][1])
            ret.append(rows[0][2])
            ret.append(rows[0][3])
            ret.append(rows[0][4])
        else:
            logging.warning(f"Tmax not found for stationid = {stationid} date = {fecha}")
    except Exception as e:
        logging.error(f"Tmax not found for stationid = {stationid} date = {fecha} {e}")	

    return ret

def update_meteo(id_num, data):
    '''
    Update meteo in incidences table
    parameters:
        incidences: Array
    returns:
    '''
    global connect

    try:
        sql= f"""
            update accidentes_no set tmax = {data[0]}, tmin = {data[1]}, tmed =  {data[2]}, sol = {data[3]}, prec = {data[4]}  where id_num = {id_num}
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
    Process all incidences and update tmax in accidentes_no
    '''

    for incidence in incidences:
        id_num = incidence[0]
        fecha = incidence[1]
        lon = incidence[2]
        lat = incidence[3]
        logging.info(f"Processing id = {id_num}")
        stationid = get_aemestation(fecha[0:10],lon, lat)
        if stationid != None:
            data = get_aemet_data(fecha[0:10], stationid)
            if len(data) > 0:
                update_meteo(id_num, data)



if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("------------------------------ Starting process ------------------------------ ")
    connect = ''
    connect = utils.conn()
    incidences = utils.read()
    process_incidences(incidences)
    utils.close()
    logging.info("------------------------------ End process ------------------------------ ")


    