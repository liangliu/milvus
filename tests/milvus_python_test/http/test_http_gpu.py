import pytest
import requests
import logging
import pdb
import json
import copy
import random
import arrow
from faker import Faker
   
# ----------------------------------- gpu_resources -----------------------------------
# test gpu resources switch of http functions
# ----------------------------------- gpu_resources -----------------------------------

class TestHTTPGPU:


    def get_mode(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'system/mode')
        return res.json()['reply'].upper()

    def test_put_gpu_resources_1(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = {}
        
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert res.json()['enable'] == True
        assert res.json()['cache_capacity'] == 1
        assert 'search_resources' in res.json().keys()
        assert 'build_index_resources' in res.json().keys()


    def test_put_gpu_resources_2(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        
        req = copy.deepcopy(original_req)
        req.pop('enable', None)
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert res.json()['enable'] == True
        assert res.json()['cache_capacity'] == 1
        assert 'search_resources' in res.json().keys()
        assert 'build_index_resources' in res.json().keys()

    
    def test_put_gpu_resources_3(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req.pop('cache_capacity', None)
        res = requests.get(base_url + 'config/gpu_resources')
        assert res.json()['enable'] == True
        assert res.json()['cache_capacity'] == 1
        assert 'search_resources' in res.json().keys()
        assert 'build_index_resources' in res.json().keys()

    
    def test_put_gpu_resources_4(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req.pop('build_index_resources', None)
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert res.json()['enable'] == True
        assert res.json()['cache_capacity'] == 1
        assert 'search_resources' in res.json().keys()
        assert 'build_index_resources' in res.json().keys()

    
    def test_put_gpu_resources_5(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req.pop('search_resources', None)

        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert res.json()['enable'] == True
        assert res.json()['cache_capacity'] == 1
        assert 'search_resources' in res.json().keys()
        assert 'build_index_resources' in res.json().keys()

    def test_put_gpu_resources_6(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['blah_blah'] = 50
        req['cpu_xxx'] = 'test'
        
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))        
        logging.getLogger().info(res.text)
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert res.json()['enable'] == True
        assert res.json()['cache_capacity'] == 1
        assert 'search_resources' in res.json().keys()
        assert 'build_index_resources' in res.json().keys()

    def test_put_gpu_resources_build_index_resources_1(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = 0
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()
        

    
    def test_put_gpu_resources_build_index_resources_2(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = 1
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_3(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = 2147483647
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_4(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = -10
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_5(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = 1.5
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_6(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = 0.0
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_7(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = ''
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()
    
    def test_put_gpu_resources_build_index_resources_8(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = 'xxxx'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_9(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = '_%20'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_10(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = []
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_11(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = [1, 2]
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_12(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = {}
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_13(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = {'k':1}
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_14(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = None
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_15(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = -3.222
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()        

    
    def test_put_gpu_resources_build_index_resources_16(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = ' '
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()
    
    def test_put_gpu_resources_build_index_resources_17(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = '汉子'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_18(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['build_index_resources'] = '\t'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_19(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources#')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources#', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources#')
        assert False == false_res.json()['enable']

        requests.put(base_url + 'config/gpu_resources#', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources#')
        assert false_res.json() == res.json()
        
    
    def test_put_gpu_resources_build_index_resources_20(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources?')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources?', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources?')
        assert False == false_res.json()['enable']

        requests.put(base_url + 'config/gpu_resources?', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources?')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_21(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources/')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources/', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources/')
        assert False == false_res.json()['enable']

        requests.put(base_url + 'config/gpu_resources/', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources/')
        assert false_res.json() == res.json()

    def test_put_gpu_resources_build_index_resources_22(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        logging.getLogger().info(true_res.json())
        req = copy.deepcopy(original_req)
        req['build_index_resources'] = 0
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        logging.getLogger().info(res.json())
        
    def test_put_gpu_resources_build_index_resources_23(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = 5
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    def test_put_gpu_resources_build_index_resources_24(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = 2147386
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_25(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = -10
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()
    
    def test_put_gpu_resources_build_index_resources_26(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = 5
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_27(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = 0.0
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_28(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ''
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_29(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = 'xxxx'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_30(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = '_%20'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_31(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = []
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu build index resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_32(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = [1, 2]
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()


    def test_put_gpu_resources_build_index_resources_33(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = {}
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_34(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = {'k':1}
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_35(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = None
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_36(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = -3.222
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()   

    
    def test_put_gpu_resources_build_index_resources_37(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ' '
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()
    
    def test_put_gpu_resources_build_index_resources_38(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = '汉子'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_39(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = '\t'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_build_index_resources_40(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources#')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources#', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources#')
        assert True == true_res.json()['enable']
        assert req == true_res.json()

    def test_put_gpu_resources_build_index_resources_41(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources?')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources?', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources?')
        assert True == true_res.json()['enable']
        assert req == true_res.json()
   
    def test_put_gpu_resources_build_index_resources_42(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources/')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources/', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources/')
        assert True == true_res.json()['enable']
        assert req == true_res.json()

    def test_put_gpu_resources_build_index_resources_43(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ['GPU0', 2]
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()

    def test_put_gpu_resources_build_index_resources_44(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ['GPU0', 'gpu0', 'gpu0']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu build index resource.' in res.json()['message']
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        

    def test_put_gpu_resources_build_index_resources_45(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ['gpu1']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
    
    def test_put_gpu_resources_build_index_resources_46(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ['xpx']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()


    def test_put_gpu_resources_build_index_resources_47(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ['gpux']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    def test_put_gpu_resources_build_index_resources_48(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ['gpu100']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    def test_put_gpu_resources_build_index_resources_49(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ['GPUx']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    def test_put_gpu_resources_build_index_resources_50(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ['GPU100']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    def test_put_gpu_resources_build_index_resources_51(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['build_index_resources'] = ['GPU0', 'GPU0']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu build index resource.' in res.json()['message']
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']


    def test_put_gpu_resources_search_resources_1(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = 0
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()
        

    
    def test_put_gpu_resources_search_resources_2(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = 1
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_3(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = 2147483647
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_4(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = -10
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_5(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = 1.5
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_6(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = 0.0
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_7(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = ''
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()
    
    def test_put_gpu_resources_search_resources_8(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = 'xxxx'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_9(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = '_%20'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_10(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = []
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_11(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = [1, 2]
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_12(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = {}
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_13(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = {'k':1}
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_14(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = None
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_15(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = -3.222
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()        

    
    def test_put_gpu_resources_search_resources_16(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = ' '
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()
    
    def test_put_gpu_resources_search_resources_17(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = '汉子'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_18(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources')
        assert False == false_res.json()['enable']

        req['search_resources'] = '\t'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_19(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources#')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources#', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources#')
        assert False == false_res.json()['enable']

        requests.put(base_url + 'config/gpu_resources#', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources#')
        assert false_res.json() == res.json()
        
    
    def test_put_gpu_resources_search_resources_20(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources?')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources?', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources?')
        assert False == false_res.json()['enable']

        requests.put(base_url + 'config/gpu_resources?', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources?')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_21(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources/')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = False
        res = requests.put(base_url + 'config/gpu_resources/', data=json.dumps(req))
        false_res = requests.get(base_url + 'config/gpu_resources/')
        assert False == false_res.json()['enable']

        requests.put(base_url + 'config/gpu_resources/', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources/')
        assert false_res.json() == res.json()

    def test_put_gpu_resources_search_resources_22(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req = copy.deepcopy(original_req)
        req['search_resources'] = 0
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert res.json() == true_res.json()
        
    def test_put_gpu_resources_search_resources_23(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = 5
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    def test_put_gpu_resources_search_resources_24(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = 2147386
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_25(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = -10
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()
    
    def test_put_gpu_resources_search_resources_26(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = 5
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_27(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = 0.0
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_28(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = ''
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_29(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = 'xxxx'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_30(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = '_%20'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_31(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = []
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu search resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_32(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = [1, 2]
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()


    def test_put_gpu_resources_search_resources_33(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = {}
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_34(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = {'k':1}
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_35(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = None
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'OK'

        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_36(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = -3.222
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()   

    
    def test_put_gpu_resources_search_resources_37(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = ' '
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()
    
    def test_put_gpu_resources_search_resources_38(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = '汉子'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_39(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = '\t'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_search_resources_40(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources#')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources#', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources#')
        assert True == true_res.json()['enable']
        assert req == true_res.json()

    def test_put_gpu_resources_search_resources_41(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources?')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources?', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources?')
        assert True == true_res.json()['enable']
        assert req == true_res.json()
   
    def test_put_gpu_resources_search_resources_42(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources/')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources/', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources/')
        assert True == true_res.json()['enable']
        assert req == true_res.json()

    def test_put_gpu_resources_search_resources_43(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = ['GPU0', 2]
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        # logging.getLogger().info(res.text)
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        assert true_res.json() == res.json()

    def test_put_gpu_resources_search_resources_44(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = ['GPU0', 'gpu0', 'gpu0']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu build search resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
        

    def test_put_gpu_resources_search_resources_45(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = ['gpu10']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['search_resources'] != res.json()['search_resources']
    
    def test_put_gpu_resources_search_resources_46(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = ['xpx']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()


    def test_put_gpu_resources_search_resources_47(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = ['gpux']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    def test_put_gpu_resources_search_resources_48(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = ['gpu100']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    def test_put_gpu_resources_search_resources_49(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = ['GPUx']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

    def test_put_gpu_resources_search_resources_50(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        true_res = requests.get(base_url + 'config/gpu_resources')
        assert True == true_res.json()['enable']

        req['search_resources'] = ['GPU100']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid gpu resource' in res.json()['message']
        res = requests.get(base_url + 'config/gpu_resources')
        assert true_res.json() == res.json()

# ----------------------------------- gpu_resources -----------------------------------
