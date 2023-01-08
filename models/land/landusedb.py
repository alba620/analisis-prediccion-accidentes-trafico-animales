#!/bin/python

'''
Update table accidentes_no with uso_suelo data
'''
import logging
import utils


# Update db uso_suelo from id, lon, lat
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
                     and uso_suelo is null
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

def process_incidences(incidences):
    '''
    It processes and updates uso_suelo in accidentes_no table
    parameters: 
        incidences: array
    returns:
    '''

    for inci in incidences: 
        logging.info(f"Processing id ={inci[0]}")
        uso = utils.get_uso_fromdb( inci[1], inci[2])
        if uso != None:
            # update record with uso
            utils.update_record(inci[0], uso)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("----------------- Starting process ----------------- ")
    connect = ''
    connect = utils.conn()
    incidences = read()
    process_incidences(incidences)
    utils.close()
    logging.info("-----------------  End process ----------------- ")      