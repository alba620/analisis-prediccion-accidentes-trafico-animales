#!/bin/python

'''
Update table accidentes_animales_final with maxspeed data
'''
import logging
import utils

def process_incidences(incidences):
    '''
    It processes and updates incidences (records)
    parameters:
        incidences: array
    returns:
    '''

    for inci in incidences: 
        maxspeed = utils.query_maxspeedfromdb(inci[1], inci[2])
        if maxspeed != None:
            logging.info(f"Processing id = {inci[0]}")
            utils.update_record(inci[0], maxspeed)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("----------------- Starting process ----------------- ")
    connect = ''
    connect = utils.conn()
    incidences = utils.read()
    process_incidences(incidences)
    utils.close()
    logging.info("-----------------  End process ----------------- ")    