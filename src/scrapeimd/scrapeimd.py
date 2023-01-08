#!/bin/python

'''
Scrapping over IMD data from DGT
'''
import logging 
import utils

def get_imds():
    '''
    It runs scraping over IMD DGT data
    parameters:
    returns:
    '''
    for year, url in utils.dict_url.items():
        raw_data = utils.get_imd_fromurl(url)
        features = raw_data['features']
        utils.insert_features(features, year, True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Starting process")
    get_imds()
    logging.info("End process")    