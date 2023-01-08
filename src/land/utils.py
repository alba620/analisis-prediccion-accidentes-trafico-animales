import psycopg2
import logging
import os

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
    It returns array with data to get location
    parameters:
    returns:
        array: incidence
    '''
    global connect

    try:
        sql= f"""
                select 
                    id_num, longitud, latitud
                from  
                    accidentes_animales_final aaf 
                where 
                    geom is not null
                    and uso_suelo is null
                order by id
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
                ret.append(inci)
        return ret
    except Exception as e:
        logging.error(f'cannot get incidencies {e}')	
        return None

def get_uso_fromdb(lon, lat):
    '''
    It gets the more extensive uso_suelo from location
    parameters:
        lon: float
        lat: float
    returns:
        str: uso_suelo
    '''
    global connect
    try:
        sql= f"""
                select 	mf.usos_suelo, st_area(mf.geom) areas
                from mapa_forestal mf 
                where st_intersects(st_buffer(ST_SetSRID(ST_Point({lon}, {lat}),4326)::geography,500)::geometry, mf.geom)
                order by areas desc
                limit 1
        """

        cur= connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        ret = []
        if len(rows) > 0:
            ret = rows[0][0]
            return ret
        else:
            return 0

    except Exception as e:
        logging.error(f'cannot get incidencies {e}')	
        return 0

def update_record(id_num, uso):
    '''
    It updates field uso_suelo of each incidence record
    parameters:
        id_num: int
        uso: str
    returns:
        True
    '''
    global connect

    try:
        sql= f"""
            update accidentes_animales_final set uso_suelo = '{uso}'  where id_num = {id_num}
        """
        cur= connect.cursor()
        cur.execute(sql)
        connect.commit()
    except Exception as e:
        logging.error(f'cannot update incidence \n{sql} \{e}')	
        connect.rollback()
        return False

    return True