import json
import os
import logging


import numpy as np

class Process():
    """
    """
    def __init__(self, dir):
        self.dir = dir
        self.update(os.path.join(dir, "params.json"))

    def run(self, overwrite=False):
        """
        """
        return True 
    

    def update(self, json_path):
        """Loads parameters from json file"""
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)
