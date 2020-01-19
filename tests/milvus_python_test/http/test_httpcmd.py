import pytest
import requests
import logging
import json
import copy
import random
import arrow
from faker import Faker
    
# ----------------------------------- command -----------------------------------
class TestHTTPCMD:

    # 1. version    => ServerVersion()
    # 2. status   => ServerStatus()
    # 3. build_commit_id
    # 4. mode
    # 5. get_system_info

    system_prefix = 'system/'
    version = '0.6.0'
    status = 'OK'
    mode = 'GPU'

    def test_http_cmd_version(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = 'version'
        res = requests.get(base_url + self.system_prefix + cmd)
        # logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert res.json()['reply'] == self.version
    
    def test_http_cmd_status(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = 'status'
        res = requests.get(base_url + self.system_prefix + cmd)
        # logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_mode(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = 'mode'
        res = requests.get(base_url + self.system_prefix + cmd)
        # logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = 'build_commit_id'
        res = requests.get(base_url + self.system_prefix + cmd)
        # logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    # TODO dont know how to use tasktable
    def test_http_cmd_tasktable(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = 'tasktable'
        res = requests.get(base_url + self.system_prefix + cmd)
        logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_get_system_info(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = 'get_system_info'
        res = requests.get(base_url + self.system_prefix + cmd)
        logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    # def test_http_cmd_get_config(self):
    #     cmd = 'get_config'
    #     res = requests.get(base_url + self.system_prefix + cmd)
    #     assert res.status_code == 200
    #     assert 'reply' in res.json().keys()

    def test_http_cmd_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = ''
        res = requests.get(base_url + self.system_prefix + cmd)
        # code=404
        # description=Not Found
        # message=Current url has no mapping
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = '/'
        res = requests.get(base_url + self.system_prefix + cmd)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = '//'
        res = requests.get(base_url + self.system_prefix + cmd)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = '/fuck/'
        res = requests.get(base_url + self.system_prefix + cmd)
        # logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert 'Unknown command' == res.json()['reply']

    def test_http_cmd_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        cmd = 'unknown_cmd'
        res = requests.get(base_url + self.system_prefix + cmd)
        assert res.status_code == 200
        assert 'Unknown command' == res.json()['reply']
        
    def test_http_cmd_version_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version/myparams')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_version_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version?q=myparams')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version/10')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_version_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version?q=10')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/version')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '//version')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/////version')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version/')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/version/')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version//')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '//version//')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version/////')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/////version/////')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version/?')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    # TODO return code diff with other apis
    def test_http_cmd_version_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version%20')
        # assert res.status_code == 404
        assert res.status_code == 200
        # assert 'Current url has no mapping' in res.text
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_version_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version?')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version??')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version\/')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_version_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '\/version')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_version_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version/%20')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_version_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + r'%20version')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_version_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + r'%20/version')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_version_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version#')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version/ ')
        # logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_version_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        rurl = base_url + self.system_prefix + 'version#'
        logging.getLogger().info(rurl)
        mm = rurl.replace('.', '%2E')
        res = requests.get(mm)
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version?a=1&b=2')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_version_27(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'version?a=1%26b=2')
        assert res.status_code == 200
        assert res.json()['reply'] == self.version

    def test_http_cmd_post_version_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'version')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_post_version_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'version')
        req = {}
        requests.post(base_url + 'version', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_post_version_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'version')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'version', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_put_version_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'version')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_put_version_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'version')
        req = {}
        requests.post(base_url + 'version', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_put_version_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'version')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'version', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_options_version_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'version')
        assert res.status_code == 204
    
    def test_http_cmd_options_version_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'version?a=1')
        assert res.status_code == 204
    
    def test_http_cmd_options_version_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'version/aaa')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_status_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status/myparams')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_status_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status?q=myparams')
        logging.getLogger().info(res.json())
        assert res.status_code == 200
        # assert res.json()['reply'] == self.status

    def test_http_cmd_status_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status/10')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_status_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status?q=10')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/status')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '//status')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/////status')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status/')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/status/')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status//')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '//status//')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status/////')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/////status/////')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status/?')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    # TODO return code diff with other apis
    def test_http_cmd_status_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status%20')
        # assert res.status_code == 404
        assert res.status_code == 200
        # assert 'Current url has no mapping' in res.text
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_status_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status?')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status??')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status\/')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_status_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '\/status')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_status_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status/%20')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_status_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + r'%20status')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_status_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + r'%20/status')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_status_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status#')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status/ ')
        # logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_status_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        rurl = base_url + self.system_prefix + 'status#'
        logging.getLogger().info(rurl)
        mm = rurl.replace('.', '%2E')
        res = requests.get(mm)
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status?a=1&b=2')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_status_27(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'status?a=1%26b=2')
        assert res.status_code == 200
        assert res.json()['reply'] == self.status

    def test_http_cmd_post_status_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'status')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_post_status_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'status')
        req = {}
        requests.post(base_url + 'status', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_post_status_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'status')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'status', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_put_status_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'status')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_put_status_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'status')
        req = {}
        requests.post(base_url + 'status', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_put_status_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'status')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'status', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_options_status_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'status')
        assert res.status_code == 204
    
    def test_http_cmd_options_status_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'status?a=1')
        assert res.status_code == 204
    
    def test_http_cmd_options_status_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'status/aaa')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_mode_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode/myparams')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_mode_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode?q=myparams')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode/10')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_mode_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode?q=10')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/mode')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '//mode')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/////mode')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode/')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/mode/')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode//')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '//mode//')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode/////')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/////mode/////')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode/?')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    # TODO return code diff with other apis
    def test_http_cmd_mode_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode%20')
        # assert res.status_code == 404
        assert res.status_code == 200
        # assert 'Current url has no mapping' in res.text
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_mode_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode?')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode??')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode\/')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_mode_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '\/mode')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_mode_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode/%20')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_mode_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + r'%20mode')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_mode_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + r'%20/mode')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_mode_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode#')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode/ ')
        # logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_mode_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        rurl = base_url + self.system_prefix + 'mode#'
        logging.getLogger().info(rurl)
        mm = rurl.replace('.', '%2E')
        res = requests.get(mm)
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode?a=1&b=2')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_mode_27(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'mode?a=1%26b=2')
        assert res.status_code == 200
        assert res.json()['reply'] == self.mode

    def test_http_cmd_post_mode_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'mode')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_post_mode_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'mode')
        req = {}
        requests.post(base_url + 'mode', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_post_mode_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'mode')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'mode', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_put_mode_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'mode')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_put_mode_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'mode')
        req = {}
        requests.post(base_url + 'mode', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_put_mode_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'mode')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'mode', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_options_mode_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'mode')
        assert res.status_code == 204
    
    def test_http_cmd_options_mode_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'mode?a=1')
        assert res.status_code == 204
    
    def test_http_cmd_options_mode_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'mode/aaa')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    
    def test_http_cmd_get_system_info_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info/myparams')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_get_system_info_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info?q=myparams')
        # logging.getLogger().info(res.json())
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info/10')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_get_system_info_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info?q=10')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/get_system_info')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '//get_system_info')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/////get_system_info')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info/')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/get_system_info/')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info//')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '//get_system_info//')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info/////')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/////get_system_info/////')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info/?')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    # TODO return code diff with other apis
    def test_http_cmd_get_system_info_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info%20')
        # assert res.status_code == 404
        assert res.status_code == 200
        # assert 'Current url has no mapping' in res.text
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_get_system_info_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info?')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info??')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info\/')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_get_system_info_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '\/get_system_info')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_get_system_info_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info/%20')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_get_system_info_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + r'%20get_system_info')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_get_system_info_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + r'%20/get_system_info')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_get_system_info_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info#')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info/ ')
        # logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_get_system_info_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        rurl = base_url + self.system_prefix + 'get_system_info#'
        logging.getLogger().info(rurl)
        mm = rurl.replace('.', '%2E')
        res = requests.get(mm)
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info?a=1&b=2')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_get_system_info_27(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'get_system_info?a=1%26b=2')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()
        real_res = eval(res.json()['reply'])
        assert 'gpu0_memory_total' in real_res.keys()
        assert 'gpu0_memory_used' in real_res.keys()
        assert 'memory_total' in real_res.keys()
        assert 'memory_used' in real_res.keys()

    def test_http_cmd_post_get_system_info_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'get_system_info')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_post_get_system_info_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'get_system_info')
        req = {}
        requests.post(base_url + 'get_system_info', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_post_get_system_info_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'get_system_info')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'get_system_info', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_put_get_system_info_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'get_system_info')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_put_get_system_info_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'get_system_info')
        req = {}
        requests.post(base_url + 'get_system_info', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_put_get_system_info_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'get_system_info')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'get_system_info', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_options_get_system_info_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'get_system_info')
        assert res.status_code == 204
    
    def test_http_cmd_options_get_system_info_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'get_system_info?a=1')
        assert res.status_code == 204
    
    def test_http_cmd_options_get_system_info_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'get_system_info/aaa')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    
    def test_http_cmd_build_commit_id_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id/myparams')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_build_commit_id_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id?q=myparams')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id/10')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_build_commit_id_4(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id?q=10')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_5(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/build_commit_id')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_6(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '//build_commit_id')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_7(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/////build_commit_id')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_8(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id/')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_9(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/build_commit_id/')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_10(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id//')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_11(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '//build_commit_id//')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_12(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id/////')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_13(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '/////build_commit_id/////')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_14(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id/?')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    # TODO return code diff with other apis
    def test_http_cmd_build_commit_id_15(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id%20')
        # assert res.status_code == 404
        assert res.status_code == 200
        # assert 'Current url has no mapping' in res.text
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_build_commit_id_16(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id?')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_17(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id??')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_18(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id\/')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_build_commit_id_19(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + '\/build_commit_id')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_build_commit_id_20(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id/%20')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_build_commit_id_21(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + r'%20build_commit_id')
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert res.json()['reply'] == 'Unknown command'

    def test_http_cmd_build_commit_id_22(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + r'%20/build_commit_id')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_build_commit_id_23(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id#')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_24(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id/ ')
        # logging.getLogger().info(res.text)
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_build_commit_id_25(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        rurl = base_url + self.system_prefix + 'build_commit_id#'
        logging.getLogger().info(rurl)
        mm = rurl.replace('.', '%2E')
        res = requests.get(mm)
        # logging.getLogger().info(res.text)
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_26(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id?a=1&b=2')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_build_commit_id_27(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.get(base_url + self.system_prefix + 'build_commit_id?a=1%26b=2')
        assert res.status_code == 200
        assert 'reply' in res.json().keys()

    def test_http_cmd_post_build_commit_id_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'build_commit_id')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_post_build_commit_id_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'build_commit_id')
        req = {}
        requests.post(base_url + 'build_commit_id', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_post_build_commit_id_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.post(base_url + self.system_prefix + 'build_commit_id')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'build_commit_id', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_put_build_commit_id_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'build_commit_id')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

    def test_http_cmd_put_build_commit_id_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'build_commit_id')
        req = {}
        requests.post(base_url + 'build_commit_id', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_put_build_commit_id_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.put(base_url + self.system_prefix + 'build_commit_id')
        req = {'a':1, 'b':2}
        requests.post(base_url + 'build_commit_id', data=json.dumps(req))
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text
    
    def test_http_cmd_options_build_commit_id_1(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'build_commit_id')
        assert res.status_code == 204
    
    def test_http_cmd_options_build_commit_id_2(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'build_commit_id?a=1')
        assert res.status_code == 204
    
    def test_http_cmd_options_build_commit_id_3(self, args):
        base_url = 'http://%s:%s/' % (args['ip'], args['port'])
        res = requests.options(base_url + self.system_prefix + 'build_commit_id/aaa')
        assert res.status_code == 404
        assert 'Current url has no mapping' in res.text

# ----------------------------------- command -----------------------------------