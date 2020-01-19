import pytest
import requests
import logging
import json
import copy
import random
import arrow
from faker import Faker
    
    
# ----------------------------------- partition -----------------------------------
class TestHTTPTablePartition:
    fa = Faker()

    # @classmethod
    # def setup_class(cls):
    #     # cls.base_url = 'http://%s:%s/' % (args['ip'], args['port'])
    #     cls.HOST = 'http://192.168.1.65:19122/'

    def drop_table(self, table_name, args):
        try:
            base_url = 'http://%s:%s/' % (args['ip'], args['port'])
            requests.delete(base_url + 'tables/' + table_name)
        except Exception as e:
            logging.getLogger().info(e)

    
    def test_table_partitions_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert 'partitions' in res.json().keys()
        assert [] == res.json()['partitions']

        self.drop_table(req['table_name'], args)
    
    def test_table_partitions_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        params = {}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        logging.getLogger().info(res.status_code)
        logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert 'partitions' in res.json().keys()
        assert [] == res.json()['partitions']
        self.drop_table(req['table_name'], args)

    def test_table_partitions_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        params = {'offset':0}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert 'partitions' in res.json().keys()
        assert [] == res.json()['partitions']
        self.drop_table(req['table_name'], args)

    def test_table_partitions_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        params = {'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert 'partitions' in res.json().keys()
        assert [] == res.json()['partitions']
        self.drop_table(req['table_name'], args)

    def test_table_partitions_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        
        params = {'page_size':10, 'offset':0}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'][0:-2] + '*', params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 'message=Current url has no mapping' in res.text

    def test_table_partitions_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        params = {'page_size':10, 'offset':0}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'][1:], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 4 == res.json()['code']
        assert "Table %s not exists" % req['table_name'][1:] == res.json()['message']


    def test_table_partitions_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))

        params = {'page_size':10, 'offset':20000}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert [] == res.json()['partitions']

    
    def test_table_partitions_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        params = {'page_size':10, 'offset':32769}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert [] == res.json()['partitions']

    def test_table_partitions_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        params = {'page_size':10, 'offset':5.11}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal, only integer supported" == res.json()['message']

    def test_table_partitions_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        params = {'page_size':10.96, 'offset':5}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal, only integer supported" == res.json()['message']

    def test_table_partitions_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        params = {'page_size':10, 'offset':0.0}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal, only integer supported" == res.json()['message']

    
    def test_table_partitions_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        params = {'page_size':10, 'offset':[]}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        logging.getLogger().info(res.status_code)
        logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert [] == res.json()['partitions']

    def test_table_partitions_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))        
        params = {'page_size':[], 'offset':1}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert [] == res.json()['partitions']

    
    def test_table_partitions_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))        
        params = {'page_size':10, 'offset':None}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert [] == res.json()['partitions']
    
    def test_table_partitions_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        res = requests.post(base_url + 'tables', data=json.dumps(req))        
        params = {'page_size':None, 'offset':1}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert [] == res.json()['partitions']
        
    def test_post_table_partitions_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_table_partitions_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code        
        assert 1 == res.json()['code']
        assert "Duplicate partition is not allowed" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        req_partition['partition_name'] = self.fa.pystr()
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code        
        assert 1 == res.json()['code']
        assert "Duplicate partition is not allowed" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_table_partitions_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        req_partition['partition_tag'] = self.fa.pystr()
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code        
        assert 9 == res.json()['code']
        assert "Partition already exists" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = ''        
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "Invalid partition tag:" in res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = ' '        
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code        
        assert 9 == res.json()['code']
        assert "Invalid partition tag:" in res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = '%20'
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code        
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = '__' + self.fa.pystr()
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code        
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)


    def test_post_table_partitions_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = self.fa.pystr() + '__'
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code        
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)


    def test_post_table_partitions_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = self.fa.pystr() + '__' + 'xxxx'
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code        
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = 0
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 500 == res.status_code        
        assert "Internal Server Error" in res.text
        self.drop_table(req['table_name'], args)


    def test_post_table_partitions_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = 0.0
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 500 == res.status_code        
        assert "Internal Server Error" in res.text
        self.drop_table(req['table_name'], args)
    
    def test_post_table_partitions_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = '0.0'
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code        
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = 'Y'
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code        
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }        
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        req_partition['partition_name'] = req_partition['partition_name'].upper()
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code        
        assert 1 == res.json()['code']
        assert "Duplicate partition is not allowed" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }        
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        req_partition['partition_name'] = req_partition['partition_name'].lower()
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code        
        assert 1 == res.json()['code']
        assert "Duplicate partition is not allowed" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }        
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        req_partition['partition_tag'] = req_partition['partition_tag'].upper()
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code        
        assert 9 == res.json()['code']
        assert "Partition already exists" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }        
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        req_partition['partition_tag'] = req_partition['partition_tag'].lower()
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "Partition already exists" == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        res = requests.post(base_url + 'tables/%s/partitions/' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        res = requests.post(base_url + 'tables/%s/partitions?' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        res = requests.post(base_url + 'tables/%s/partitions#' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_name'] = 'x' * 250
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        logging.getLogger().info(res.text)
        logging.getLogger().info(res.status_code)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_name'] = 'x' * 256
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert 'Invalid partition name' in res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_name'] = 'x' * 259
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert 'Invalid partition name' in res.json()['message']

    def test_post_table_partitions_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = 'x' * 255
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_table_partitions_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = 'x' * 256
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        self.drop_table(req['table_name'], args)
        # assert False
    
    def test_post_table_partitions_27(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = 'x' * 259
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        self.drop_table(req['table_name'], args)
        # assert False


    def test_post_table_partitions_28(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_tag'] = '汉子'
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        self.drop_table(req['table_name'], args)

    # BUG
    def test_post_table_partitions_29(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {
            "partition_name": self.fa.pystr(),
            "partition_tag": self.fa.pystr(),
        }
        req_partition['partition_name'] = '汉子'
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert 'Invalid partition name' in res.json()['message']
        self.drop_table(req['table_name'], args)
        # assert False

    def test_post_table_partitions_30(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        for i in range(10):
            req_partition = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
            res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        
        params = {'offset':0, 'page_size':20}
        res = requests.get(base_url + 'tables/%s/partitions' % req['table_name'], params)
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert 200 == res.status_code
        assert 10 == len(res.json()['partitions'])
        self.drop_table(req['table_name'], args)

# ==============================================================================================================================================
    def test_del_table_partitions_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        
        res = requests.delete(base_url + 'tables/%s/partitions/%s' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code

        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % (req['table_name']), params)
        # logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        assert [] == res.json()['partitions']
        self.drop_table(req['table_name'], args)
    
    def test_del_table_partitions_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        
        res = requests.delete(base_url + 'tables/%s/partitions/%s' % (req['table_name'], req_partition['partition_tag'] + 'xxxx'))
        assert 404 == res.status_code
        assert 4 == res.json()['code']
        assert "Table %s's partition %s not found" % (req['table_name'], req_partition['partition_tag'] + 'xxxx') == res.json()['message']

        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % (req['table_name']), params)
        assert req_partition == res.json()['partitions'][0]
        
        self.drop_table(req['table_name'], args)

    # BUG 1029
    def test_del_table_partitions_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        
        res = requests.delete(base_url + 'tables/%s/partitions/%s' % (req['table_name'] + 'xxxx', req_partition['partition_tag']))
        logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 4 == res.json()['code']
        
        # assert "Table %s's partition %s not found" % (req['table_name'], req_partition['partition_tag'] + 'xxxx') == res.json()['message']

        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % (req['table_name']), params)
        assert req_partition == res.json()['partitions'][0]
        
        self.drop_table(req['table_name'], args)

    def test_del_table_partitions_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        
        res = requests.delete(base_url + 'tables/%s/partitions/%s' % (req['table_name'], ''))
        # logging.getLogger().info(res.status_code)
        assert 404 == res.status_code
        assert 'Current url has no mapping' in res.text
        
        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % (req['table_name']), params)
        assert req_partition == res.json()['partitions'][0]
        
        self.drop_table(req['table_name'], args)
    
    def test_del_table_partitions_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        
        res = requests.delete(base_url + 'tables/%s/partitions/%s' % ('', req_partition['partition_tag']))
        # logging.getLogger().info(res.status_code)
        assert 404 == res.status_code
        assert 'Current url has no mapping' in res.text
        
        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % (req['table_name']), params)
        assert req_partition == res.json()['partitions'][0]
        
        self.drop_table(req['table_name'], args)

    def test_del_table_partitions_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition1 = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition1))
        req_partition2 = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition2))
        
        res = requests.delete(base_url + 'tables/%s/partitions/%s' % (req['table_name'], req_partition1['partition_tag']))
        res = requests.delete(base_url + 'tables/%s/partitions/%s' % (req['table_name'], req_partition2['partition_tag']))
        
        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % (req['table_name']), params)
        assert [] == res.json()['partitions']
        
        self.drop_table(req['table_name'], args)


    def test_del_table_partitions_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        
        res = requests.delete(base_url + 'tables/%s/partitions/%s///' % (req['table_name'], req_partition['partition_tag']))
        
        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % (req['table_name']), params)
        assert [] == res.json()['partitions']
        
        self.drop_table(req['table_name'], args)

    def test_del_table_partitions_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        
        res = requests.delete(base_url + 'tables/%s/partitions/%s?' % (req['table_name'], req_partition['partition_tag']))
        
        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % (req['table_name']), params)
        assert [] == res.json()['partitions']
        
        self.drop_table(req['table_name'], args)

    def test_del_table_partitions_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        
        res = requests.delete(base_url + 'tables/%s/partitions/%s#' % (req['table_name'], req_partition['partition_tag']))
        
        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % (req['table_name']), params)
        assert [] == res.json()['partitions']
        
        self.drop_table(req['table_name'], args)


    def test_del_table_partitions_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        count = 10
        for i in range(count):
            req_partition = {"partition_name": self.fa.pystr(), "partition_tag": self.fa.pystr()}
            res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        
        res = requests.delete(base_url + 'tables/%s/partitions/%s' % (req['table_name'], req_partition['partition_tag']))
        
        params = {'offset':0, 'page_size':10}
        res = requests.get(base_url + 'tables/%s/partitions' % (req['table_name']), params)
        assert (count - 1) == len(res.json()['partitions'])

        p_names = [x['partition_name'] for x in res.json()['partitions']]
        p_tags = [x['partition_tag'] for x in res.json()['partitions']]
        
        assert req_partition['partition_name'] not in p_names
        assert req_partition['partition_tag'] not in p_tags
        
        self.drop_table(req['table_name'], args)

