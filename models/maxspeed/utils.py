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
        array: Incidence (id, lon, lat)
    '''
    global connect
    try:
        sql= f"""
                select 
                    id_num, longitud, latitud
                from  
                    accidentes_no aaf 
                where geom is not null
                    and maxspeed is null
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

def update_record(id_num, maxspeed):
    '''
    Update incidence record
    parameters:
        id_num: int
        maxspeed: int
    returns:
        True
    '''
    global connect
    
    try:
        sql= f"""
            update accidentes_no set maxspeed = {maxspeed} where id_num = {id_num}
        """
        cur= connect.cursor()
        cur.execute(sql)
        connect.commit()
    except Exception as e:
        logging.error(f'cannot update incidence \n{sql} \{e}')	
        connect.rollback()
        return None

    return True

def query_maxspeedfromdb(lon, lat):
    '''
    It gets maxspeed_infered from location
    parameters:
        lon: float
        lat: float
    returns:
        int: maxspeed
    '''
    global connect
    try:
        sql= f"""
                with areabbox as
                (
                    select   
                        st_transform(  
                            st_envelope(  
                                st_buffer(  
                                    st_transform(ST_SetSRID(ST_Point({lon}, {lat}),4326) ,25830)
                                ,1000
                                    )  
                            ),4326   
                        ) as bbox  
                ), carreteras_tmp as
                (
                    select maxspeed_infered , geom, bbox
                    from roads_tfm, areabbox
                    where st_intersects(geom, bbox)
                )
                select maxspeed_infered
                from 
                    carreteras_tmp   
                where geom is not null
                and maxspeed_infered is not null
                order by st_distance(ST_SetSRID(ST_Point({lon}, {lat}),4326), geom)
                limit 1
        """
        cur= connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        ret = rows[0][0]
        return ret
    except Exception as e:
        logging.error(f'cannot get maxspeed_infered from db {e}')	
        return 0
