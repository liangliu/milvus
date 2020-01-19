import pytest
import requests
import logging
import json
import copy
import random
import arrow
from faker import Faker
   
   
# ----------------------------------- vectors -----------------------------------
class TestHTTPVector:
    small_size = 10000
    normal_size = 100000
    big_size = 50000000
    
    def get_mode(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'system/mode')
        return res.json()['reply'].upper()

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
    
    def test_post_vectors_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, size * 50)

        req_vectors = {
            "records": arr
        }

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert size == len(res.json()['ids'])
        self.drop_table(req['table_name'], args)

    
    def test_post_vectors_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim - 2, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert 400 == res.status_code
        assert 7 == res.json()['code']
        assert "The vector dimension must be equal to the table dimension." == res.json()['message']
        self.drop_table(req['table_name'], args)

    def test_post_vectors_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim + 2, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert 7 == res.json()['code']
        assert "The vector dimension must be equal to the table dimension." == res.json()['message']
        self.drop_table(req['table_name'], args)


    def test_post_vectors_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('INT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)

    def test_post_vectors_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 64,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('INT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)

    def test_post_vectors_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('INT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)

    def test_post_vectors_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('INT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)
    
    def test_post_vectors_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 512,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('INT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)
    
    def test_post_vectors_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 64,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)

    def test_post_vectors_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)

    def test_post_vectors_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)
    
    def test_post_vectors_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 512,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)

    def test_post_vectors_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 512,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('INT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors/' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)
    
    def test_post_vectors_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 64,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors/' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)
    
    def test_post_vectors_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('INT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors?' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)
    
    def test_post_vectors_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 32,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors?' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)
    
    def test_post_vectors_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('INT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors#' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)
    
    def test_post_vectors_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, size * 50)

        req_vectors = {"records": arr}

        res = requests.post(base_url + 'tables/%s/vectors#' % req['table_name'], json.dumps(req_vectors))
        assert len(res.json()['ids']) == size
        assert 201 == res.status_code
        self.drop_table(req['table_name'], args)

    # =============================================================================================
    def test_put_vectors_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFFLAT', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = arr[random.randint(1, size)]
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": [vec]}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == 1
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) == 0.0
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFFLAT', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        vec.append(arr[random.randint(1, size)])

        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == len(vec)
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert len(res.json()['results'][1]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) == 0.0
        assert float(res.json()['results'][1][0]['distance']) == 0.0
        
        self.drop_table(req['table_name'], args)


    def test_put_vectors_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFFLAT', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = arr[random.randint(1, size)]
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": [vec]}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        logging.getLogger().info(res.status_code)
        logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == 1
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) >= 0.0
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'IP'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFFLAT', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        vec.append(arr[random.randint(1, size)])

        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        logging.getLogger().info(res.status_code)
        logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == len(vec)
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert len(res.json()['results'][1]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) >= 0.0
        assert float(res.json()['results'][1][0]['distance']) >= 0.0
        
        self.drop_table(req['table_name'], args)
    
    def test_put_vectors_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'FLAT', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == 1
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) == 0.0
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'FLAT', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        vec.append(arr[random.randint(1, size)])

        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == len(vec)
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert len(res.json()['results'][1]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) == 0.0
        assert float(res.json()['results'][1][0]['distance']) == 0.0
        
        self.drop_table(req['table_name'], args)
    
    def test_put_vectors_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFSQ8', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == 1
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) >= 0.0
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFSQ8', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        vec.append(arr[random.randint(1, size)])

        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == len(vec)
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert len(res.json()['results'][1]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) >= 0.0
        assert float(res.json()['results'][1][0]['distance']) >= 0.0
        
        self.drop_table(req['table_name'], args)
        
    def test_put_vectors_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFSQ8H', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == 1
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) >= 0.0
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFSQ8H', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        vec.append(arr[random.randint(1, size)])

        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == len(vec)
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert len(res.json()['results'][1]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) >= 0.0
        assert float(res.json()['results'][1][0]['distance']) >= 0.0
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_11(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('do not do NSG build on CPU version')

        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))
        
        req_index = {"index_type":'RNSG', "nlist":8192}       
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        for i in range(10):
            vec = [arr[random.randint(1, size)]]
            req_search = {"topk": 10,
                        "nprobe": 32,
                        "records": vec}
            
            res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
            
            logging.getLogger().info(res.text)
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == 1
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) == 0.0
        
        self.drop_table(req['table_name'], args)

    # BUG: https://github.com/milvus-io/milvus/issues/1036
    def test_put_vectors_12(self, args):
        # if self.get_mode(args) == 'CPU':
        #     pytest.skip('do not do NSG build on CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        # size = self.small_size
        size = 2000
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'RNSG', "nlist":8192}
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))

        vec = [arr[random.randint(1, size)]]
        vec.append(arr[random.randint(1, size)])

        req_search = {"topk": 5, "nprobe": 32, "records": vec}
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        logging.getLogger().info(res.status_code)
        logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == len(vec)
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert len(res.json()['results'][1]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) >= 0.0
        assert float(res.json()['results'][1][0]['distance']) >= 0.0
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_13(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('do not do PQ build on CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFPQ', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == 1
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) >= 0.0
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_14(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('do not do PQ build on CPU version')

        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFPQ', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        vec.append(arr[random.randint(1, size)])

        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 200 == res.status_code
        assert res.json()['num'] == len(vec)
        assert len(res.json()['results'][0]) == req_search["topk"]
        assert len(res.json()['results'][1]) == req_search["topk"]
        assert float(res.json()['results'][0][0]['distance']) >= 0.0
        assert float(res.json()['results'][1][0]['distance']) >= 0.0
        
        self.drop_table(req['table_name'], args)
    
    def test_put_vectors_15(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('do not do PQ build on CPU version')

        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFPQ', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)][0:-1]]
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        # logging.getLogger().info(res.status_code)
        # logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert res.json()['code'] == 7
        assert res.json()['message'] == "The vector dimension must be equal to the table dimension."
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_16(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('do not do PQ build on CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFPQ', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [arr[random.randint(1, size)]]
        vec[0].append(0.7475476094053792)
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        logging.getLogger().info(res.status_code)
        logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert res.json()['code'] == 7
        assert res.json()['message'] == "The vector dimension must be equal to the table dimension."
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFSQ8', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [[]]
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        logging.getLogger().info(res.status_code)
        logging.getLogger().info(res.text)
        assert 400 == res.status_code
        assert res.json()['code'] == 11
        assert res.json()['message'] == "The vector array is empty. Make sure you have entered vector records."
        
        self.drop_table(req['table_name'], args)

    def test_put_vectors_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFSQ8', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        vec = [None]
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        logging.getLogger().info(res.status_code)
        logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        self.drop_table(req['table_name'], args)
    
    def test_put_vectors_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFFLAT', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        arr =[]
        for i in range(req['dimension']):
            arr.append('')
        vec = [arr]
        
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        logging.getLogger().info(res.status_code)
        logging.getLogger().info(res.text)
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        self.drop_table(req['table_name'], args)
    
    def test_put_vectors_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 128,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))

        size = self.small_size
        dim = req['dimension']
        arr = self.make_records('FLOAT', size, dim, 0, 1)
        req_vectors = {"records": arr}
        res = requests.post(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_vectors))

        req_index = {"index_type":'IVFFLAT', "nlist":8192}
        
        res = requests.post(base_url + 'tables/%s/indexes' % req['table_name'], data=json.dumps(req_index))
        

        arr =[]
        for i in range(req['dimension']):
            arr.append(random.randint(1, 100))
        vec = [arr]
        
        req_search = {"topk": 10,
                      "nprobe": 32,
                      "records": vec}
        
        res = requests.put(base_url + 'tables/%s/vectors' % req['table_name'], json.dumps(req_search))
        
        assert 200 == res.status_code
        assert res.json()['num'] == len(vec)
        assert len(res.json()['results'][0]) == req_search["topk"]
        
        self.drop_table(req['table_name'], args)

    # =============================================================================================

    def test_options_vectors_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/vectors' % req['table_name'])
        assert 204 == res.status_code

    def test_options_vectors_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/vectors/' % req['table_name'])
        assert 204 == res.status_code

    def test_options_vectors_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/vectors///' % req['table_name'])
        assert 204 == res.status_code

    def test_options_vectors_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/////vectors///' % req['table_name'])
        assert 204 == res.status_code
    
    def test_options_vectors_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/////%s///vectors///' % req['table_name'])
        assert 204 == res.status_code
    
    def test_options_vectors_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/vectors?' % req['table_name'])
        assert 204 == res.status_code

    def test_options_vectors_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/vectors#' % req['table_name'])
        assert 204 == res.status_code

    def test_options_vectors_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/vectors' % req['table_name'][1:])
        assert 204 == res.status_code
    
    def test_options_vectors_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/vectors#' % req['table_name'][:-2])
        assert 204 == res.status_code
    
    def test_options_vectors_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = { 
            "table_name": self.fa.pystr(),
            "dimension": 256,
            "index_file_size": 10,
            "metric_type": 'L2'
            }
        res = requests.post(base_url + 'tables', json.dumps(req))
        res = requests.options(base_url + 'tables/%s/vector' % req['table_name'])
        # assert 404 == res.status_code
        assert 'Current url has no mapping' in res.text
# ----------------------------------- vectors -----------------------------------
