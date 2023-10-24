'''
Created on 27 may. 2020

@author: avespe
''' 
import configparser


class ConfigParser(object):


    def __init__(self):
        config = configparser.ConfigParser()
        config.read('cfg/conf.ini')
        config.sections()
        self.params = config
        