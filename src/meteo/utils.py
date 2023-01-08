import psycopg2
import logging
import os
from models import aemet_data

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

def read():
    '''
    It returns an array with data to get location
    parameters:
    returns:
        array: Incidence
    '''
    global connect
    logging.info("Reading incidences")
    try:
        sql= f"""
            select 
                id_num, concat(fecha_accidente , 'T', hora_accidente, ':00UTC') , st_x(geom), st_y(geom)
            from  
                accidentes_animales_final aaf 
            where 
                carretera != 'No inventariada'
                and geom is not null
                and tmax is null                    
            order by id_num
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

def update_record(station_data: aemet_data,  id_num):
    '''
    It updated each meteo fields of incidence records in accidentes_animales_final table
    parameters:
        station_data: aemet_data
        id_num: int
    returns:
        True
    '''
    global connect

    try:
        sql= f"""
            update accidentes_animales_final set tmed = {station_data.tmed}, prec = {station_data.prec}
            , tmin = {station_data.tmin}, hora_tmin = {station_data.horatmin}, tmax = {station_data.tmax}
            , hora_tmax = {station_data.horatmax}, sol = {station_data.sol}  where id = {id_num}
        
        """
        cur= connect.cursor()
        cur.execute(sql)
        connect.commit()
    except Exception as e:
        logging.error(f'cannot update incidence \n{sql} \{e}')	
        connect.rollback()
        return False

    return True