# ==============================================================================================================================================

    def test_options_tablepartition_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/partitions' % req['table_name'])
        assert 204 == res.status_code

    def test_options_tablepartition_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/partitions/' % req['table_name'])
        assert 204 == res.status_code

    def test_options_tablepartition_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/partitions///' % req['table_name'])
        assert 204 == res.status_code

    def test_options_tablepartition_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/////partitions///' % req['table_name'])
        assert 204 == res.status_code
    
    def test_options_tablepartition_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/////%s///partitions///' % req['table_name'])
        assert 204 == res.status_code
    
    def test_options_tablepartition_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/partitions?' % req['table_name'])
        assert 204 == res.status_code

    def test_options_tablepartition_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/partitions#' % req['table_name'])
        assert 204 == res.status_code

    def test_options_tablepartition_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/partitions' % req['table_name'][1:])
        assert 204 == res.status_code
    
    def test_options_tablepartition_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/partitions#' % req['table_name'][:-2])
        assert 204 == res.status_code

    

    def test_options_tablepartition_partition_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partitions/%s' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code
    
    def test_options_tablepartition_partition_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partitions/%s' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code

    def test_options_tablepartition_partition_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        # req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        # res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))
        for i in range(5):
            req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
            res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partitions/%s' % (req['table_name'] + 'xxxxx', req_partition['partition_tag'] + 'xxxxx'))
        assert 204 == res.status_code


    def test_options_tablepartition_partition_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partitions/%s/' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code

    def test_options_tablepartition_partition_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partitions/%s///' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code

    def test_options_tablepartition_partition_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/////partitions/%s////' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code
    
    def test_options_tablepartition_partition_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables///////%s///partitions/////%s' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code
    
    def test_options_tablepartition_partition_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partitions/%s?' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code

    def test_options_tablepartition_partition_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partitions/%s#' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code

    def test_options_tablepartition_partition_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partitions/%s///?' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code
    
    def test_options_tablepartition_partition_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partitions/%s//##/?' % (req['table_name'], req_partition['partition_tag']))
        assert 204 == res.status_code
    
    def test_options_tablepartition_partition_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partition/%s//##/?' % (req['table_name'], req_partition['partition_tag']))
        assert 404 == res.status_code
        assert 'message=Current url has no mapping' in res.text
        # logging.getLogger().info(res.text)
    
    def test_options_tablepartition_partition_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        req_partition = {'partition_name': self.fa.pystr(), 'partition_tag': self.fa.pystr()}
        res = requests.post(base_url + 'tables/%s/partitions' % req['table_name'], json.dumps(req_partition))

        res = requests.options(base_url + 'tables/%s/partitions/%s//##/?' % (req['table_name'], req_partition['partition_tag'] + '^&%'))
        assert 204 == res.status_code

# ----------------------------------- partition -----------------------------------
