import logging
import os
import uuid
import random

from errors import *
from config import *
import master_bucket as mb
import worker_bucket as wb

from tests.helper_test import loggerfile_path

def _on_worker(folder_path=''):
    zfb_file_name = '.zfb_config'
    return WorkerConfig.is_config_file(os.path.join(folder_path, zfb_file_name))

def TaskBucket(name, folder_path=''):
    if _on_worker(folder_path):
        return wb.TaskBucket(name)
    else:
        return mb.MasterTaskBucket(name)

if __name__ == "__main__":
    def execute_example():
        '''Funkcja zawierajaca testy'''
        def moje_obliczenia1(a, b):
            return a + b
            
        def moje_obliczenia2(a, b):
            return a * b
            
        def moje_obliczenia3():
            return uuid.uuid1()
            
        def return_tuple():
            return (random.randint(1, 10), [random.randint(1, 10)])
            
        buck = TaskBucket(name="Moje obliczenia")
        
        buck.add_task(moje_obliczenia1, 2, *(1, 5))
        buck.add_task(moje_obliczenia2, 3, *(4, 5))
        buck.add_task(moje_obliczenia3, 4)
        buck.add_task(return_tuple, 6)
        
        my_results = buck.execute()
        
        print my_results.get_table_bucket_result()
    
    # https://docs.python.org/2/library/logging.handlers.html#rotatingfilehandler
    with open(loggerfile_path, 'w') as logfile: pass
    logging.basicConfig(filename=loggerfile_path, format='%(levelname)s:%(message)s', level=logging.INFO)
    
    execute_example()
    