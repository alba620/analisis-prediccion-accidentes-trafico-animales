#!/bin/python

'''
Update table accidentes_animales_final with luna data if parte_dia = 'Noche'
'''
import logging
import utils

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("------------------- Starting process update_moonlight ------------------- ")
    connect = utils.conn()
    date_moonlight = utils.read()
    utils.update_moonlight(date_moonlight)
    utils.close()
    logging.info("------------------- End process------------------- ")     