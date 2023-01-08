#!/bin/python

'''
Update table accidentes_no with imd data
'''
import logging
import pk2loc
import utils

def read():
    '''
    It returns array with data to get location
    parameters:
    returns:
        array: incidence (id, lon, lat, carretera, anyo)
    '''
    global connect
    try:
        sql= f"""
                select 
                    id_num, longitud, latitud, carretera, anyo
                from  
                    accidentes_no aaf 
                where geom is not null
                    and imd_total is null
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
                inci.append(row[4])
                ret.append(inci)
        return ret

    except Exception as e:
        logging.error(f'cannot get incidencies {e}')	
        return None

def update_record(id_num, imd_total):
    '''
    It updates field of 'imd_total' of each incidence record in accidentes_no table
    parameters:
        id_num: int
        imd_total: int
    returns:
        True
    '''
    global connect
    
    try:
        sql= f"""
            update accidentes_no set imd_total = {imd_total} where id_num = {id_num}
        """
        cur= connect.cursor()
        cur.execute(sql)
        connect.commit()
    except Exception as e:
        logging.error(f'cannot update incidence \n{sql} \{e}')	
        connect.rollback()
        return None

    return True

def process_incidences(incidences):
    '''
    It processes each incidence
    parameters: 
        incidences: array
    returns:
    '''

    for inci in incidences: 
        # get location
        year = inci[4]
        if year == 2020 or year == 2021:
            year = 2019
        imd_total = utils.get_imd_fromdb(inci[1], inci[2], inci[3], year)
        if imd_total != None:
            logging.info(f"Processing id = {inci[0]}")
            # update record with imd
            update_record(inci[0], imd_total)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("----------------- Starting process ----------------- ")
    connect = ''
    connect = utils.conn()
    incidences = read()
    process_incidences(incidences)
    utils.close()
    logging.info("-----------------  End process ----------------- ")    