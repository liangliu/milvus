import pytest
from milvus import Milvus
import pdb
import requests
from requests.compat import urljoin
import threading
from multiprocessing import Process
from utils import *
import logging
import json


CONNECT_TIMEOUT = 12
HOST = 'http://192.168.1.57:19121/'


# ----------------------------------- basic -----------------------------------
class TestHTTPBasic:

    def test_server_state(self):
        '''
        target: test http server state
        '''
        res = requests.get(HOST + 'state')
        # logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    def test_errorcode_map(self):
    
        res = requests.get(HOST + 'error_code_map')
        # logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert ('error_map' in res.json().keys())
    
    def test_devices(self):
    
        res = requests.get(HOST + 'devices')
        # logging.getLogger().info(res.json())
        assert ('cpu' in res.json().keys())
        assert ('gpus' in res.json().keys())

    def test_config_advanced(self):
    
        res = requests.get(HOST + 'config/advanced')
        # logging.getLogger().info(res.json())
        assert ('cpu_cache_capacity' in res.json().keys())
        assert ('cache_insert_data' in res.json().keys())
        assert ('use_blas_threshold' in res.json().keys())
        assert ('gpu_search_threshold' in res.json().keys())

    def test_config_advanced_error(self):
    
        res = requests.get(HOST + 'config/geterror')
        logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
        

    def test_options_config_advanced(self):
    
        res = requests.options(HOST + 'config/advanced')
        # logging.getLogger().info(res.json())
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'
    
    #TODO: not finished
    def test_put_config_advanced(self):
        res = requests.get(HOST + 'config/advanced')
        # logging.getLogger().info(res.json())

        payload = json.dumps({'cache_insert_data': False})
        # res = requests.put(HOST + 'config/advanced', data=payload)

        # res = requests.get(HOST + 'config/advanced')
        # logging.getLogger().info(res.json())
        assert False


    def test_gpu_resources(self):
    
        res = requests.get(HOST + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert ('enable' in res.json().keys())
        assert ('cache_capacity' in res.json().keys())
        assert ('search_resources' in res.json().keys())
        assert ('build_index_resources' in res.json().keys())

    def test_options_gpu_resources(self):
    
        res = requests.options(HOST + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'
    
    #TODO: not finished
    def test_put_gpu_resources(self):
        assert False

# ----------------------------------- basic -----------------------------------

    
# ----------------------------------- table -----------------------------------
class TestHTTPTable:
    def drop_table(self, table_name):
        requests.delete(HOST + 'tables/' + table_name)

    def test_clear(self):
        res = requests.get(HOST + 'tables', params={'offset':0, 'page_size':10})
        
        for t in res.json()['tables']:
            # clear all tables in milvus
            pass

    def test_tables(self):
        res = requests.get(HOST + 'tables', params={'offset':0, 'page_size':10})
        assert ('tables' in res.json().keys())
    
    def test_post_tables(self):    
        req = { 
            "table_name": "mytest",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

    def test_post_tables_name_numbers(self):
        req = { 
            "table_name": "mytest22",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'])

    def test_post_tables_name_underscore(self):
        req = { 
            "table_name": "mytest__22",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'])

    def test_post_tables_name_short(self):
        req = { 
            "table_name": "y",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'])

    def test_post_tables_name_underscore_only(self):
        req = { 
            "table_name": "____",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'])

    def test_post_tables_name_space(self):
        req = { 
            "table_name": "_1mMtt t",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert 'Invalid table name: %s. Table name can only contain numbers, letters, and underscores.' % req['table_name'] == res.json()['message']

    def test_post_tables_name_number_only(self):
        req = { 
            "table_name": "22",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert 'Invalid table name: %s. The first character of a table name must be an underscore or letter.' % req['table_name'] == res.json()['message']

    def test_post_tables_name_start_number(self):
        req = { 
            "table_name": "33mytest",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert 'Invalid table name: %s. The first character of a table name must be an underscore or letter.' % req['table_name'] == res.json()['message']

    def test_post_tables_name_float(self):
        req = { 
            "table_name": "mytest1.2",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert ('Invalid table name: %s' % req['table_name'] in res.json()['message'])

    #TODO:
    def test_post_tables_name_very_long(self):
        assert False

    def test_post_tables_name_han(self):
        req = { 
            "table_name": "mytest汉字",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert ('Invalid table name: %s' % req['table_name'] in res.json()['message'])

    def test_post_tables_name_upper(self):
        req = { 
            "table_name": "MYtest",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'])

    #TODO: not finished
    def test_post_tables_same(self):
        req = { 
            "table_name": "mytest",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": MetricType.L2
            }
        res = requests.post(HOST + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert res.json()['message'] == 'Table already exists'

    def test_options_tables(self):
        res = requests.options(HOST + 'tables')        
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    def test_single_table(self):
        table_name = 'mytest'
        res = requests.get(HOST + 'tables/' + table_name)
        assert ('table_name' in res.json().keys())
        assert res.json()['table_name'] == table_name

        assert ('dimension' in res.json().keys())
        assert ('metric_type' in res.json().keys())
        assert ('index' in res.json().keys())
        assert ('nlist' in res.json().keys())

    def test_single_table_not_exists(self):
        table_name = 'non_exist'
        res = requests.get(HOST + 'tables/' + table_name)
        assert res.status_code == 404
        assert ('Table %s not found' % table_name in res.json()['message'])
        assert res.json()['code'] == 4

    #TODO: res not given
    def test_del_single_table(self):
        table_name = 'mytest'
        res = requests.delete(HOST + 'tables/' + table_name)
        # logging.getLogger().info(res.json())
        # logging.getLogger().info(res.text)
        assert res.status_code == 204
        assert False
    
    def test_del_table_not_exist(self):
        table_name = 'non_exist'
        res = requests.delete(HOST + 'tables/' + table_name)
        assert res.status_code == 404
        assert ('Table %s does not exist' % table_name in res.json()['message'])
        assert res.json()['code'] == 4

    def test_del_single_table_upper(self):
        table_name = 'Mytest'
        res = requests.delete(HOST + 'tables/' + table_name)
        assert res.status_code == 404
        assert ('Table %s does not exist' % table_name in res.json()['message'])
        assert res.json()['code'] == 4

    def test_del_single_table_numbers(self):
        table_name = '11'
        res = requests.delete(HOST + 'tables/' + table_name)
        assert res.status_code == 400
        assert res.json()['code'] == 9
        assert 'Invalid table name: %s. The first character of a table name must be an underscore or letter.' % table_name == res.json()['message']

    def test_options_single_table(self):
        table_name = 'mytest'
        res = requests.options(HOST + 'tables/' + table_name)
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

    def test_options_table_not_exist(self):
    
        table_name = 'non_exist'
        res = requests.options(HOST + 'tables/' + table_name)
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

# ----------------------------------- table -----------------------------------

# ----------------------------------- index -----------------------------------
class TestHTTPTableIndex:
    def test_table_index(self):
        table_name = 'mytest'
        res = requests.get(HOST + 'tables/' + table_name + '/indexes')
        # logging.getLogger().info(res.json())
        assert ('index_type' in res.json().keys())
        assert ('nlist' in res.json().keys())
    
    def test_table_not_exist_index(self):
        table_name = 'non_exist'
        res = requests.get(HOST + 'tables/' + table_name + '/indexes')
        # logging.getLogger().info(res.json())
        assert res.json()['code'] == 4
        assert res.json()['message'] == 'Table %s not found' % table_name

    #TODO
    def test_post_table_index(self):
        table_name = 'mytest'
        # res = requests.get(HOST + 'tables/' + table_name + '/indexes')

    #TODO
    def test_post_table_not_exist_index(self):
        table_name = 'non_exist'
    
    #TODO
    def test_post_table_index_again(self):
        table_name = 'mytest'


    def test_options_table_index(self):
        table_name = 'mytest'
        res = requests.options(HOST + 'tables/' + table_name + '/indexes')
        # logging.getLogger().info(res.json())
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    def test_options_table_not_exist_index(self):
        table_name = 'non_exist'
        res = requests.options(HOST + 'tables/' + table_name + '/indexes')
        # logging.getLogger().info(res.json())
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    #TODO
    def test_options_table_incorrect_index(self):
        table_name = '11_table'
        res = requests.options(HOST + 'tables/' + table_name + '/indexes')
        logging.getLogger().info(res.json())
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    #TODO
    def test_del_table_index(self):
        table_name = 'mytest'

    #TODO
    def test_del_table_not_exist_index(self):
        table_name = 'mytest'

    #TODO
    def test_del_table_index_deleted(self):
        table_name = 'mytest'

# ----------------------------------- index -----------------------------------

    
# ----------------------------------- partition -----------------------------------
class TestHTTPTablePartition:
    #TODO
    def test_table_partitions(self):
        table_name = 'mytest'
        res = requests.get(HOST + 'tables/' + table_name + '/partitions')
        logging.getLogger().info(res.json())
        # assert ('index_type' in res.json().keys())
        # assert ('nlist' in res.json().keys())
    
    #TODO
    def test_table_not_exist_partitions(self):
        table_name = 'non_exist'
        res = requests.get(HOST + 'tables/' + table_name + '/partitions')
        logging.getLogger().info(res.json())
        # assert res.json()['code'] == 4
        # assert res.json()['message'] == 'Table non_exist not found'


    #TODO
    def test_post_table_partitions(self):
        table_name = 'mytest'
        # res = requests.get(HOST + 'tables/' + table_name + '/indexes')

    #TODO
    def test_post_table_not_exist_partitions(self):
        table_name = 'non_exist'
    
    #TODO
    def test_post_table_partition_again(self):
        table_name = 'mytest'

    #TODO
    def test_options_table_partitions(self):
        pass

    #TODO
    def test_del_table_partition(self):
        table_name = 'mytest'

    #TODO
    def test_del_table_not_exist_partition(self):
        table_name = 'mytest'

    #TODO
    def test_del_table_partition_deleted(self):
        table_name = 'mytest'



# ----------------------------------- partition -----------------------------------

# ----------------------------------- vectors -----------------------------------
class TestHTTPVector:

    #TODO: search vectors
    def test_table_vectors(self):
        table_name = 'mytest'
        # use PUT function
    
    #TODO: insert vectors
    def test_insert_table_vectors(self):
        table_name = 'mytest'
        # use POST function
    
    def test_options_table_vectors(self):
        table_name = 'mytest'
        res = requests.options(HOST + 'tables/' + table_name + '/vectors')
        # logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'
    
    def test_options_table_non_exist_vectors(self):
        table_name = 'non_exist'
        res = requests.options(HOST + 'tables/' + table_name + '/vectors')
        # logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

# ----------------------------------- vectors -----------------------------------

# ----------------------------------- command -----------------------------------
class TestHTTPCMD:

    #TODO: execute command thru http
    def test_http_cmd(self):
        cmd = 'mode'
        res = requests.options(HOST + 'cmd/' + cmd)
        logging.getLogger().info(res.text)

# ----------------------------------- command -----------------------------------