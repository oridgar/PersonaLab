'''
Created on Jul 13, 2017

@author: idgar
'''
import ConfigParser
import io

def get_config(filename):
    with open(filename) as f:
        config_file = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(config_file))
    return config