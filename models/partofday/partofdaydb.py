#!/bin/python

'''
Update table accidentes_no with parte_dia data
'''
import logging
import utils

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("------------------- Starting process part_day ------------------- ")
    connect = utils.conn()
    date_accident = utils.read()
    utils.update_partofday(date_accident)
    utils.close()
    logging.info("------------------- End process------------------- ")     