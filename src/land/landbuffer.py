#!/bin/python

'''
Create a forest map layer with a 1 km buffer around Spanish interurban roads
'''
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
    It returns an array with road name
    parameters:
    returns:
        str: name
    '''
    global connect
    try:
        sql= f"""
            select distinct ddcar_carr nom from carreteras c
            where ddcar_carr not in(select distinct roadname from mapa_forestal_carreteras)
            order by ddcar_carr
        """

        cur= connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        ret = []
        if len(rows) > 0:
            for row in rows:
                ret.append(row)
        return ret

    except Exception as e:
        logging.error(f'cannot get incidencies {e}')	
        return None

def update_record(roads):
    '''
    It updates incidence record
    parameters:
        id: int
        imd_total: int
    returns:
        True
    '''
    global connect
    
    for roadname in roads:

        logging.info(f"Processing road {roadname[0]}")

        try:
            sql= f"""
                insert into public.mapa_forestal_carreteras  (id, geom, roadname)
                with carr as
                (
                    select ddcar_carr , geom_4326 , ddcar_codi , ddtram_cod , st_buffer(geom_4326::geography,500) buff -- buffer de 500 metros a cada lado de la carretera
                        , st_transform(  
                        st_envelope(  
                            st_buffer(  
                                geom
                            ,1000
                                )  
                        ),4326   
                    ) as bbox  
                    from carreteras c 
                    where ddcar_carr  = '{roadname[0]}'
                    order by ddcar_carr 
                ), mf_intersectado as 
                (
                select mf.id, mf.geom , carr.bbox, carr.geom_4326, carr.buff
                from mapa_forestal mf , carr
                where st_intersects(mf.geom, carr.bbox)
                )
                select id, st_intersection(ST_MakeValid(geom),buff)::geometry buffinal,'{roadname[0]}'
                from mf_intersectado
                where buff is not null
                and st_astext(st_intersection(ST_MakeValid(geom),buff)) != 'POLYGON EMPTY'
            
            """
            cur= connect.cursor()
            cur.execute(sql)
            connect.commit()
            '''
            rows = cur.fetchall()
            if len(rows) > 0:
                id = rows[0][0]
                geom = rows[0][1]
                sql_insert = f"""
                            INSERT INTO public.mapa_forestal_carreteras
                                    (id, geom, roadname)
                                    VALUES({id}, '{geom}','{roadname[0]}');
                
                """
                curin = connect.cursor()
                curin.execute(sql_insert)
                connect.commit()
            '''
        except Exception as e:
            logging.error(f'cannot update mapa_forestal id = {id} \{e}')	
            connect.rollback()


    return True

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    logging.info("----------------- Starting process ----------------- ")

    connect = ''
    connect = conn()
    roads = read()
    update_record(roads)
    close()
    logging.info("-----------------  End process ----------------- ")    