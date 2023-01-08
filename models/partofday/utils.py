import psycopg2
import logging
import os
from datetime import timedelta, datetime
from astral.geocoder import group, database
from astral import LocationInfo
from astral.sun import sun

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
    It returns array with data to calculate part of day
    parameters:
    returns:
        array: date_accident
    '''
    global connect

    try:
        sql= f"""
                select 
                    id_num, fecha_accidente, hora_accidente, longitud, latitud, nombre_ccaa
                from  
                    accidentes_no
                where 
                    longitud is not null
                    and parte_dia is null
                order by id_num
        """

        cur= connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        ret = []
        if len(rows) > 0:
            for row in rows:
                date_accident = []
                date_accident.append(row[0])
                date_accident.append(row[1])
                date_accident.append(row[2])   
                date_accident.append(row[3])
                date_accident.append(row[4]) 
                date_accident.append(row[5])    
                ret.append(date_accident)
        return ret
    except Exception as e:
        logging.error(f'cannot get dates {e}')	
        return None


def update_partofday(date_accident):
    '''
    It calculates part of day and updates parte_dia field in accidentes_no
    parameters:
        date_accident: array
    returns:
        True
    '''
    global connect

    for id_num, date, hour, lon, lat, nombre_ccaa in date_accident:
        id_num = id_num
        place = LocationInfo()
        place.name = 'somewhere'
        place.region = 'somewhere'
        if nombre_ccaa == 'Canarias':
            place.timezone = 'Europe/Lisbon'
        else:
            place.timezone = 'Europe/Madrid'
        place.latitude = lat
        place.longitude = lon
        s = sun(place.observer, date = date, tzinfo = place.timezone)
        quarter_hour = timedelta(minutes = 15)
        if hour > (s["dawn"] - quarter_hour).time() and hour < (s["sunrise"] + quarter_hour).time():
            parte_dia = 'Amanecer'
        elif hour > (s["sunrise"] + quarter_hour).time() and hour < (s["sunset"] - quarter_hour).time():
            parte_dia = 'Día'
        elif hour > (s["sunset"] - quarter_hour).time() and hour < (s["dusk"] + quarter_hour).time():
            parte_dia = 'Anochecer'
        else:
            parte_dia = 'Noche'

        try:
            sql= f"""
               update accidentes_no set parte_dia = '{parte_dia}' where id_num = {id_num} 
            """
            cur= connect.cursor()
            cur.execute(sql)
            connect.commit()
        except Exception as e:
            logging.error(f'cannot update incidence \n{sql} \{e}')	
            connect.rollback()
            return False

    return True