# -*- coding: utf-8 -*-

import time
import pymongo
import sys
import os
import json
# --------------------------------------------------------------------------------------------------

def main():
    # mongo connect set
    client = pymongo.MongoClient(
        'mongodb://%s:%s@10.120.38.13' % ("root", "root"), 27017)
    db = client.test
    
    
    
if __name__ == "__main__":
    main()