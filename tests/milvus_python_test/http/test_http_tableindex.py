import pytest
import requests
import logging
import json
import copy
import random
import arrow
from faker import Faker

# ----------------------------------- table -----------------------------------
class TestHTTPTableIndex:
    fa = Faker()

    def get_mode(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'system/mode')
        return res.json()['reply'].upper()

    def make_records(self, value_type='FLOAT', count=1000, length=32, min_value=0, max_value=1000):
        arr = []
        
        for i in range(count):
            vector = []
            for j in range(length):
                if value_type == 'INT':
                    vector.append(random.randint(min_value, max_value))
                else:
                    vector.append(random.uniform(min_value, max_value))
            arr.append(vector)
        return arr

    def drop_table_and_wait(self, table_name, args):
        try:
            base_url = 'http://%s:%s/' % (args['ip'], args['port'])
            requests.delete(base_url + 'tables/' + table_name)
        except Exception as e:
            logging.getLogger().info(e)
        finally:
            time.sleep(2)

    def drop_table(self, table_name, args):
        try:
            base_url = 'http://%s:%s/' % (args['ip'], args['port'])
            requests.delete(base_url + 'tables/' + table_name)
        except Exception as e:
            logging.getLogger().info(e)


    def test_tableindex_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert 16384 == res.json()['nlist']
        assert 'FLAT' == res.json()['index_type']
    
    def test_tableindex_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert 16384 == res.json()['nlist']
        assert 'FLAT' == res.json()['index_type']

    def test_tableindex_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert 16384 == res.json()['nlist']
        assert 'FLAT' == res.json()['index_type']

    def test_tableindex_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'][0:-2])
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 4 == res.json()['code']
        assert "Table %s not found" % req['table_name'][0:-2] == res.json()['message']

    def test_tableindex_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'][0:-2] + '*')
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 'message=Current url has no mapping' in res.text


    def test_tableindex_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'][1:])
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 4 == res.json()['code']
        assert "Table %s not found" % req['table_name'][1:] == res.json()['message']

    def test_tableindex_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % '*' + req['table_name'][1:])
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 'message=Current url has no mapping' in res.text

    
    def test_tableindex_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'] + '/geterror')
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 'message=Current url has no mapping' in res.text

    
    def test_tableindex_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'] + 'dsad/xxzxsa')
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 'message=Current url has no mapping' in res.text
    
    def test_tableindex_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'] + '/L2')
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 'message=Current url has no mapping' in res.text

    def test_tableindex_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'] + '/IP')
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 'message=Current url has no mapping' in res.text

    def test_tableindex_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        xname = 'x' * 500
        res = requests.get(base_url + 'tables/%s/indexes' % xname)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "Invalid table name" in res.json()['message']

    def test_tableindex_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))        
        res = requests.get(base_url + 'tables/%s/indexes' % '')
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 4 == res.json()['code']
        assert "Table indexes not found" == res.json()['message']

    
    def test_tableindex_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))        
        res = requests.get(base_url + 'tables/%s/indexes' % ' ')
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "Invalid table name" in res.json()['message']
    
    def test_tableindex_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))        
        res = requests.get(base_url + 'tables/%s/indexes' % '%20')
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "Invalid table name" in res.json()['message']

    def test_post_tableindex_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('FLOAT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFFLAT', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']

        self.drop_table(req['table_name'], args)


    def test_post_tableindex_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'IVFFLAT', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'FLAT', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']

        req_index = {"index_type":'IVFSQ8', "nlist":2048}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert 200 == res.status_code
        assert req_index == res.json()
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'FLAT', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'FLAT', "nlist":4096}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'FLAT', "nlist":2048}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'FLAT', "nlist":1024}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'FLAT', "nlist":1}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)


    def test_post_tableindex_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'FLAT', "nlist":0}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 22 == res.json()['code']
        assert "Invalid index nlist" in res.json()['message']
        
        req_index = {"index_type":'IVFSQ8', "nlist":1024}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert 200 == res.status_code
        assert req_index == res.json()

        self.drop_table(req['table_name'], args)

    def test_post_tableindex_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'FLAT', "nlist":-1}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 22 == res.json()['code']
        assert "Invalid index nlist" in res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'IVFSQ8', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)

        req_index = {"index_type":'IVFSQ8H', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'RNSG', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    # GPU only
    def test_post_tableindex_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'IVFPQ', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 1 == res.json()['code']
        assert "PQ not support IP in GPU version!" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'IVFFLAT', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']

        req_index = {"index_type":'IVFFLAT', "nlist":4096}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'IVFFLAT', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']

        req_index = {"index_type":'IVFSQ8H', "nlist":4096}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'IVF_FLAT', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'IVF_flat', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'IVF_SQ8', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'ivfsq8', "nlist":512}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'IVFsq8h', "nlist":4096}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'NSG', "nlist":1024}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    # GPU only
    def test_post_tableindex_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        req_index = {"index_type":'IVFPQ', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

# --------------------------------------------------------------------------------------------------------------------------
    def test_post_tableindex_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('FLOAT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'FLAT', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'FLAT', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_27(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'FLAT', "nlist":4096}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_28(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'FLAT', "nlist":2048}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_29(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('FLOAT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'FLAT', "nlist":1024}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_30(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('FLOAT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'FLAT', "nlist":1}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)


    def test_post_tableindex_31(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('FLOAT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'FLAT', "nlist":0}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 22 == res.json()['code']
        assert "Invalid index nlist" in res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_32(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('FLOAT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'FLAT', "nlist":-1}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 22 == res.json()['code']
        assert "Invalid index nlist" in res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_33(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('FLOAT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFSQ8', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_34(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, 20)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFSQ8H', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_35(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('do not do NSG build on CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'RNSG', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_36(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('do not do PQ build on CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFPQ', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 1 == res.json()['code']
        assert "PQ not support IP in GPU version!" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_37(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFFLAT', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']

        req_index = {"index_type":'IVFFLAT', "nlist":4096}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_38(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFFLAT', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']

        req_index = {"index_type":'IVFSQ8H', "nlist":4096}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_39(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVF_FLAT', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_40(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVF_flat', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_42(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVF_SQ8', "nlist":16384}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_43(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'ivfsq8', "nlist":512}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_tableindex_44(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFsq8h', "nlist":4096}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tableindex_45(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'NSG', "nlist":1024}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    # GPU only
    def test_post_tableindex_46(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('FLOAT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFPQ', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    

    def test_post_tableindex_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('INT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IvfPQ', "nlist":2048}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 8 == res.json()['code']
        assert "The index type is invalid." == res.json()['message']
        self.drop_table(req['table_name'], args)


    def test_options_tableindex_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/indexes' % req['table_name'])
        assert 204 == res.status_code

    def test_options_tableindex_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/indexes/' % req['table_name'])
        assert 204 == res.status_code

    def test_options_tableindex_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/indexes///' % req['table_name'])
        assert 204 == res.status_code

    def test_options_tableindex_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/////indexes///' % req['table_name'])
        assert 204 == res.status_code
    
    def test_options_tableindex_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/////%s///indexes///' % req['table_name'])
        assert 204 == res.status_code
    
    def test_options_tableindex_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/indexes?' % req['table_name'])
        assert 204 == res.status_code

    def test_options_tableindex_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/indexes#' % req['table_name'])
        assert 204 == res.status_code

    def test_options_tableindex_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/indexes' % req['table_name'][1:])
        assert 204 == res.status_code
    
    def test_options_tableindex_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/indexes#' % req['table_name'][:-2])
        assert 204 == res.status_code
    
    # --------------------------------------------------------------------------------------------------------------------------
    req_default = {"index_type":"FLAT","nlist":16384}
    
    def test_del_tableindex_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        size = 10000
        dim = req['dimension']
        req_vectors = {"records": self.make_records('FLOAT', size, dim, 0, size * 50)}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFFLAT', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])        
        assert req_index == res.json()

        res = requests.delete(base_url + 'tables/%s/indexes' % req['table_name'])
        assert 204 == res.status_code

        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert self.req_default == res.json()

        self.drop_table(req['table_name'], args)
    
    def test_del_tableindex_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        
        req_index = {"index_type":'IVFFLAT', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])        
        assert req_index == res.json()

        res = requests.delete(base_url + 'tables/%s/indexes' % req['table_name'])
        assert 204 == res.status_code

        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert self.req_default == res.json()

        self.drop_table(req['table_name'], args)
    
    def test_del_tableindex_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])        
        assert self.req_default == res.json()

        res = requests.delete(base_url + 'tables/%s/indexes' % req['table_name'])
        assert 204 == res.status_code

        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert self.req_default == res.json()

        self.drop_table(req['table_name'], args)

    def test_del_tableindex_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])        
        assert self.req_default == res.json()

        res = requests.delete(base_url + 'tables/%s/indexes' % req['table_name'][:-2])
        assert 404 == res.status_code
        assert ('Table %s does not exist.' % req['table_name'][:-2]) in res.json()['message']
        assert 4 == res.json()['code']

        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert self.req_default == res.json()

        self.drop_table(req['table_name'], args)
    
    def test_del_tableindex_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])        
        assert self.req_default == res.json()

        res = requests.delete(base_url + 'tables/%s/indexes' % (req['table_name'] + 'xxxx'))
        assert 404 == res.status_code
        assert ('Table %s does not exist.' % (req['table_name'] + 'xxxx')) in res.json()['message']
        assert 4 == res.json()['code']

        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert self.req_default == res.json()

        self.drop_table(req['table_name'], args)
    
    def test_del_tableindex_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])        
        assert self.req_default == res.json()

        res = requests.delete(base_url + 'tables/%s/indexes?' % req['table_name'])
        assert 204 == res.status_code
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)

        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert self.req_default == res.json()

        self.drop_table(req['table_name'], args)

    def test_del_tableindex_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])        
        assert self.req_default == res.json()

        res = requests.delete(base_url + 'tables/%s/indexes/' % req['table_name'])
        assert 204 == res.status_code
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)

        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert self.req_default == res.json()

        self.drop_table(req['table_name'], args)

    def test_del_tableindex_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes#' % req['table_name'])
        assert self.req_default == res.json()

        res = requests.delete(base_url + 'tables/%s/indexes?' % req['table_name'])
        assert 204 == res.status_code
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)

        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert self.req_default == res.json()

        self.drop_table(req['table_name'], args)

    def test_del_tableindex_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes#' % req['table_name'])
        assert self.req_default == res.json()

        res = requests.delete(base_url + 'tables/%s/indexes/?' % req['table_name'])
        assert 204 == res.status_code
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)

        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert self.req_default == res.json()

        self.drop_table(req['table_name'], args)

    def test_del_tableindex_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        res = requests.get(base_url + 'tables/%s/indexes#' % req['table_name'])
        assert self.req_default == res.json()

        res = requests.delete(base_url + 'tables/%s/indexes/#' % req['table_name'])
        assert 204 == res.status_code
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)

        res = requests.get(base_url + 'tables/%s/indexes' % req['table_name'])
        assert self.req_default == res.json()

        self.drop_table(req['table_name'], args)


# ----------------------------------- index -----------------------------------