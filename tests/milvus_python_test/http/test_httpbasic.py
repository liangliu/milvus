import pytest
import requests
import logging
import json
import copy
import random

# ----------------------------------- basic -----------------------------------
class TestHTTPBasic:

    default_conf = {'cpu_cache_capacity': 4, 'cache_insert_data': False, 'use_blas_threshold': 1100, 'gpu_search_threshold': 1000}

    def get_mode(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'system/mode')
        return res.json()['reply'].upper()

    def test_server_state(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'
    
    def test_server_state_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state/myparams')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_server_state_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state?q=myparams')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    def test_server_state_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state/10')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_state_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state?q=10')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'


    def test_server_state_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '/state')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    
    def test_server_state_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '//state')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'
    
    
    def test_server_state_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '/////state')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    
    def test_server_state_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state/')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    
    def test_server_state_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '/state/')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    
    def test_server_state_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state//')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'
    
    
    def test_server_state_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '//state//')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    
    def test_server_state_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state/////')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    
    def test_server_state_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '/////state/////')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    
    def test_server_state_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state/?')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    def test_server_state_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state%20')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    
    def test_server_state_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state?')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'
    
    
    def test_server_state_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state??')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    
    def test_server_state_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state\/')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    
    def test_server_state_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '\/state')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_state_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state/%20')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    
    def test_server_state_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + r'%20state')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_server_state_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + r'%20/state')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_state_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state#')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    def test_server_state_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state/ ')
        logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_server_state_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        rurl = base_url + 'state#'
        logging.getLogger().info(rurl)
        mm = rurl.replace('.', '%2E')
        res = requests.get(mm)
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    def test_server_state_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state?a=1&b=2')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    def test_server_state_27(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'state?a=1%26b=2')
        assert res.status_code == 200
        assert res.json()['code'] == 0
        assert res.json()['message'] == 'Success'

    def test_server_post_state_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + 'state')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_post_state_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + 'state')
        req = {}
        requests.post(base_url + 'state', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_post_state_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + 'state')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'state', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    
    def test_server_put_state_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + 'state')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_put_state_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + 'state')
        req = {}
        requests.post(base_url + 'state', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_put_state_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + 'state')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'state', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_options_state_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'state')
        assert res.status_code == 204

    def test_server_options_state_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'state?a=1')
        assert res.status_code == 204
    
    def test_server_options_state_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'state/aaa')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    
    def test_server_devices(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    
    def test_server_devices_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices/myparams')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    
    def test_server_devices_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices?q=myparams')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()
        
    def test_server_devices_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices/10')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text


    def test_server_devices_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices?q=10')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()


    def test_server_devices_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '/devices')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    
    def test_server_devices_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '//devices')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()
    
    
    def test_server_devices_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '/////devices')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    
    def test_server_devices_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices/')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    
    def test_server_devices_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '/devices/')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    
    def test_server_devices_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices//')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()
    
    
    def test_server_devices_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '//devices//')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    
    def test_server_devices_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices/////')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()
    
    def test_server_devices_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '/////devices/////')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    
    def test_server_devices_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices/?')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    
    def test_server_devices_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices%20')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    
    def test_server_devices_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices?')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()
    
    
    def test_server_devices_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices??')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    
    def test_server_devices_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices\/')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    
    def test_server_devices_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + '\/devices')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_devices_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices/%20')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    
    def test_server_devices_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + r'%20devices')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_server_devices_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + r'%20/devices')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_devices_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices#')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    def test_server_devices_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices/ ')
        logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_server_devices_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        rurl = base_url + 'devices#'
        logging.getLogger().info(rurl)
        mm = rurl.replace('.', '%2E')
        res = requests.get(mm)
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    def test_server_devices_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices?a=1&b=2')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    def test_server_devices_27(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'devices?a=1%26b=2')
        assert res.status_code == 200
        assert 'cpu' in res.json().keys()
        assert 'gpus' in res.json().keys()

    def test_server_post_devices_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + 'devices')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_post_devices_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + 'devices')
        req = {}
        requests.post(base_url + 'devices', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_post_devices_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + 'devices')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'devices', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    
    def test_server_put_devices_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + 'devices')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_put_devices_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + 'devices')
        req = {}
        requests.post(base_url + 'devices', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_put_devices_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + 'devices')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'devices', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_server_options_devices_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'devices')
        assert res.status_code == 204

    def test_server_options_devices_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'devices?a=1')
        assert res.status_code == 204
    
    def test_server_options_devices_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'devices/aaa')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text


    # ----------------------------------- config_advanced -----------------------------------
    def test_config_advanced(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        logging.getLogger().info(res.json())
        assert ('cpu_cache_capacity' in res.json().keys())
        assert ('cache_insert_data' in res.json().keys())
        assert ('use_blas_threshold' in res.json().keys())
        if self.get_mode(args) == 'GPU':
            assert ('gpu_search_threshold' in res.json().keys())

    def test_config_advanced_cpu_cache_capacity(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced/cpu_cache_capacity')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_config_advanced_cache_insert_data(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced/cache_insert_data')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_config_advanced_use_blas_threshold(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced/use_blas_threshold')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_config_advanced_gpu_search_threshold(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced/gpu_search_threshold')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_put_config_advanced_cpu_cache_capacity_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = 0
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid cpu cache capacity' in res.json()['message']
    
    def test_put_config_advanced_cpu_cache_capacity_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = 1
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert req == res.json()
        res = requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_cpu_cache_capacity_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = 2147483647
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 5 == res.json()['code']
        assert 'exceeds system memory' in res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_cpu_cache_capacity_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = 2147483648
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 5 == res.json()['code']
        assert 'Invalid' in res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = -10
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        
        assert 5 == res.json()['code']
        assert 'Invalid' in res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = 9223372036854775807
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
    
        assert 5 == res.json()['code']
        assert 'Invalid' in res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = 1.5
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = 0.0
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = ''
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = 'xxxx'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = True
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = '_%20'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = []
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = [1, 2]
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = {}
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = {'k':1}
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = None
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 400 == res.status_code
        assert 33 == res.json()['code']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = -3.2222
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = ' '
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'ERROR_INVALID_INTEGER' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = '汉子'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'ERROR_INVALID_INTEGER' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = '\t'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'ERROR_INVALID_INTEGER' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced#')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cpu_cache_capacity_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced?')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
    
    
    def test_put_config_advanced_cpu_cache_capacity_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced/')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    def test_put_config_advanced_cache_insert_data_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = 0
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = 1
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_cache_insert_data_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = 2147483647
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_cache_insert_data_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = 2147483648
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_cache_insert_data_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = -10
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_cache_insert_data_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = 9223372036854775807
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_cache_insert_data_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = 1.5
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_cache_insert_data_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = 0.0
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_cache_insert_data_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = ''
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = 'xxxx'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        logging.getLogger().info(original_req)
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = True
        logging.getLogger().info(req)
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.json())
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_cache_insert_data_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = '_%20'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = []
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = [1, 2]
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = {}
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = {'k':1}
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = None
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 400 == res.status_code
        assert 33 == res.json()['code']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = -3.2222
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = ' '
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = '汉子'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = '\t'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced#')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_cache_insert_data_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced?')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
    
    
    def test_put_config_advanced_cache_insert_data_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced/')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    def test_post_config_advanced_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + 'config/advanced')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_post_config_advanced_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = None
        res = requests.post(base_url + 'config/advanced', json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_post_config_advanced_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = {}
        res = requests.post(base_url + 'config/advanced', json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_post_config_advanced_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = {'a':1, 'b':2}
        res = requests.post(base_url + 'config/advanced', json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_options_config_advanced_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'config/advanced')
        assert res.status_code == 204

    def test_options_config_advanced_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'config/advanced?a=1')
        assert res.status_code == 204
    
    def test_options_config_advanced_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'config/advanced/aaa')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_config_advanced_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/geterror')
        logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_config_advanced_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'configxxx/advanced')
        logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_put_config_advanced_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = None
        
        requests.put(base_url + 'config/advanced', data=json.dumps(req))
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    def test_put_config_advanced_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        requests.put(base_url + 'config/advanced', data=json.dumps(req))
        res = requests.get(base_url + 'config/advanced')
        assert req == res.json()
        assert original_req == res.json()

    def test_put_config_advanced_3(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = random.randint(10, 1000)
        
        requests.put(base_url + 'config/advanced', data=json.dumps(req))
        res = requests.get(base_url + 'config/advanced')
        assert req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))


    def test_put_config_advanced_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = random.randint(10, 1000)
        
        requests.put(base_url + 'config/advanced', data=json.dumps(req))
        res = requests.get(base_url + 'config/advanced')
        assert req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    def test_put_config_advanced_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cpu_cache_capacity'] = random.randint(300, 1000)
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert res.status_code == 400
        assert 5 == res.json()['code']
        assert 'Invalid cpu cache capacity' in res.json()['message']

        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    def test_put_config_advanced_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['cache_insert_data'] = random.randint(10, 1000)
        
        logging.getLogger().info(req)
        requests.put(base_url + 'config/advanced', data=json.dumps(req))
        res = requests.get(base_url + 'config/advanced')
        logging.getLogger().info(res.json())
        assert original_req == res.json()
        requests.put(base_url + 'config/advanced', data=json.dumps(original_req))
    
    def test_put_config_advanced_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = {}
        
        requests.put(base_url + 'config/advanced', data=json.dumps(req))
        res = requests.get(base_url + 'config/advanced')
        assert self.default_conf == res.json()


    def test_put_config_advanced_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        
        req = copy.deepcopy(original_req)
        req.pop('cpu_cache_capacity', None)
        requests.put(base_url + 'config/advanced', data=json.dumps(req))
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    def test_put_config_advanced_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req.pop('cache_insert_data', None)
        requests.put(base_url + 'config/advanced', data=json.dumps(req))
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    def test_put_config_advanced_10(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req.pop('gpu_search_threshold', None)
        requests.put(base_url + 'config/advanced', data=json.dumps(req))
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    def test_put_config_advanced_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req.pop('use_blas_threshold', None)

        requests.put(base_url + 'config/advanced', data=json.dumps(req))
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    def test_put_config_advanced_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['blah_blah'] = 50
        req['cpu_xxx'] = 'test'
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))        
        assert res.status_code == 500
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    # BUG: https://github.com/milvus-io/milvus/issues/987
    def test_put_config_advanced_gpu_search_threshold_1(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = 0
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
    
    def test_put_config_advanced_gpu_search_threshold_2(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = 1
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert req == res.json()
        res = requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_gpu_search_threshold_3(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = 2147483647
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert req == res.json()
        res = requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    # BUG: https://github.com/milvus-io/milvus/issues/953
    # should be a different bug
    def test_put_config_advanced_gpu_search_threshold_4(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = 2147483648
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        assert 5 == res.json()['code']
        assert 'Invalid' in res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    # BUG: https://github.com/milvus-io/milvus/issues/953
    def test_put_config_advanced_gpu_search_threshold_5(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = -10
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        assert 5 == res.json()['code']
        assert 'Invalid' in res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    # BUG: https://github.com/milvus-io/milvus/issues/953
    # should be a different bug
    def test_put_config_advanced_gpu_search_threshold_6(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = 9223372036854775807
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
    
        assert 5 == res.json()['code']
        assert 'Invalid' in res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_7(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = 1.5
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_8(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = 0.0
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_9(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = ''
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_10(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = 'xxxx'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_11(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = True
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_12(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = '_%20'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_13(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = []
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_14(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = [1, 2]
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_15(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = {}
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_16(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = {'k':1}
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_17(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = None
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 400 == res.status_code
        assert 33 == res.json()['code']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_18(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = -3.2222
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_19(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = ' '
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'ERROR_INVALID_INTEGER' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_20(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = '汉子'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'ERROR_INVALID_INTEGER' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_21(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['gpu_search_threshold'] = '\t'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'ERROR_INVALID_INTEGER' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_22(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced#')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_gpu_search_threshold_23(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced?')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
    
    
    def test_put_config_advanced_gpu_search_threshold_24(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced/')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    def test_put_config_advanced_use_blas_threshold_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = 0
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']

    
    def test_put_config_advanced_use_blas_threshold_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = 1
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert req == res.json()
        res = requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_use_blas_threshold_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = 2147483647
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert req == res.json()
        res = requests.put(base_url + 'config/advanced', data=json.dumps(original_req))

    
    def test_put_config_advanced_use_blas_threshold_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = 2147483648
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 5 == res.json()['code']
        assert 'Invalid' in res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = -10
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        
        assert 5 == res.json()['code']
        assert 'Invalid' in res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = 9223372036854775807
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
    
        assert 5 == res.json()['code']
        assert 'Invalid' in res.json()['message']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = 1.5
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = 0.0
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = ''
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = 'xxxx'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = True
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = '_%20'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = []
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = [1, 2]
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = {}
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = {'k':1}
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = None
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 400 == res.status_code
        assert 33 == res.json()['code']
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = -3.2222
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = ' '
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'ERROR_INVALID_INTEGER' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = '汉子'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'ERROR_INVALID_INTEGER' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['use_blas_threshold'] = '\t'
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'ERROR_INVALID_INTEGER' in res.text
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced#')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    
    def test_put_config_advanced_use_blas_threshold_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced?')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()
    
    
    def test_put_config_advanced_use_blas_threshold_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/advanced/')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/advanced', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/advanced')
        assert original_req == res.json()

    # ----------------------------------- config_advanced -----------------------------------

    # ----------------------------------- gpu_resources -----------------------------------
    def test_gpu_resources(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        logging.getLogger().info(res.json())
        assert ('enable' in res.json().keys())
        assert ('cache_capacity' in res.json().keys())
        assert ('search_resources' in res.json().keys())
        assert ('build_index_resources' in res.json().keys())

    def test_gpu_resources_enable(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources/enable')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_gpu_resources_cache_capacity(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources/cache_capacity')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_gpu_resources_search_resources(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources/search_resources')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_gpu_resources_build_index_resources(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources/build_index_resources')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_put_gpu_resources_enable_1(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = 0
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(original_req))

    
    def test_put_gpu_resources_enable_2(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = 1
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(original_req))

    
    def test_put_gpu_resources_enable_3(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = 2147483647
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(original_req))

    
    def test_put_gpu_resources_enable_4(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = 2147483648
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(original_req))

    
    def test_put_gpu_resources_enable_5(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = -10
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(original_req))

    
    def test_put_gpu_resources_enable_6(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = 9223372036854775807
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(original_req))

    
    def test_put_gpu_resources_enable_7(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = 1.5
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(original_req))
    
    def test_put_gpu_resources_enable_8(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = 0.0
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(original_req))

    
    def test_put_gpu_resources_enable_9(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = ''
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_10(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = 'xxxx'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()
    
    def test_put_gpu_resources_enable_25(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        
        req = copy.deepcopy(original_req)
        req['enable'] = False          
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 200 == res.status_code
        assert 0 == res.json()['code']
        assert 'Set Gpu resources to false' == res.json()['message']
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert False == res.json()['enable']
        assert 'cache_capacity' in res.json().keys()
        assert res.json()['search_resources'] is None
        assert res.json()['build_index_resources'] is None
        
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(original_req))

    def test_put_gpu_resources_enable_11(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        
        req = copy.deepcopy(original_req)
        req['enable'] = True
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 200 == res.status_code
        assert 0 == res.json()['code']
        assert 'OK' == res.json()['message']
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert True == res.json()['enable']
        assert 'cache_capacity' in res.json().keys()
        assert isinstance(res.json()['search_resources'], list)
        assert isinstance(res.json()['build_index_resources'], list)
        
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(original_req))
    
    def test_put_gpu_resources_enable_12(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = '_%20'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_13(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = []
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_14(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = [1, 2]
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_15(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = {}
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_16(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = {'k':1}
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_17(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = None
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 400 == res.status_code
        assert 33 == res.json()['code']
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_18(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = -3.2222
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_19(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = ' '
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_20(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = '汉子'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_21(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        req['enable'] = '\t'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert 500 == res.status_code
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    def test_put_gpu_resources_enable_22(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources#')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_enable_23(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources?')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()
    
    
    def test_put_gpu_resources_enable_24(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources/')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        logging.getLogger().info(res.text)
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

    
    def test_put_gpu_resources_cache_capacity_1(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # logging.getLogger().info(res.json())
        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 0
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()
        

    
    def test_put_gpu_resources_cache_capacity_2(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # logging.getLogger().info(res.json())
        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 1
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_3(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # logging.getLogger().info(res.json())
        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 2147483647
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_4(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = -10
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_5(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 1.5
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_6(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 0.0
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_7(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = ''
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()
    
    def test_put_gpu_resources_cache_capacity_8(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 'xxxx'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_9(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = '_%20'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_10(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = []
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_11(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = [1, 2]
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_12(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = {}
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_13(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = {'k':1}
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_14(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = None
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_15(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = -3.222
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()        

    
    def test_put_gpu_resources_cache_capacity_16(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = ' '
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()
    
    def test_put_gpu_resources_cache_capacity_17(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = '汉子'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_18(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = '\t'
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_19(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        requests.put(base_url + 'config/gpu_resources#', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources#')
        assert false_res.json() == res.json()
        
    
    def test_put_gpu_resources_cache_capacity_20(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        requests.put(base_url + 'config/gpu_resources?', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources?')
        assert false_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_21(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        requests.put(base_url + 'config/gpu_resources/', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources/')
        assert false_res.json() == res.json()

    # BUG
    def test_put_gpu_resources_cache_capacity_22(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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
        req['cache_capacity'] = 0
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        logging.getLogger().info(res.json())
        # assert true_res.json() == res.json()
        
    def test_put_gpu_resources_cache_capacity_23(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 5
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['cache_capacity'] == res.json()['cache_capacity']

    # BUG
    def test_put_gpu_resources_cache_capacity_24(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 2147386
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        # assert true_res.json()['cache_capacity'] == res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_25(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = -10
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_26(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 1.5
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_27(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 0.0
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_28(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = ''
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()
    
    def test_put_gpu_resources_cache_capacity_29(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = 'xxxx'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_30(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = '_%20'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_31(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = []
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_32(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = [1, 2]
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_33(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = {}
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_34(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = {'k':1}
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_35(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = None
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        logging.getLogger().info(res.json())
        assert res.status_code == 400
        assert res.json()['code'] == 33
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_36(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = -3.222
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()   

    
    def test_put_gpu_resources_cache_capacity_37(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = ' '
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()
    
    def test_put_gpu_resources_cache_capacity_38(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = '汉子'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_39(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        req['cache_capacity'] = '\t'
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        assert res.status_code == 500
        assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        # logging.getLogger().info(res.json())
        assert req['cache_capacity'] != res.json()['cache_capacity']
        assert true_res.json() == res.json()

    
    def test_put_gpu_resources_cache_capacity_40(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # # req = copy.deepcopy(original_req)
        # requests.put(base_url + 'config/gpu_resources#', data=json.dumps(req))
        # res = requests.get(base_url + 'config/gpu_resources#')
        # assert original_req == res.json()
        
    
    def test_put_gpu_resources_cache_capacity_41(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        # req = copy.deepcopy(original_req)
        # requests.put(base_url + 'config/gpu_resources?', data=json.dumps(req))
        # res = requests.get(base_url + 'config/gpu_resources?')
        # assert original_req == res.json()

    
    def test_put_gpu_resources_cache_capacity_42(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

    def test_post_gpu_resources_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + 'config/gpu_resources')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_post_gpu_resources_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = None
        res = requests.post(base_url + 'config/gpu_resources', json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_post_gpu_resources_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = {}
        res = requests.post(base_url + 'config/gpu_resources', json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_post_gpu_resources_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        req = {'a':1, 'b':2}
        res = requests.post(base_url + 'config/gpu_resources', json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_options_gpu_resources_1(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'config/gpu_resources')
        assert res.status_code == 204

    def test_options_gpu_resources_2(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'config/gpu_resources?a=1')
        assert res.status_code == 204
    
    def test_options_gpu_resources_3(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + 'config/gpu_resources/aaa')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_gpu_resources_1(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/geterror')
        logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_gpu_resources_2(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'configxxx/advanced')
        logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

# -------------------------------------------------------------- xxxxxxxxxx ---------------------------------------------------------------
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
    
    def test_put_gpu_resources_7(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = None
        
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert res.json()['enable'] == True
        assert res.json()['cache_capacity'] == 1
        assert 'search_resources' in res.json().keys()
        assert 'build_index_resources' in res.json().keys()

    def test_put_gpu_resources_8(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + 'config/gpu_resources')
        original_req = res.json()
        req = copy.deepcopy(original_req)
        
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        assert original_req == res.json()

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
        assert 'Invalid gpu build index resource' in res.json()['message']

        res = requests.get(base_url + 'config/gpu_resources')
        assert req['build_index_resources'] != res.json()['build_index_resources']
        assert true_res.json() == res.json()

    def test_put_gpu_resources_build_index_resources_45(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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
        logging.getLogger().info(res.text)
        # assert res.status_code == 200
        # assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        logging.getLogger().info(res.json())
        # assert req['build_index_resources'] != res.json()['build_index_resources']
        # assert true_res.json() == res.json()
    
    def test_put_gpu_resources_build_index_resources_46(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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


    def test_put_gpu_resources_search_resources_1(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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
        req['search_resources'] = 0
        requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        res = requests.get(base_url + 'config/gpu_resources')
        logging.getLogger().info(res.json())
        
    def test_put_gpu_resources_search_resources_23(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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
        assert true_res.json() == res.json()

    def test_put_gpu_resources_search_resources_45(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

        req['search_resources'] = ['gpu1']
        res = requests.put(base_url + 'config/gpu_resources', data=json.dumps(req))
        logging.getLogger().info(res.text)
        # assert res.status_code == 200
        # assert 'Internal Server Error' in res.text
        res = requests.get(base_url + 'config/gpu_resources')
        logging.getLogger().info(res.json())
        # assert req['search_resources'] != res.json()['search_resources']
        # assert true_res.json() == res.json()
    
    def test_put_gpu_resources_search_resources_46(self, args):
        if self.get_mode(args) == 'CPU':
            pytest.skip('this API do not support CPU version')
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

# ----------------------------------- basic -----------------------------------
