#!/bin/python

'''
Update table accidentes_no with meteo data from API
'''
import logging
import os 
import requests
import json 
import models
import utils

def get_aemet_data(date, lon, lat):
    '''
    parameters:
        date: str observation date (AAAA-MM-DDTHH:MM:SSUTC)
        lon: float longitude
        lat: float latitude
    returns:
        station_data
    '''
    global connect
    fecha_ini_str = date # str | Fecha Inicial (AAAA-MM-DDTHH:MM:SSUTC) 2022-10-01T00:00:00UTC
    fecha_fin_str = date # str | Fecha Final (AAAA-MM-DDTHH:MM:SSUTC)
    idema = 'idema_example' # str | Indicativo climatológico de la EMA. Puede introducir varios indicativos separados por comas (,)

    # Get EMA id from aemet_estaciones table
    try:
        sql = f"""
                SELECT 
                    indicativo
                    , ae.geom <-> ST_SetSRID(ST_Point({lon},{lat}),4326) AS dist
                FROM
                aemet_estaciones ae 
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
            logging.warn(f"EMAID not found {lon},{lat}")
    except Exception as e:
        logging.error(f'cannot get emaid {e}')	

    if emaid != None:
        url = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini_str}/fechafin/{fecha_fin_str}/estacion/{emaid}"
        station_data = aemet_data(url)
    
    return station_data

def aemet_data(url):
    '''
    params:
        url: str 
    returns:
        array: aemet_data
    '''
    try:
        headers={"api_key":f"{os.environ['AEMET_APIKEY']}", "accept": "application/json"}
        r = requests.get(url,verify=False, headers= headers)
        raw_data = json.loads(r.text)
        if raw_data['estado'] == 200:
            url_datos = raw_data['datos']
            r = requests.get(url_datos,verify=False, headers= headers)
            raw_data = json.loads(r.text)
            aemet_data = models.aemet_data()
            aemet_data.tmed = raw_data['tmed']
            aemet_data.prec = raw_data['prec']
            aemet_data.tmin = raw_data['tmin']
            aemet_data.horatmin = raw_data['horatmin']
            aemet_data.tmax = raw_data['tmax']
            aemet_data.horatmax = raw_data['horatmax']
            aemet_data.sol = raw_data['sol']
            return aemet_data
        else:
            return None
        
    except Exception as e:
        logging.error(f"Cannot get data from url {e}")
        return None

def update_meteo(incidences):
    '''
    It updates meteo fields in incidences table
    parameters:
        incidences: Array
    returns:
    '''

    for inci in incidences:
        station_data = get_aemet_data(inci[1], inci[2], inci[3])
        utils.update_record(station_data, inci[0])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("------------------------------ Starting process ------------------------------ ")
    connect = ''
    connect = utils.conn()
    incidences = utils.read()
    update_meteo(incidences)
    utils.close()
    logging.info("------------------------------ End process ------------------------------ ") 