import pytest
import requests
import logging
import json
import copy
import random
import arrow
from faker import Faker
import time
    
# ----------------------------------- table -----------------------------------
# test table interface of http functions
# ----------------------------------- table -----------------------------------
class TestHTTPTable:
    
    # @classmethod
    # def setup_class(cls):
    #     # cls.base_url = 'http://%s:%s/' % (args['ip'], args['port'])
    #     cls.HOST = 'http://192.168.1.65:19122/'

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
        
    fa = Faker()

    def test_tables(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':10})
        logging.getLogger().info(res.text)
        assert ('tables' in res.json().keys())
        assert ('count' in res.json().keys())
    
    def test_post_tables_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'], args)

    def test_post_tables_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr() + str(random.randint(100, 999)),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": 'L2',
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'], args)

    def test_post_tables_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr() + '_' + str(random.randint(100, 999)),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": 'L2',
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'], args)

    def test_post_tables_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": "y",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'], args)

    def test_post_tables_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": "_" * random.randint(10, 30),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'], args)

    def test_post_tables_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": "_1mMtt t",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert 'Invalid table name: %s. Table name can only contain numbers, letters, and underscores.' % req['table_name'] == res.json()['message']

    def test_post_tables_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": "22",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert 'Invalid table name: %s. The first character of a table name must be an underscore or letter.' % req['table_name'] == res.json()['message']

    def test_post_tables_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": "33" + self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert 'Invalid table name: %s. The first character of a table name must be an underscore or letter.' % req['table_name'] == res.json()['message']

    def test_post_tables_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr() + "1.2",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert ('Invalid table name: %s' % req['table_name'] in res.json()['message'])

    def test_post_tables_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr() + "汉字",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert ('Invalid table name: %s' % req['table_name'] in res.json()['message'])

    def test_post_tables_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr().upper(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        # logging.getLogger().info(req)
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

        lname = req['table_name'].lower()
        req['table_name'] = lname
        # logging.getLogger().info(req)
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'
        self.drop_table(req['table_name'], args)

    def test_post_tables_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

        res = requests.post(base_url + 'tables', json.dumps(req))
        assert res.json()['code'] == 9
        assert res.json()['message'] == 'Table already exists'
        self.drop_table(req['table_name'], args)


    def test_post_tables_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": "table_name",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        self.drop_table_and_wait(req['table_name'], args)

        res = requests.post(base_url + 'tables', json.dumps(req))
        logging.getLogger().info(res.text)
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

        self.drop_table(req['table_name'], args)

    def test_post_tables_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": "dimension",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        self.drop_table_and_wait(req['table_name'], args)

        res = requests.post(base_url + 'tables', json.dumps(req))
        logging.getLogger().info(res.text)
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

        self.drop_table(req['table_name'], args)

    def test_post_tables_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": "index_file_size",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        self.drop_table_and_wait(req['table_name'], args)

        res = requests.post(base_url + 'tables', json.dumps(req))
        logging.getLogger().info(res.text)
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

        self.drop_table(req['table_name'], args)

    def test_post_tables_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": "metric_type",
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        self.drop_table_and_wait(req['table_name'], args)

        res = requests.post(base_url + 'tables', json.dumps(req))
        logging.getLogger().info(res.text)
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

        self.drop_table(req['table_name'], args)

    def test_del_table_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        # logging.getLogger().info(res.text)
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

        res = requests.delete(base_url + 'tables/' + req['table_name'])
        assert 204 == res.status_code

    def test_del_table_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables?table_name=' + req['table_name'])
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert 'Current url has no mapping' in res.text

    def test_del_table_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + req['table_name'].upper())
        logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert "Table %s does not exist" % req['table_name'].upper() in res.json()['message']
        assert 4 == res.json()["code"]
    
    def test_del_table_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + req['table_name'].lower())
        logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert "Table %s does not exist" % req['table_name'].lower() in res.json()['message']
        assert 4 == res.json()["code"]

    def test_del_table_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + req['table_name'][0:-2])
        logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert "Table %s does not exist" % req['table_name'][0:-2] in res.json()['message']
        assert 4 == res.json()["code"]

    def test_del_table_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + req['table_name'][0:-2] + '*')
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert "Invalid table name: %s" % req['table_name'][0:-2] + '*' in res.json()['message']
        assert 9 == res.json()["code"]

    def test_del_table_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + '')
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert "message=Current url has no mapping" in res.text
    
    def test_del_table_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + ' ')
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert "Invalid table name:" in res.json()['message']
        assert 9 == res.json()["code"]


    def test_del_table_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + '%20')
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert "Invalid table name:" in res.json()['message']
        assert 9 == res.json()["code"]

    def test_del_table_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables//' + req['table_name'])
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code

    def test_del_table_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables///////////////' + req['table_name'])
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code

    def test_del_table_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + '/tables/' + req['table_name'])
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code

    def test_del_table_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + '////////tables/' + req['table_name'])
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code

    def test_del_table_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + '///tables///' + req['table_name'])
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code

    def test_del_table_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + '/tables/?' + req['table_name'])
        # logging.getLogger().info(res.text)        
        assert 400 == res.status_code
        assert "Table name should not be empty." == res.json()['message']
        assert 9 == res.json()["code"]
    
    def test_del_table_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + '/tables/#' + req['table_name'])
        logging.getLogger().info(res.text)        
        assert 404 == res.status_code
        assert "message=Current url has no mapping" in res.text
        
    def test_del_table_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + req['table_name'] + '?')
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code

    def test_del_table_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + req['table_name'] + '/')
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code
    
    def test_del_table_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + req['table_name'] + '#')
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code

    def test_del_table_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + req['table_name'] + '/?')
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code

    def test_del_table_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + req['table_name'] + '//')
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code
    
    def test_del_table_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.delete(base_url + 'tables/' + req['table_name'] + '/#')
        # logging.getLogger().info(res.text)
        assert 204 == res.status_code

    def test_del_table_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }

        res = requests.post(base_url + 'tables', json.dumps(req))
        xname = 'x' * 500
        res = requests.delete(base_url + 'tables/' + xname)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert "Invalid table name:" in res.json()['message']
        assert 9 == res.json()["code"]


