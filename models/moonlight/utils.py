import psycopg2
import logging
import os
import ephem

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
    It returns array with data to calculate moonlight
    parameters:
    returns:
        array: date_moonlight
    '''
    global connect

    try:
        sql= f"""
                select 
                    id_num, fecha_accidente
                from  
                    accidentes_no
                where 
                    parte_dia = 'Noche'
                    and luna is null                    
                order by id_num
        """

        cur= connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        ret = []
        if len(rows) > 0:
            for row in rows:
                date_moonlight = []
                date_moonlight.append(row[0])
                date_moonlight.append(row[1])
                ret.append(date_moonlight)
        return ret
    except Exception as e:
        logging.error(f'cannot get dates {e}')	
        return None


def update_moonlight(date_moonlight):
    '''
    It updates moonlight record
    parameters:
        date_moonlight: array
    returns:
        True
    '''
    global connect

    for id_num, datemoon in date_moonlight:
        id_num = id_num
        m = ephem.Moon(datemoon)
        moonlight = round(m.moon_phase * 100)
        try:
            sql= f"""
                update accidentes_no set luna = {moonlight}  where id_num = {id_num}
            """
            cur= connect.cursor()
            cur.execute(sql)
            connect.commit()
        except Exception as e:
            logging.error(f'cannot update incidence \n{sql} \{e}')	
            connect.rollback()
            return False

    return True