# ----------------------------------- table -----------------------------------

    def test_tables_table_name(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables/table_name')
        assert res.status_code == 404
        assert 4 == res.json()['code']
        assert "Table table_name not found" == res.json()['message']
    
    def test_tables_dimension(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables/dimension')
        assert res.status_code == 404
        assert 4 == res.json()['code']
        assert "Table dimension not found" == res.json()['message']

    def test_tables_index_file_size(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables/index_file_size')
        assert res.status_code == 404
        assert 4 == res.json()['code']
        assert "Table index_file_size not found" == res.json()['message']

    def test_tables_metric_type(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables/metric_type')
        assert res.status_code == 404
        assert 4 == res.json()['code']
        assert "Table metric_type not found" == res.json()['message']

    def test_post_tables_table_name_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = 0
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text


    
    def test_post_tables_table_name_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = 1
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    
    def test_post_tables_table_name_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = 2147483647
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    
    def test_post_tables_table_name_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = -10
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    
    def test_post_tables_table_name_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = 0.0
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    
    def test_post_tables_table_name_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = ''
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "Table name should not be empty." == res.json()["message"]

    
    def test_post_tables_table_name_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = True
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        

    
    def test_post_tables_table_name_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = '_%20'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "Invalid table name" in res.json()["message"]

    
    def test_post_tables_table_name_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = []
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text


    
    def test_post_tables_table_name_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = [1, 2]
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    
    def test_post_tables_table_name_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = {}
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    
    def test_post_tables_table_name_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = {'k':1}
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    
    def test_post_tables_table_name_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = None
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 33 == res.json()['code']
        assert "Field 'table_name' is missing" in res.json()["message"]

    
    def test_post_tables_table_name_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = ' '
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "Invalid table name" in res.json()["message"]

    
    def test_post_tables_table_name_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = '汉子'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "Invalid table name" in res.json()["message"]
    
    def test_post_tables_table_name_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['table_name'] = '\t'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "Invalid table name" in res.json()["message"]

    def test_post_tables_table_name_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        res = requests.post(base_url + 'tables#', data=json.dumps(req))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()["message"]
        self.drop_table(req['table_name'], args)

    
    def test_post_tables_table_name_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        res = requests.post(base_url + 'tables?', data=json.dumps(req))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()["message"]
        self.drop_table(req['table_name'], args)
    
    
    def test_post_tables_table_name_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        res = requests.post(base_url + 'tables/', data=json.dumps(req))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()["message"]
        self.drop_table(req['table_name'], args)

    def test_post_tables_table_name_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        xname = 'x' * 5000
        original_req = { 
            "table_name": xname,
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        res = requests.post(base_url + 'tables/', data=json.dumps(req))

        assert 400 == res.status_code
        assert 9 == res.json()['code']
        assert "The length of a table name must be less than 255 characters." in res.json()["message"]
        self.drop_table(req['table_name'], args)
    
    def test_post_tables_table_name_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        req = copy.deepcopy(original_req)
        res = requests.post(base_url + 'tables/', data=json.dumps(req))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()["message"]
        self.drop_table(req['table_name'], args)

    def test_post_tables_dimension_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = 0
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 400 == res.status_code
        assert 7 == res.json()['code']
        assert 'Invalid table dimension' in res.json()['message']

    def test_post_tables_dimension_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = 1
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']

    def test_post_tables_dimension_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = 2147483647
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 7 == res.json()['code']
        assert 'Invalid table dimension' in res.json()['message']

    def test_post_tables_dimension_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            } 
        req = copy.deepcopy(original_req)
        req['dimension'] = -10
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 400 == res.status_code
        assert 7 == res.json()['code']
        assert 'Invalid table dimension' in res.json()['message']

    def test_post_tables_dimension_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = 0.0
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    def test_post_tables_dimension_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = -3.1213
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text


    def test_post_tables_dimension_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = ''
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    def test_post_tables_dimension_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = True
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    def test_post_tables_dimension_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = '_%20'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    def test_post_tables_dimension_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = []
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    def test_post_tables_dimension_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = [1, 2]
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    def test_post_tables_dimension_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = {}
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    def test_post_tables_dimension_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = {'k':1}
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    def test_post_tables_dimension_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = None
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 33 == res.json()['code']
        assert "Field 'dimension' is missing" in res.json()["message"]

    def test_post_tables_dimension_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = ' '
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
    def test_post_tables_dimension_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = '汉子'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    def test_post_tables_dimension_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = copy.deepcopy(original_req)
        req['dimension'] = '\t'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    
    
    def test_post_tables_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + 'tables')
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
    
    def test_post_tables_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = None
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text

    def test_post_tables_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = {}
        res = requests.post(base_url + 'tables', json.dumps(req))
        assert 400 == res.status_code
        # logging.getLogger().info(res.text)
        
        assert 33 == res.json()['code']
        assert "Field 'table_name' is missing" == res.json()['message']

    def test_post_tables_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = {'a':1, 'b':2}
        res = requests.post(base_url + 'tables', json.dumps(req))
        # logging.getLogger().info(res.text)
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text

    def test_options_tables_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'tables')
        assert res.status_code == 204

    def test_options_tables_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'tables?a=1')
        assert res.status_code == 204
    
    def test_options_tables_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'tables/aaa')
        # logging.getLogger().info(res.text)
        assert res.status_code == 204

    def test_tables_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables/geterror')
        # logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 4 == res.json()['code']
        assert 'Table geterror not found' == res.json()['message']
    
    def test_tables_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tablesxxx/aaa')
        # logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_tables_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':-1, 'page_size':10})
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' or 'page_size' should equal or bigger than 0" == res.json()['message']

    def test_tables_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':32768, 'page_size':10})
        assert res.status_code == 200
        assert 0 == res.json()['count']
        assert [] == res.json()['tables']
    
    def test_tables_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':32768})
        assert res.status_code == 200
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0
        

    def test_tables_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':9223372036854775807})
        assert res.status_code == 200
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0

    # BUG: https://github.com/milvus-io/milvus/issues/1075
    def test_tables_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        # res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':92233720368547758070000000000000000000000000000})
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':90000000000000000000000})
        logging.getLogger().info(res.text)
        assert res.status_code == 400
        # {"message":"Query param 'page_size' is illegal:stol","code":36}
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0

    def test_tables_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0.0, 'page_size':922})
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal" in res.json()['message']

    def test_tables_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0.1, 'page_size':922})
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal" in res.json()['message']

    def test_tables_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':-5.5423543, 'page_size':922})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal, only integer supported" == res.json()['message']

    # BUG: https://github.com/milvus-io/milvus/issues/1007
    def test_tables_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':r'', 'page_size':922})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal, only integer supported" == res.json()['message']

    
    def test_tables_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':' ', 'page_size':922})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal, only integer supported" == res.json()['message']
    
    
    def test_tables_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':None, 'page_size':922})
        assert res.status_code == 200
        # logging.getLogger().info(res.text)
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0
        
    def test_tables_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':'\t', 'page_size':922})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal" in res.json()['message']

    def test_tables_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':'%20', 'page_size':922})
        logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal" in res.json()['message']

    def test_tables_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':[], 'page_size':922})
        assert res.status_code == 200
        # logging.getLogger().info(res.text)
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0

    def test_tables_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':{}, 'page_size':922})
        assert res.status_code == 200
        # logging.getLogger().info(res.text)
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0

    def test_tables_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':'x' * 1000, 'page_size':922})
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal" in res.json()['message']

    def test_tables_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':True, 'page_size':922})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal" in res.json()['message']
    
    def test_tables_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':-1})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' or 'page_size' should equal or bigger than 0" == res.json()['message']

    def test_tables_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':9223372036854775807, 'page_size':1})
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert 0 == res.json()['count']
        assert [] == res.json()['tables']

    # BUG: https://github.com/milvus-io/milvus/issues/1075
    def test_tables_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':92233720368547758070000000000000000000000000000, 'page_size':1})
        logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'offset' is illegal" in res.json()['message']

    def test_tables_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':0.0})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal, only integer supported" == res.json()["message"]

    def test_tables_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':0.11})
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal, only integer supported" == res.json()["message"]

    def test_tables_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':-5.5423543})
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal, only integer supported" == res.json()["message"]

    def test_tables_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':''})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal" in res.json()['message']

    def test_tables_27(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':' '})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal" in res.json()['message']
    
    
    def test_tables_28(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':None})
        assert res.status_code == 200
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0

    def test_tables_29(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':'\t'})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal" in res.json()['message']

    def test_tables_30(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':'%20'})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal" in res.json()['message']

    def test_tables_31(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':[]})
        assert res.status_code == 200
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0
    

    def test_tables_32(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':[22]})
        assert res.status_code == 200
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0

    def test_tables_33(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':[0,1], 'page_size':[22, 23]})
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0

    def test_tables_34(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':[0], 'page_size':22})
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0


    def test_tables_35(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':0})
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert 'count' in res.json().keys()
        assert [] == res.json()['tables']


    def test_tables_36(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':{}})
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0
    
    def test_tables_37(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':[0, 1], 'page_size':22})
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0

    def test_tables_38(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':'x' * 500})
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal" in res.json()['message']

    def test_tables_39(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':True})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal" in res.json()['message']

    def test_tables_40(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':False})
        # logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal" in res.json()['message']

    def test_tables_41(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':922337203685477582})
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        if res.json()['count'] > 0:
            assert len(res.json()['tables']) > 0
        else:
            assert len(res.json()['tables']) == 0

    # BUG: https://github.com/milvus-io/milvus/issues/1075
    def test_tables_42(self, args):        
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'tables', params={'offset':0, 'page_size':92233720368547758200000000000000000000000000000000000000000000000000000000000000000000})
        assert res.status_code == 400
        assert 36 == res.json()['code']
        assert "Query param 'page_size' is illegal" in res.json()['message']

    def test_put_tables_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "L2"
            }
        req = None
        res = requests.put(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_put_tables_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        original_req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
            }
        req = copy.deepcopy(original_req)

        res = requests.put(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 404 == res.status_code
        assert "Current url has no mapping" in res.text

    def test_put_tables_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = random.randint(10, 1000)
        
        res = requests.put(base_url + 'tables', data=json.dumps(req))
        assert 404 == res.status_code
        assert "Current url has no mapping" in res.text
        

    def test_put_tables_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        
        req.pop('table_name', None)
        res = requests.put(base_url + 'tables', data=json.dumps(req))
        assert 404 == res.status_code
        assert "Current url has no mapping" in res.text
        # logging.getLogger().info(res.text)
        
    
    def test_put_tables_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req.pop('dimension', None)
        res = requests.put(base_url + 'tables', data=json.dumps(req))
        assert 404 == res.status_code
        assert "Current url has no mapping" in res.text

    def test_put_tables_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req.pop('metric_type', None)
        res = requests.put(base_url + 'tables', data=json.dumps(req))
        assert 404 == res.status_code
        assert "Current url has no mapping" in res.text

    
    def test_put_tables_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req.pop('index_file_size', None)
        res = requests.put(base_url + 'tables', data=json.dumps(req))
        assert 404 == res.status_code
        assert "Current url has no mapping" in res.text

    def test_put_tables_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['blah_blah'] = 50
        req['cpu_xxx'] = 'test'
        
        res = requests.put(base_url + 'tables', data=json.dumps(req))
        assert 404 == res.status_code
        assert "Current url has no mapping" in res.text

    def test_post_tables_metric_type_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = 0
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    def test_post_tables_metric_type_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = 1
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = 2147483647
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text
    
    def test_post_tables_metric_type_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = 2147483648
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = -10
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = 9223372036854775807
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = 1.5
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = 0.0
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    def test_post_tables_metric_type_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = ''
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 23 == res.json()['code']
        assert "metric_type is illegal" == res.json()['message']

    
    def test_post_tables_metric_type_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = 'xxxx'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 23 == res.json()['code']
        assert "metric_type is illegal" == res.json()['message']

    
    def test_post_tables_metric_type_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = True
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = '_%20'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 400 == res.status_code
        # logging.getLogger().info(res.text)
        assert 23 == res.json()['code']
        assert "metric_type is illegal" == res.json()['message']

    
    def test_post_tables_metric_type_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = []
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = [1, 2]
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = {}
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = {'k':1}
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = None
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 33 == res.json()['code']
        assert "Field 'metric_type' is missing" == res.json()['message']

    
    def test_post_tables_metric_type_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = -1.08867
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "Internal Server Error" in res.text

    
    def test_post_tables_metric_type_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = ' '
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 400 == res.status_code
        # logging.getLogger().info(res.text)
        assert 23 == res.json()['code']
        assert "metric_type is illegal" == res.json()['message']

    
    def test_post_tables_metric_type_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = '和今年'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 400 == res.status_code
        # logging.getLogger().info(res.text)
        assert 23 == res.json()['code']
        assert "metric_type is illegal" == res.json()['message']

    
    def test_post_tables_metric_type_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['metric_type'] = '\t'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 400 == res.status_code
        # logging.getLogger().info(res.text)
        assert 23 == res.json()['code']
        assert "metric_type is illegal" == res.json()['message']

    
    def test_post_tables_metric_type_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        res = requests.post(base_url + 'tables#', data=json.dumps(req))
        assert 201 == res.status_code
        # logging.getLogger().info(res.text)
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']

    
    def test_post_tables_metric_type_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        res = requests.post(base_url + 'tables?', data=json.dumps(req))
        assert 201 == res.status_code
        # logging.getLogger().info(res.text)
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
    
    def test_post_tables_metric_type_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        res = requests.post(base_url + 'tables/', data=json.dumps(req))
        assert 201 == res.status_code
        # logging.getLogger().info(res.text)
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']

    def test_post_tables_metric_type_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "ip"
        }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 23 == res.json()['code']
        assert "metric_type is illegal" == res.json()['message']

    def test_post_tables_metric_type_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "l1"
        }
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 23 == res.json()['code']
        assert "metric_type is illegal" == res.json()['message']


    def test_post_tables_index_file_size_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = 0
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 5 == res.json()['code']
        assert "Invalid index file size: 0. The index file size must be within the range of 1 ~ 4096." == res.json()['message']

    
    def test_post_tables_index_file_size_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = 1
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']

    
    def test_post_tables_index_file_size_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = 32867
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 400 == res.status_code
        assert 5 == res.json()['code']
        assert "Invalid index file size: " in res.json()['message']

    
    def test_post_tables_index_file_size_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = 1.5
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = -10
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        assert 400 == res.status_code
        assert 5 == res.json()['code']
        assert "Invalid index file size: " in res.json()['message']

    
    def test_post_tables_index_file_size_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = 0.0
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = ''
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text


    
    def test_post_tables_index_file_size_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = 'xxxx'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = True
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = False
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text
    
    def test_post_tables_index_file_size_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = '_%20'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = []
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = [10]
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = [5, 6]
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = {}
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = {'k':1}
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = None
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 33 == res.json()['code']
        assert "Field 'index_file_size' is missing" == res.json()['message']
    
    def test_post_tables_index_file_size_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = -3.2221
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = ' '
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = '大家快乐'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        req['index_file_size'] = '\t'
        res = requests.post(base_url + 'tables', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert "description=Internal Server Error" in res.text

    
    def test_post_tables_index_file_size_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        
        res = requests.post(base_url + 'tables#', data=json.dumps(req))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)

    
    def test_post_tables_index_file_size_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        
        res = requests.post(base_url + 'tables?', data=json.dumps(req))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
    
    def test_post_tables_index_file_size_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 10,
            "index_file_size": 10,
            "metric_type": "IP"
        }
        
        res = requests.post(base_url + 'tables/', data=json.dumps(req))
        assert 201 == res.status_code
        assert 0 == res.json()['code']
        assert "OK" == res.json()['message']
        self.drop_table(req['table_name'], args)
