import pdb
import copy
import struct

import pytest
import threading
import datetime
import logging
from time import sleep
from multiprocessing import Process
import numpy
from milvus import IndexType, MetricType
from utils import *

dim = 128
table_id = "test_search"
add_interval_time = 2
vectors = gen_vectors(6000, dim)
# vectors /= numpy.linalg.norm(vectors)
# vectors = vectors.tolist()
nprobe = 1
epsilon = 0.001
tag = "overallpaper"
non_exist_id = 9527
small_size = 2500
raw_vectors, binary_vectors = gen_binary_vectors(6000, dim)


class TestSearchById:
    def init_data(self, connect, table, nb=6000):
        '''
        Generate vectors and add it in table, before search vectors
        '''
        global vectors
        if nb == 6000:
            add_vectors = vectors
        else:  
            add_vectors = gen_vectors(nb, dim)

        status, ids = connect.add_vectors(table, add_vectors)
        sleep(add_interval_time)
        return add_vectors, ids
    
    def init_data_no_flush(self, connect, table, nb=6000):
        
        global vectors
        if nb == 6000:
            add_vectors = vectors
        else:  
            add_vectors = gen_vectors(nb, dim)

        status, ids = connect.add_vectors(table, add_vectors)
        # sleep(add_interval_time)
        return add_vectors, ids

    def init_data_no_flush_ids(self, connect, table, nb=6000):
        
        global vectors
        if nb == 6000:
            add_vectors = vectors
        else:  
            add_vectors = gen_vectors(nb, dim)
            my_ids = [i for i in range(nb)]

        status, ids = connect.add_vectors(table, add_vectors, my_ids)
        # sleep(add_interval_time)
        return add_vectors, ids

    def init_data_ids(self, connect, table, nb=6000):
        global vectors
        if nb == 6000:
            add_vectors = vectors
        else:  
            add_vectors = gen_vectors(nb, dim)
            my_ids = [i for i in range(nb)]

        status, ids = connect.add_vectors(table, add_vectors, my_ids)
        sleep(add_interval_time)
        return add_vectors, ids

    def add_data(self, connect, table, vectors):
        '''
        Add specified vectors to table
        '''
        
        status, ids = connect.add_vectors(table, vectors)
        # sleep(add_interval_time)
        sleep(10)
        return vectors, ids

    def add_data_ids(self, connect, table, vectors):
        
        my_ids = [i for i in range(len(vectors))]
        status, ids = connect.add_vectors(table, vectors, my_ids)
        sleep(add_interval_time)
        return vectors, ids

    def add_data_and_flush(self, connect, table, vectors):
        
        status, ids = connect.add_vectors(table, vectors)
        connect.flush([table])
        return vectors, ids

    def add_data_and_flush_ids(self, connect, table, vectors):
        
        my_ids = [i for i in range(len(vectors))]
        status, ids = connect.add_vectors(table, vectors, my_ids)
        connect.flush([table])
        return vectors, ids

    def add_data_no_flush(self, connect, table, vectors):
        '''
        Add specified vectors to table
        '''
        status, ids = connect.add_vectors(table, vectors)
        return vectors, ids
    
    def add_data_no_flush_ids(self, connect, table, vectors):
        my_ids = [i for i in range(len(vectors))]
        status, ids = connect.add_vectors(table, vectors, my_ids)
        return vectors, ids

    # delete data and auto flush - timeout due to the flush interval in config file
    def delete_data(self, connect, table, ids):
        '''
        delete vectors by id
        '''

        status = connect.delete_by_id(table, ids)
        sleep(add_interval_time)
        return status

    # delete data and auto flush - timeout due to the flush interval in config file
    def delete_data_no_flush(self, connect, table, ids):
        '''
        delete vectors by id
        '''
        status = connect.delete_by_id(table, ids)
        return status

    # delete data and manual flush
    def delete_data_and_flush(self, connect, table, ids):
        '''
        delete vectors by id
        '''
        status = connect.delete_by_id(table, ids)
        connect.flush([table])
        return status
    
    def check_no_result(self, results):
        
        if len(results) == 0:
            return True

        flag = True
        for r in results:
            flag = flag and (r.id == -1)
            if not flag:
                return False
        
        return flag

    
    def init_data_partition(self, connect, table, partition_tag, nb=6000):
        '''
        Generate vectors and add it in table, before search vectors
        '''
        global vectors
        if nb == 6000:
            add_vectors = vectors
        else:  
            add_vectors = gen_vectors(nb, dim)
            # add_vectors /= numpy.linalg.norm(add_vectors)
            # add_vectors = add_vectors.tolist()
        status, ids = connect.add_vectors(table, add_vectors, partition_tag=partition_tag)
        sleep(add_interval_time)
        return add_vectors, ids
    
    def init_data_and_flush(self, connect, table, nb=6000):
        '''
        Generate vectors and add it in table, before search vectors
        '''
        global vectors
        if nb == 6000:
            add_vectors = vectors
        else:  
            add_vectors = gen_vectors(nb, dim)
            # add_vectors /= numpy.linalg.norm(add_vectors)
            # add_vectors = add_vectors.tolist()
        status, ids = connect.add_vectors(table, add_vectors)
        connect.flush([table])
        return add_vectors, ids

    def init_data_and_flush_ids(self, connect, table, nb=6000):
        
        global vectors
        if nb == 6000:
            add_vectors = vectors
        else:  
            add_vectors = gen_vectors(nb, dim)
            my_ids = [i for i in range(nb)]
        
        status, ids = connect.add_vectors(table, add_vectors, my_ids)
        connect.flush([table])
        return add_vectors, ids

    def init_data_partition_and_flush(self, connect, table, partition_tag, nb=6000):
        '''
        Generate vectors and add it in table, before search vectors
        '''
        global vectors
        if nb == 6000:
            add_vectors = vectors
        else:  
            add_vectors = gen_vectors(nb, dim)
            # add_vectors /= numpy.linalg.norm(add_vectors)
            # add_vectors = add_vectors.tolist()
        status, ids = connect.add_vectors(table, add_vectors, partition_tag=partition_tag)
        connect.flush([table])
        return add_vectors, ids

    def init_binary_data(self, connect, table, nb=6000, insert=True):
        '''
        Generate vectors and add it in table, before search vectors
        '''
        ids = []
        global binary_vectors
        global raw_vectors
        if nb == 6000:
            add_vectors = binary_vectors
            add_raw_vectors = raw_vectors
        else:  
            add_raw_vectors, add_vectors = gen_binary_vectors(nb, dim)
            # add_vectors /= numpy.linalg.norm(add_vectors)
            # add_vectors = add_vectors.tolist()
        if insert is True:
            status, ids = connect.add_vectors(table, add_vectors)
            sleep(add_interval_time)
        return add_raw_vectors, add_vectors, ids

    """
    generate valid create_index params
    """
    @pytest.fixture(
        scope="function",
        params=gen_index_params()
    )
    def get_index_params(self, request, connect):
        if request.param["index_type"] == IndexType.IVF_PQ:
            pytest.skip("Skip PQ Temporary")

        if str(connect._cmd("mode")[1]) == "CPU":
            if request.param["index_type"] == IndexType.IVF_SQ8H:
                pytest.skip("sq8h not support in open source")

        if str(connect._cmd("mode")[1]) == "GPU":
            config = eval(connect._cmd("get_config *")[1])
            if config['gpu_resource_config']['enable'] == 'true':
                pytest.skip("GPU search resource enable not support yet")
            if config['gpu_resource_config']['enable'] == 'false':
                if request.param["index_type"] == IndexType.IVF_SQ8H:
                    pytest.skip("sq8h not support yet")

        return request.param

    @pytest.fixture(
        scope="function",
        params=gen_simple_index_params()
    )
    def get_simple_index_params(self, request, connect):
        if request.param["index_type"] == IndexType.IVF_PQ:
            pytest.skip("Skip PQ Temporary")

        if str(connect._cmd("mode")[1]) == "CPU":
            if request.param["index_type"] == IndexType.IVF_SQ8H:
                pytest.skip("sq8h not support in open source")

        if str(connect._cmd("mode")[1]) == "GPU":
            config = eval(connect._cmd("get_config *")[1])
            if config['gpu_resource_config']['enable'] == 'true':
                pytest.skip("GPU search resource enable not support yet")
            if config['gpu_resource_config']['enable'] == 'false':
                if request.param["index_type"] == IndexType.IVF_SQ8H:
                    pytest.skip("sq8h not support yet")

        return request.param

    @pytest.fixture(
        scope="function",
        params=gen_simple_index_params()
    )
    def get_jaccard_index_params(self, request, connect):
        logging.getLogger().info(request.param)
        if request.param["index_type"] == IndexType.IVFLAT or request.param["index_type"] == IndexType.FLAT:
            return request.param
        else:
            pytest.skip("Skip index Temporary")

    @pytest.fixture(
        scope="function",
        params=gen_simple_index_params()
    )
    def get_hamming_index_params(self, request, connect):
        logging.getLogger().info(request.param)
        if request.param["index_type"] == IndexType.IVFLAT or request.param["index_type"] == IndexType.FLAT:
            return request.param
        else:
            pytest.skip("Skip index Temporary")

    """
    generate top-k params
    """
    @pytest.fixture(
        scope="function",
        params=[1, 99, 1024, 2048, 2049]
    )
    def get_top_k(self, request):
        yield request.param

    # auto flush
    def test_search_top_k_flat_index_1(self, connect, table, get_top_k):
        '''
        target: test basic search fuction, all the search params is corrent, change top-k value
        method: search with the given vector id, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        vectors, ids = self.init_data(connect, table, nb=small_size)
        query_id = ids[0]
        # logging.getLogger().info(ids[:10])
        top_k = get_top_k
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)

        if top_k <= 2048:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()

    # manual flush
    def test_search_top_k_flat_index_2(self, connect, table, get_top_k):
        '''
        target: test basic search fuction, all the search params is corrent, change top-k value
        method: search with the given vector id, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        query_id = ids[0]
        top_k = get_top_k
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 2048:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()
    
    # manual flush
    def test_search_top_k_flat_index_4(self, connect, table, get_top_k):
        '''
        target: test basic search fuction, all the search params is corrent, change top-k value
        method: search with the given vector id, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        query_id = non_exist_id
        top_k = get_top_k
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 2048:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            # assert len(result[0]) == 0
            # assert result[0][0].distance <= epsilon
            # assert check_result(result[0], ids[0])
        else:
            assert not status.OK()

    # auto flush
    def test_search_top_k_flat_index_3(self, connect, table, get_top_k):
        '''
        target: test basic search fuction, all the search params is corrent, change top-k value
        method: search with the given vector id, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        vectors, ids = self.init_data(connect, table, nb=small_size)
        query_id = non_exist_id
        # logging.getLogger().info(ids[:10])
        top_k = get_top_k
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)

        if top_k <= 2048:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            # assert len(result[0]) == 0
            # assert result[0][0].distance <= epsilon
            # assert check_result(result[0], ids[0])
        else:
            assert not status.OK()
    

    # auto flush
    def test_search_top_k_flat_index_id_1(self, connect, table, get_top_k):
        
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        query_id = ids[0]
        logging.getLogger().info(ids[:10])
        top_k = get_top_k
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)

        if top_k <= 2048:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()

    # manual flush
    def test_search_top_k_flat_index_id_2(self, connect, table, get_top_k):
        
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        query_id = ids[0]
        top_k = get_top_k
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 2048:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()
    
    # auto flush
    def test_search_top_k_flat_index_id_3(self, connect, table, get_top_k):
        
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        query_id = non_exist_id
        top_k = get_top_k
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)

        if top_k <= 2048:
            assert status.OK()
            # assert len(result[0]) == min(len(vectors), top_k)
            # assert len(result[0]) == 0
            # assert result[0][0].distance <= epsilon
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()
    
    # manual flush
    def test_search_top_k_flat_index_id_4(self, connect, table, get_top_k):
        
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        query_id = non_exist_id
        top_k = get_top_k
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 2048:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            # assert len(result[0]) == 0
            # assert result[0][0].distance <= epsilon
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()
    

        # ------------------------------------------------------------- l2, add manual flush, delete, search ------------------------------------------------------------- #
    # ids, manual flush, search table, exist
    def test_search_m_l2_index_params_id_1(self, connect, table, get_simple_index_params):
        '''
        target: test basic search fuction, all the search params is corrent, test all index params, and build
        method: search with the given vectors, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        # logging.getLogger().info(result)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()
    
    # ids, manual flush, search table, non exist
    def test_search_m_l2_index_params_id_2(self, connect, table, get_simple_index_params):
        '''
        target: test basic search fuction, all the search params is corrent, test all index params, and build
        method: search with the given vectors, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = non_exist_id
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        # logging.getLogger().info(result)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            # assert len(result[0]) == 0
            # assert result[0][0].distance <= epsilon
            # assert check_result(result[0], ids[0])
        else:
            assert not status.OK() 

    # ids, manual flush, delete, manual flush, search table, exist
    def test_search_m_l2_index_params_id_3(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_and_flush(connect, table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # ids, manual flush, delete, manual flush, search table, non exist
    def test_search_m_l2_index_params_id_4(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_and_flush(connect, table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # ids, manual flush, delete, no flush, search table, exist
    def test_search_m_l2_index_params_id_5(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            # assert self.check_no_result(result[0])
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # ids, manual flush, delete, no flush, search table, non exist
    def test_search_m_l2_index_params_id_6(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # # ids, manual flush, delete, no flush, add again no id, manual flush, search table, exist
    # def test_search_m_l2_index_params_id_7(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     vectors, new_ids = self.add_data_and_flush(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         assert len(result[0]) == min(len(vectors), top_k)
    #         assert result[0][0].distance <= epsilon
    #         assert check_result(result[0], ids[0])
    #     else:
    #         assert not status.OK()

    # # ids, manual flush, delete, no flush, add again no id, manual flush, search table, exist
    # def test_search_m_l2_index_params_id_8(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         assert self.check_no_result(result[0])
    #     else:
    #         assert not status.OK()

    # # add manual flush, delete no flush, add again manual flush
    # # TODO: https://github.com/milvus-io/milvus/issues/1170
    # def test_search_m_l2_index_params_id_9(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     vectors, new_ids = self.add_data_and_flush(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     query_id = non_exist_id + len(ids)
    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         assert self.check_no_result(result[0])
    #     else:
    #         assert not status.OK()

    # # add manual flush, delete no flush, add again no flush
    # # TODO: https://github.com/milvus-io/milvus/issues/1170
    # def test_search_m_l2_index_params_id_10(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     query_id = non_exist_id + len(ids)
    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         assert self.check_no_result(result[0])
    #     else:
    #         assert not status.OK()

    # # add manual flush, delete no flush, add again manual flush, search new id, exist
    # # TODO: https://github.com/milvus-io/milvus/issues/1170
    # def test_search_m_l2_index_params_id_11(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     vectors, new_ids = self.add_data_and_flush(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     query_id = new_ids[0]
    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         assert len(result[0]) == min(len(vectors), top_k)
    #         assert result[0][0].distance <= epsilon
    #         assert check_result(result[0], ids[0])
    #     else:
    #         assert not status.OK()

    # # add manual flush, delete no flush, add again no flush
    # # TODO: https://github.com/milvus-io/milvus/issues/1170
    # def test_search_m_l2_index_params_id_12(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     query_id = new_ids[0]
    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         # assert len(result[0]) == min(len(vectors), top_k)
    #         # assert result[0][0].distance <= epsilon
    #         assert self.check_no_result(result[0])
    #     else:
    #         assert not status.OK()

    # add manual flush, delete no flush, add again manual flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    # updateddd #
    def test_search_m_l2_index_params_id_13(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_and_flush_ids(connect, table, vectors)
        status = connect.create_index(table, index_params)

        # query_id = new_ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], query_id)
            # assert result[0][0].id != query_id
        else:
            assert not status.OK()


    # add manual flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_m_l2_index_params_id_14(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush_ids(connect, table, vectors)
        status = connect.create_index(table, index_params)

        # query_id = new_ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # add manual flush, delete no flush, add again manual flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_m_l2_index_params_id_15(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_and_flush_ids(connect, table, vectors)
        status = connect.create_index(table, index_params)

        query_id = non_exist_id + len(ids)
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            # assert len(result[0]) == min(len(vectors), top_k)
            # assert result[0][0].distance <= epsilon
            # assert check_result(result[0], query_id)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()


    # add manual flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_m_l2_index_params_id_16(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush_ids(connect, table, vectors)
        status = connect.create_index(table, index_params)

        query_id = non_exist_id + len(ids)
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            # assert len(result[0]) == min(len(vectors), top_k)
            # assert result[0][0].distance <= epsilon
            # assert check_result(result[0], query_id)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # ------------------------------------------------------------- l2, add manual flush, delete, search ------------------------------------------------------------- #

    # ------------------------------------------------------------- l2, add auto flush, delete, search ------------------------------------------------------------- #
    # ids, auto flush, search table, exist
    def test_search_l2_index_params_id_1(self, connect, table, get_simple_index_params):
        '''
        target: test basic search fuction, all the search params is corrent, test all index params, and build
        method: search with the given vectors, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        # logging.getLogger().info(result)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()
    
    # ids, auto flush, search table, non exist
    def test_search_l2_index_params_id_2(self, connect, table, get_simple_index_params):
        '''
        target: test basic search fuction, all the search params is corrent, test all index params, and build
        method: search with the given vectors, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = non_exist_id
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        # logging.getLogger().info(result)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            # assert len(result[0]) == 0
            # assert result[0][0].distance <= epsilon
            # assert check_result(result[0], ids[0])
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # ids, no flush, search table, exist
    def test_search_l2_index_params_id_17(self, connect, table, get_simple_index_params):
        
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_no_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        # logging.getLogger().info(result)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            # assert result[0][0].distance <= epsilon
            # assert self.check_no_result(result[0])
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()

    # ids, no flush, search table, non exist
    def test_search_l2_index_params_id_18(self, connect, table, get_simple_index_params):
        
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_no_flush_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = non_exist_id + len(ids)
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        # logging.getLogger().info(result)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            # assert result[0][0].distance <= epsilon
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # ids, auto flush, delete, auto flush, search table, exist
    def test_search_l2_index_params_id_3(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # ids, auto flush, delete, auto flush, search table, non exist
    def test_search_l2_index_params_id_4(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # ids, auto flush, delete, no flush, search table, exist
    def test_search_l2_index_params_id_5(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            # assert self.check_no_result(result[0])
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # ids, auto flush, delete, no flush, search table, non exist
    def test_search_l2_index_params_id_6(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # def test_search_test(self, connect, table):

    #     index_params = {'index_type':IndexType.IVF_SQ8, 'nlist':512}
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_ids(connect, table, nb=small_size)
    #     logging.getLogger().info(ids[:10])
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     # status = self.delete_data_no_flush(connect, table, [query_id])
    #     # # status = self.delete_data(connect, table, [query_id])
    #     # assert status.OK()

    #     logging.getLogger().info(table)
    #     status, new_ids = connect.add_vectors(table, vectors)
    #     logging.getLogger().info(status)
    #     status = connect.create_index(table, index_params)

    #     logging.getLogger().info(new_ids[:10])

    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     for r in result[0][:5]:
    #         logging.getLogger().info(r)
    #     # if top_k <= 1024:
    #     #     assert status.OK()
    #     #     assert len(result[0]) == min(len(vectors), top_k)
    #     #     assert result[0][0].distance <= epsilon
    #     #     assert check_result(result[0], ids[0])
    #     # else:
    #     #     assert not status.OK()


    # # ids, auto flush, delete, no flush, add again no id, auto flush, search table, exist
    # def test_search_l2_index_params_id_7(self, connect, table, get_simple_index_params):

    #     index_params = {'index_type':IndexType.IVF_SQ8, 'nlist':512}
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_ids(connect, table, nb=small_size)
    #     logging.getLogger().info(ids[:10])
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     # status = self.delete_data(connect, table, [query_id])
    #     assert status.OK()

    #     logging.getLogger().info(table)
    #     vectors, new_ids = self.add_data(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     logging.getLogger().info(new_ids[:10])

    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         assert len(result[0]) == min(len(vectors), top_k)
    #         assert result[0][0].distance <= epsilon
    #         assert check_result(result[0], ids[0])
    #     else:
    #         assert not status.OK()

    # # ids, auto flush, delete, no flush, add again no id, auto flush, search table, exist
    # def test_search_l2_index_params_id_8(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         assert self.check_no_result(result[0])
    #     else:
    #         assert not status.OK()

    # # add auto flush, delete no flush, add again auto flush
    # # TODO: https://github.com/milvus-io/milvus/issues/1170
    # def test_search_l2_index_params_id_9(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     vectors, new_ids = self.add_data(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     query_id = non_exist_id + len(ids)
    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         assert self.check_no_result(result[0])
    #     else:
    #         assert not status.OK()

    # # add auto flush, delete no flush, add again no flush
    # # TODO: https://github.com/milvus-io/milvus/issues/1170
    # def test_search_l2_index_params_id_10(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     query_id = non_exist_id + len(ids)
    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         assert self.check_no_result(result[0])
    #     else:
    #         assert not status.OK()

    # # add auto flush, delete no flush, add again auto flush, search new id, exist
    # # TODO: https://github.com/milvus-io/milvus/issues/1170
    # def test_search_l2_index_params_id_11(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     # vectors, new_ids = self.add_data(connect, table, vectors)
    #     vectors, new_ids = connect.add_vectors(table, vectors)
    #     status = connect.create_index(table, index_params)

    #     logging.getLogger().info(new_ids[:10])
    #     query_id = new_ids[0]
    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         assert len(result[0]) == min(len(vectors), top_k)
    #         assert result[0][0].distance <= epsilon
    #         assert check_result(result[0], ids[0])
    #     else:
    #         assert not status.OK()

    # # add auto flush, delete no flush, add again no flush
    # # TODO: https://github.com/milvus-io/milvus/issues/1170
    # def test_search_l2_index_params_id_12(self, connect, table, get_simple_index_params):

    #     index_params = get_simple_index_params
    #     logging.getLogger().info(index_params)
    #     vectors, ids = self.init_data_ids(connect, table, nb=small_size)
    #     status = connect.create_index(table, index_params)
    #     query_id = ids[0]
    #     top_k = 10
    #     nprobe = 1

    #     status = self.delete_data_no_flush(connect, table, [query_id])
    #     assert status.OK()

    #     vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
    #     status = connect.create_index(table, index_params)

    #     query_id = new_ids[0]
    #     status, result = connect.search_by_id(table, top_k, nprobe, query_id)
    #     if top_k <= 1024:
    #         assert status.OK()
    #         # assert len(result[0]) == min(len(vectors), top_k)
    #         # assert result[0][0].distance <= epsilon
    #         assert self.check_no_result(result[0])
    #     else:
    #         assert not status.OK()

    # add auto flush, delete no flush, add again auto flush
    def test_search_l2_index_params_id_13(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_ids(connect, table, vectors)
        status = connect.create_index(table, index_params)

        # query_id = new_ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()


    # add auto flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_l2_index_params_id_14(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush_ids(connect, table, vectors)
        status = connect.create_index(table, index_params)

        # query_id = new_ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again auto flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_l2_index_params_id_15(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_ids(connect, table, vectors)
        status = connect.create_index(table, index_params)

        query_id = non_exist_id + len(ids)
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            # assert len(result[0]) == min(len(vectors), top_k)
            # assert result[0][0].distance <= epsilon
            # assert check_result(result[0], query_id)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()


    # add auto flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_l2_index_params_id_16(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_ids(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush_ids(connect, table, vectors)
        status = connect.create_index(table, index_params)

        query_id = non_exist_id + len(ids)
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            # assert len(result[0]) == min(len(vectors), top_k)
            # assert result[0][0].distance <= epsilon
            # assert check_result(result[0], query_id)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # ------------------------------------------------------------- l2, add auto flush, delete, search ------------------------------------------------------------- #


    # ------------------------------------------------------------- l2, add auto flush, delete, search ------------------------------------------------------------- #
    # auto flush
    def test_search_l2_index_params_1(self, connect, table, get_simple_index_params):
        '''
        target: test basic search fuction, all the search params is corrent, test all index params, and build
        method: search with the given vectors, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        # logging.getLogger().info(result)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()
    
    # auto flush
    def test_search_l2_index_params_2(self, connect, table, get_simple_index_params):
        '''
        target: test basic search fuction, all the search params is corrent, test all index params, and build
        method: search with the given vectors, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = non_exist_id
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        # logging.getLogger().info(result)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            # assert len(result[0]) == 0
            # assert result[0][0].distance <= epsilon
            # assert check_result(result[0], ids[0])
        else:
            assert not status.OK()


    # add auto flush, delete auto flush
    def test_search_l2_index_params_3(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete auto flush
    def test_search_l2_index_params_4(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete manual flush
    def test_search_l2_index_params_5(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_and_flush(connect, table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete manual flush
    def test_search_l2_index_params_6(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_and_flush(connect, table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush
    def test_search_l2_index_params_7(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush
    def test_search_l2_index_params_8(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again auto flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_l2_index_params_9(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        # query_id = ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            # assert self.check_no_result(result[0])
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_l2_index_params_10(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        # query_id = ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()


    def test_base_ops(self, connect, table):
        

        vectors = gen_vectors(small_size, dim)

        def search_and_show(table, top_k, nprobe, query_id):
            status, result = connect.search_by_id(table, top_k, nprobe, query_id)
            for r in result[0][:5]:
                logging.getLogger().info(r)

        index_params = {'index_type':IndexType.FLAT, 'nlist':512}
        logging.getLogger().info(index_params)
        vectors, ids = connect.add_vectors(table, vectors)

        # sleep(4)
        status = connect.create_index(table, index_params)

        query_id = ids[0]
        logging.getLogger().info('query_id: ' + str(query_id))
        top_k = 10
        nprobe = 1

        search_and_show(table, top_k, nprobe, query_id)


    def test_1170(self, connect, table):

        def search_and_show(table, top_k, nprobe, query_id):
            status, result = connect.search_by_id(table, top_k, nprobe, query_id)
            for r in result[0][:5]:
                logging.getLogger().info(r)

        index_params = {'index_type':IndexType.FLAT, 'nlist':512}
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        query_id = ids[0]
        logging.getLogger().info('query_id: ' + str(query_id))
        top_k = 10
        nprobe = 1

        search_and_show(table, top_k, nprobe, query_id)
        
        status = self.delete_data_no_flush(connect, table, [query_id])
        search_and_show(table, top_k, nprobe, query_id)

        # connect.flush([table])
        # search_and_show(table, top_k, nprobe, query_id)

        # vectors, new_ids = self.add_data(connect, table, vectors)
        status, new_ids = connect.add_vectors(table, vectors)
        logging.getLogger().info(status)
        connect.flush([table])
        # sleep(30)
        # status = connect.create_index(table, index_params)
        search_and_show(table, top_k, nprobe, query_id)
        

    # add auto flush, delete no flush, add again auto flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_l2_index_params_11(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        # query_id = ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, non_exist_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_l2_index_params_12(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        # query_id = ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, non_exist_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again auto flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_l2_index_params_13(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        query_id = new_ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            # assert self.check_no_result(result[0])
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_l2_index_params_14(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        query_id = new_ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # ------------------------------------------------------------- l2, add auto flush, delete, search ------------------------------------------------------------- #

    # add to table, auto flush, search table, search partition exist
    
    def test_search_l2_index_params_partition_9(self, connect, table, get_simple_index_params):
        '''
        target: test basic search fuction, all the search params is corrent, test all index params, and build
        method: add vectors into table, search with the given vectors, check the result
        expected: search status ok, and the length of the result is top_k, search table with partition tag return empty
        '''
        index_params = get_simple_index_params
        # index_params = {'nlist': 1024, 'index_type': IndexType.IVF_SQ8}
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        
        assert status.OK()
        assert len(result[0]) == min(len(vectors), top_k)
        assert check_result(result[0], ids[0])
        assert result[0][0].distance <= epsilon
        
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag])
        
        assert status.OK() 
        assert len(result) == 0

    # add to table, auto flush, search partition exist
    def test_search_l2_index_params_partition_1(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag])
        assert status.OK()
        assert len(result) == 0
        

    # add to partition, auto flush, search partition exist
    def test_search_l2_index_params_partition_2(self, connect, table, get_simple_index_params):
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data_partition(connect, table, tag, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag])
        logging.getLogger().info(status)
        logging.getLogger().info(result)
        assert status.OK()
        assert len(result[0]) == min(len(vectors), top_k)
        assert check_result(result[0], query_id)

    # add to table, auto flush, search partition non exist
    def test_search_l2_index_params_partition_3(self, connect, table, get_simple_index_params):
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = non_exist_id
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag])
        assert status.OK()
        assert len(result) == 0


    # # add to partition, auto flush, search partition non exist
    def test_search_l2_index_params_partition_4(self, connect, table, get_simple_index_params):
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data_partition(connect, table, tag, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = non_exist_id
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag])
        assert status.OK()
        assert self.check_no_result(result[0])


    # # add to table, manual flush, search partition exist
    def test_search_l2_index_params_partition_5(self, connect, table, get_simple_index_params):    
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag])
        assert status.OK()
        assert len(result) == 0

    # add to partition, manual flush, search partition exist
    def test_search_l2_index_params_partition_6(self, connect, table, get_simple_index_params):
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data_partition_and_flush(connect, table, tag, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag])
        assert status.OK()
        assert len(result[0]) == min(len(vectors), top_k)
        assert check_result(result[0], query_id)

    # add to table, manual flush, search partition non exist
    def test_search_l2_index_params_partition_7(self, connect, table, get_simple_index_params):
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = non_exist_id
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag])
        assert status.OK()
        assert len(result) == 0

    # add to partition, manual flush, search partition non exist
    def test_search_l2_index_params_partition_8(self, connect, table, get_simple_index_params):
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data_partition_and_flush(connect, table, tag, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = non_exist_id
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag])
        assert status.OK()
        assert self.check_no_result(result[0])

    # add to table, manual flush, search non-existing partition non exist
    def test_search_l2_index_params_partition_15(self, connect, table, get_simple_index_params):
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data_partition_and_flush(connect, table, tag, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = non_exist_id
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=['non_existing_tag'])
        assert status.OK()
        assert len(result) == 0
    
    # add to table, manual flush, search non-existing partition non exist
    def test_search_l2_index_params_partition_14(self, connect, table, get_simple_index_params):
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data_partition_and_flush(connect, table, tag, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=['non_existing_tag'])
        assert status.OK()
        assert len(result) == 0
    
    # add to partition, auto flush, search partition, exist
    def test_search_l2_index_params_partition_13(self, connect, table, get_simple_index_params):
        
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data(connect, partition_name, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag, "new_tag"])
        logging.getLogger().info(result)
        assert status.OK()
        assert len(result[0]) == min(len(vectors), top_k)
        assert check_result(result[0], ids[0])
        assert result[0][0].distance <= epsilon

    # add to partition, auto flush, search partition, exist
    def test_search_l2_index_params_partition_10(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        vectors, ids = self.init_data(connect, partition_name, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=["new_tag"])
        assert status.OK()
        assert len(result) == 0
    
    # add to partition, auto flush, search partition, exist
    def test_search_l2_index_params_partition_11(self, connect, table, get_simple_index_params):
    
        new_tag = "new_tag"
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        new_partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        status = connect.create_partition(table, new_partition_name, new_tag)
        vectors, ids = self.init_data(connect, partition_name, nb=small_size)
        new_vectors, new_ids = self.init_data(connect, new_partition_name, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag, new_tag])
        assert status.OK()
        assert len(result[0]) == min(len(vectors), top_k)
        assert check_result(result[0], ids[0])
        assert result[0][0].distance <= epsilon
        
        query_id = new_ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=[tag, new_tag])
        assert status.OK()
        assert len(result[0]) == min(len(vectors), top_k)
        assert check_result(result[0], new_ids[0])
        assert result[0][0].distance <= epsilon

    # add to partition, auto flush, search partition, exist
    def test_search_l2_index_params_partition_12(self, connect, table, get_simple_index_params):
    
        tag = "atag"
        new_tag = "new_tag"
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        new_partition_name = gen_unique_str()
        status = connect.create_partition(table, partition_name, tag)
        status = connect.create_partition(table, new_partition_name, new_tag)
        vectors, ids = self.init_data(connect, partition_name, nb=small_size)
        new_vectors, new_ids = self.init_data(connect, new_partition_name, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=["(.*)tag"])
        assert status.OK()
        assert len(result[0]) == min(len(vectors), top_k)
        assert check_result(result[0], ids[0])
        assert result[0][0].distance <= epsilon
        
        query_id = new_ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id, partition_tag_array=["new(.*)"])
        assert len(result[0]) == min(len(new_vectors), top_k)
        assert check_result(result[0], new_ids[0])
        assert status.OK()
        assert result[0][0].distance <= epsilon

    # ------------------------------------------------------------- ip, add auto flush, delete, search ------------------------------------------------------------- #
    # add auto flush
    def test_search_ip_index_params_1(self, connect, ip_table, get_simple_index_params):
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        logging.getLogger().info(result)

        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert check_result(result[0], ids[0])
            # assert abs(result[0][0].distance - numpy.inner(numpy.array(query_id[0]), numpy.array(query_id[0]))) <= gen_inaccuracy(result[0][0].distance)
        else:
            assert not status.OK()
    
    # add auto flush
    def test_search_ip_index_params_2(self, connect, ip_table, get_simple_index_params):
        '''
        target: test basic search fuction, all the search params is corrent, test all index params, and build
        method: search with the given vectors, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)
        query_id = non_exist_id
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        logging.getLogger().info(result)

        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            # assert check_result(result[0], ids[0])
            assert self.check_no_result(result[0])

            # assert abs(result[0][0].distance - numpy.inner(numpy.array(query_id[0]), numpy.array(query_id[0]))) <= gen_inaccuracy(result[0][0].distance)
        else:
            assert not status.OK()
    
    # add auto flush, delete no flush
    def test_search_ip_index_params_3(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, ip_table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush, non exist
    def test_search_ip_index_params_4(self, connect, ip_table, get_simple_index_params):
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, ip_table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(ip_table, top_k, nprobe, non_exist_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete manual flush
    def test_search_ip_index_params_5(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_and_flush(connect, ip_table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete manual flush
    def test_search_ip_index_params_6(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_and_flush(connect, ip_table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete auto flush
    def test_search_ip_index_params_7(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data(connect, ip_table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            # assert len(result[0]) == min(len(vectors), top_k)
            # assert result[0][0].distance <= epsilon
            # assert check_result(result[0], ids[0])
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush
    def test_search_ip_index_params_8(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data(connect, ip_table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again auto flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_ip_index_params_9(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, ip_table, [query_id])
        status = self.delete_data(connect, ip_table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data(connect, ip_table, vectors)
        status = connect.create_index(ip_table, index_params)
        # # logging.getLogger().info(new_ids)
        # logging.getLogger().info(connect.count_ip_table(ip_table))

        # query_id = ids[0]
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            # assert self.check_no_result(result[0])
            assert check_result(result[0], query_id)

        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_ip_index_params_10(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, ip_table, [query_id])
        status = self.delete_data(connect, ip_table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush(connect, ip_table, vectors)
        status = connect.create_index(ip_table, index_params)
        # # logging.getLogger().info(new_ids)
        # logging.getLogger().info(connect.count_ip_table(ip_table))

        # query_id = ids[0]
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again auto flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_ip_index_params_11(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, ip_table, [query_id])
        status = self.delete_data(connect, ip_table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data(connect, ip_table, vectors)
        status = connect.create_index(ip_table, index_params)
        # # logging.getLogger().info(new_ids)
        # logging.getLogger().info(connect.count_ip_table(ip_table))

        # query_id = ids[0]
        status, result = connect.search_by_id(ip_table, top_k, nprobe, non_exist_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_ip_index_params_12(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, ip_table, [query_id])
        status = self.delete_data(connect, ip_table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush(connect, ip_table, vectors)
        status = connect.create_index(ip_table, index_params)
        # # logging.getLogger().info(new_ids)
        # logging.getLogger().info(connect.count_ip_table(ip_table))

        # query_id = ids[0]
        status, result = connect.search_by_id(ip_table, top_k, nprobe, non_exist_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            # assert check_result(result[0], query_id)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again auto flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_ip_index_params_13(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, ip_table, [query_id])
        status = self.delete_data(connect, ip_table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data(connect, ip_table, vectors)
        status = connect.create_index(ip_table, index_params)
        # # logging.getLogger().info(new_ids)
        # logging.getLogger().info(connect.count_ip_table(ip_table))

        query_id = new_ids[0]
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            # assert self.check_no_result(result[0])
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # add auto flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_ip_index_params_14(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, ip_table, [query_id])
        status = self.delete_data(connect, ip_table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush(connect, ip_table, vectors)
        status = connect.create_index(ip_table, index_params)
        # # logging.getLogger().info(new_ids)
        # # logging.getLogger().info(connect.count_ip_table(ip_table))

        query_id = new_ids[0]
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            # assert self.check_no_result(result[0])
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # ------------------------------------------------------------- ip, add auto flush, delete, search ------------------------------------------------------------- #


    # ------------------------------------------------------------- l2, add manual flush, delete, search ------------------------------------------------------------- #
    # manual flush
    def test_search_m_l2_index_params_1(self, connect, table, get_simple_index_params):
        '''
        target: test basic search fuction, all the search params is corrent, test all index params, and build
        method: search with the given vectors, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_no_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)

            for r in result[0][:5]:
                logging.getLogger().info(r)
            # assert self.check_no_result(result[0])
        else:
            assert not status.OK()
    
    # manual flush
    def test_search_m_l2_index_params_2(self, connect, table, get_simple_index_params):
        '''
        target: test basic search fuction, all the search params is corrent, test all index params, and build
        method: search with the given vectors, check the result
        expected: search status ok, and the length of the result is top_k
        '''
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_no_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = non_exist_id
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        # logging.getLogger().info(result)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            # assert len(result[0]) == 0
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()
   

    # add manual flush, delete manual flush
    def test_search_m_l2_index_params_5(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_and_flush(connect, table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add manual flush, delete manual flush
    def test_search_m_l2_index_params_6(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_and_flush(connect, table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add manual flush, delete no flush
    def test_search_m_l2_index_params_7(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert len(result[0]) == min(len(vectors), top_k)
            assert result[0][0].distance <= epsilon
            assert check_result(result[0], ids[0])
        else:
            assert not status.OK()

    # add manual flush, delete no flush
    def test_search_m_l2_index_params_8(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        query_id = non_exist_id
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add manual flush, delete no flush, add again manual flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_m_l2_index_params_9(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        status = self.delete_data_no_flush(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        # query_id = ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            # assert self.check_no_result(result[0])
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # add manual flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_m_l2_index_params_10(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        # query_id = ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add manual flush, delete no flush, add again manual flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_m_l2_index_params_11(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        # query_id = ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, non_exist_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add manual flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_m_l2_index_params_12(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        # query_id = ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, non_exist_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            assert self.check_no_result(result[0])
        else:
            assert not status.OK()

    # add manual flush, delete no flush, add again manual flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_m_l2_index_params_13(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        query_id = new_ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            # assert self.check_no_result(result[0])
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # add manual flush, delete no flush, add again no flush
    # TODO: https://github.com/milvus-io/milvus/issues/1170
    def test_search_m_l2_index_params_14(self, connect, table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        vectors, ids = self.init_data_and_flush(connect, table, nb=small_size)
        status = connect.create_index(table, index_params)

        # logging.getLogger().info(ids)

        query_id = ids[0]
        top_k = 10
        nprobe = 1

        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        logging.getLogger().info(status)
        assert status.OK()
        for r in result[0][:5]:
            logging.getLogger().info(r)

        # status = self.delete_data_no_flush(connect, table, [query_id])
        status = self.delete_data(connect, table, [query_id])
        assert status.OK()

        vectors, new_ids = self.add_data_no_flush(connect, table, vectors)
        status = connect.create_index(table, index_params)
        # # logging.getLogger().info(new_ids)
        logging.getLogger().info(connect.count_table(table))

        query_id = new_ids[0]
        status, result = connect.search_by_id(table, top_k, nprobe, query_id)
        if top_k <= 1024:
            assert status.OK()
            for r in result[0][:5]:
                logging.getLogger().info(r)
            # assert self.check_no_result(result[0])
            assert check_result(result[0], query_id)
        else:
            assert not status.OK()

    # ------------------------------------------------------------- l2, add manual flush, delete, search ------------------------------------------------------------- #

    def test_search_ip_index_params_partition(self, connect, ip_table, get_simple_index_params):
        
        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(ip_table, partition_name, tag)
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        status = connect.create_index(ip_table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
        # logging.getLogger().info(result)
        assert status.OK()
        assert len(result[0]) == min(len(vectors), top_k)
        assert check_result(result[0], ids[0])
        
        
        # logging.getLogger().info(str(index_params['index_type']) + '_tsip_1')
        # for i in range(100):
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id, partition_tag_array=[tag])
        # logging.getLogger().info(str(index_params['index_type']) + '_tsip_2')
        # logging.getLogger().info(type(result[0]))
        assert status.OK()
        assert len(result) == 0
        # assert self.check_no_result(result[0])

    def test_search_ip_index_params_partition_1(self, connect, ip_table, get_simple_index_params):

        index_params = get_simple_index_params
        logging.getLogger().info(index_params)
        partition_name = gen_unique_str()
        status = connect.create_partition(ip_table, partition_name, tag)
        vectors, ids = self.init_data(connect, partition_name, nb=small_size)
        status = connect.create_index(ip_table, index_params)
        query_id = ids[0]
        top_k = 10
        nprobe = 1
        status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id, partition_tag_array=[tag])

        assert status.OK()
        assert len(result[0]) == min(len(vectors), top_k)
        assert check_result(result[0], ids[0])

        status, result = connect.search_by_id(partition_name, top_k, nprobe, query_id)
        assert status.OK()
        assert len(result[0]) == min(len(vectors), top_k)
        assert check_result(result[0], ids[0])

    @pytest.mark.level(2)
    def test_search_by_id_without_connect(self, dis_connect, table):
        '''
        target: test search vectors without connection
        method: use dis connected instance, call search method and check if search successfully
        expected: raise exception
        '''
        query_idtors = 123
        top_k = 1
        nprobe = 1
        with pytest.raises(Exception) as e:
            status, ids = dis_connect.search_by_id(table, top_k, nprobe, query_idtors)

    def test_search_table_name_not_existed(self, connect, table):
        '''
        target: search table not existed
        method: search with the random table_name, which is not in db
        expected: status not ok
        '''
        table_name = gen_unique_str("not_existed_table")
        top_k = 1
        nprobe = 1
        query_id = non_exist_id
        status, result = connect.search_by_id(table_name, top_k, nprobe, query_id)
        assert not status.OK()

    def test_search_table_name_None(self, connect, table):
        '''
        target: search table that table name is None
        method: search with the table_name: None
        expected: status not ok
        '''
        table_name = None
        top_k = 1
        nprobe = 1
        query_ids = non_exist_id
        with pytest.raises(Exception) as e: 
            status, result = connect.search_by_id(table_name, top_k, nprobe, query_id)

    # def test_search_distance_l2_flat_index(self, connect, table):
    #     nb = 2
    #     top_k = 1
    #     nprobe = 1
    #     vectors, ids = self.init_data(connect, table, nb=nb)
    #     vs = [[0.50 for i in range(dim)]]
    #     query_ids = ids
    #     distance_0 = numpy.linalg.norm(numpy.array(vs[0]) - numpy.array(vectors[0]))
    #     distance_1 = numpy.linalg.norm(numpy.array(vs[0]) - numpy.array(vectors[1]))
    #     status, result = connect.search_by_id(table, top_k, nprobe, ids[0])
    #     assert abs(numpy.sqrt(result[0][0].distance) - min(distance_0, distance_1)) <= gen_inaccuracy(result[0][0].distance)

    # def test_search_distance_ip_flat_index(self, connect, ip_table):
    #     '''
    #     target: search ip_table, and check the result: distance
    #     method: compare the return distance value with value computed with Inner product
    #     expected: the return distance equals to the computed value
    #     '''
    #     nb = 2
    #     top_k = 1
    #     nprobe = 1
    #     vectors, ids = self.init_data(connect, ip_table, nb=nb)
    #     index_params = {
    #         "index_type": IndexType.FLAT,
    #         "nlist": 16384
    #     }
    #     connect.create_index(ip_table, index_params)
    #     logging.getLogger().info(connect.describe_index(ip_table))
    #     query_ids = [[0.50 for i in range(dim)]]
    #     distance_0 = numpy.inner(numpy.array(query_ids[0]), numpy.array(vectors[0]))
    #     distance_1 = numpy.inner(numpy.array(query_ids[0]), numpy.array(vectors[1]))
    #     status, result = connect.search_by_id(ip_table, top_k, nprobe, query_ids)
    #     assert abs(result[0][0].distance - max(distance_0, distance_1)) <= gen_inaccuracy(result[0][0].distance)

    def test_search_distance_jaccard_flat_index(self, connect, jac_table):
       
        # from scipy.spatial import distance
        top_k = 10
        nprobe = 512
        int_vectors, vectors, ids = self.init_binary_data(connect, jac_table, nb=small_size)
        index_params = {
            "index_type": IndexType.FLAT,
            "nlist": 16384
        }
        connect.create_index(jac_table, index_params)
        logging.getLogger().info(ids[:10])
        # logging.getLogger().info(connect.describe_table(jac_table))
        # logging.getLogger().info(connect.describe_index(jac_table))
        
        # query_id = random.choice(ids)
        query_id = ids[0]
        logging.getLogger().info(query_id)
        status, result = connect.search_by_id(jac_table, top_k, nprobe, query_id)
        logging.getLogger().info(status)
        logging.getLogger().info(result[0])
        # assert abs(result[0][0].distance - min(distance_0, distance_1)) <= epsilon

    def test_search_distance_hamming_flat_index(self, connect, ham_table):
    
        # from scipy.spatial import distance
        top_k = 10
        nprobe = 512
        int_vectors, vectors, ids = self.init_binary_data(connect, ham_table, nb=small_size)
        index_params = {
            "index_type": IndexType.FLAT,
            "nlist": 16384
        }
        connect.create_index(ham_table, index_params)
        logging.getLogger().info(connect.describe_table(ham_table))
        logging.getLogger().info(connect.describe_index(ham_table))
        # query_int_vectors, query_ids, tmp_ids = self.init_binary_data(connect, ham_table, nb=1, insert=False)
        # distance_0 = hamming(query_int_vectors[0], int_vectors[0])
        # distance_1 = hamming(query_int_vectors[0], int_vectors[1])

        query_id = ids[0]
        status, result = connect.search_by_id(ham_table, top_k, nprobe, query_id)
        logging.getLogger().info(status)
        logging.getLogger().info(result)
        # assert abs(result[0][0].distance - min(distance_0, distance_1).astype(float)) <= epsilon

    def test_search_distance_tanimoto_flat_index(self, connect, tanimoto_table):
        
        # from scipy.spatial import distance
        top_k = 10
        nprobe = 512
        int_vectors, vectors, ids = self.init_binary_data(connect, tanimoto_table, nb=small_size)
        index_params = {
            "index_type": IndexType.FLAT,
            "nlist": 16384
        }
        connect.create_index(tanimoto_table, index_params)
        logging.getLogger().info(connect.describe_table(tanimoto_table))
        logging.getLogger().info(connect.describe_index(tanimoto_table))
        # query_int_vectors, query_ids, tmp_ids = self.init_binary_data(connect, tanimoto_table, nb=1, insert=False)
        # distance_0 = tanimoto(query_int_vectors[0], int_vectors[0])
        # distance_1 = tanimoto(query_int_vectors[0], int_vectors[1])

        query_id = ids[0]
        status, result = connect.search_by_id(tanimoto_table, top_k, nprobe, query_id)
        logging.getLogger().info(status)
        logging.getLogger().info(result)
        # assert abs(result[0][0].distance - min(distance_0, distance_1)) <= epsilon

    # def test_search_distance_ip_index_params(self, connect, ip_table, get_index_params):
    #     '''
    #     target: search table, and check the result: distance
    #     method: compare the return distance value with value computed with Inner product
    #     expected: the return distance equals to the computed value
    #     '''
    #     top_k = 2
    #     nprobe = 1
    #     vectors, ids = self.init_data(connect, ip_table, nb=2)
    #     index_params = get_index_params
    #     connect.create_index(ip_table, index_params)
    #     logging.getLogger().info(connect.describe_index(ip_table))
    #     query_ids = [[0.50 for i in range(dim)]]
    #     status, result = connect.search_by_id(ip_table, top_k, nprobe, query_ids)
    #     logging.getLogger().debug(status)
    #     logging.getLogger().debug(result)
    #     distance_0 = numpy.inner(numpy.array(query_ids[0]), numpy.array(vectors[0]))
    #     distance_1 = numpy.inner(numpy.array(query_ids[0]), numpy.array(vectors[1]))
    #     assert abs(result[0][0].distance - max(distance_0, distance_1)) <= gen_inaccuracy(result[0][0].distance)

    # TODO: enable
    # @pytest.mark.repeat(5)
    @pytest.mark.timeout(30)
    def test_search_concurrent(self, connect, table):
        vectors, ids = self.init_data(connect, table, nb=small_size)
        thread_num = 10
        nb = 100
        top_k = 10
        threads = []
        # query_ids = vectors[nb//2:nb]
        def search(query_id):
            status, result = connect.search_by_id(table, top_k, query_id)
            ids = [x.id for x in result[0]]
            assert query_id in ids
            assert result[0][0].distance == 0.0

        for i in range(thread_num):
            query_id = random.choice(vectors)
            x = threading.Thread(target=search, args=(query_id))
            threads.append(x)
            x.start()
        for th in threads:
            th.join()

    # TODO: enable
    @pytest.mark.timeout(30)
    def test_search_concurrent_multiprocessing(self, args):
        nb = 100
        top_k = 10
        process_num = 4
        processes = []
        table = gen_unique_str("test_search_concurrent_multiprocessing")
        uri = "tcp://%s:%s" % (args["ip"], args["port"])
       
        param = {'table_name': table,
            'dimension': dim,
            'index_type': IndexType.FLAT}
        # create table
        milvus = get_milvus()
        milvus.connect(uri=uri)
        milvus.create_table(param)
        vectors, ids = self.init_data(milvus, table, nb=nb)
        
        def search(milvus, query_id):
            status, result = milvus.search_by_id(table, top_k, query_id)
            ids = [x.id for x in result[0]]
            assert query_id in ids
            assert result[0][0].distance == 0.0

        for i in range(process_num):
            milvus = get_milvus()
            milvus.connect(uri=uri)
            query_id = random.choice(vectors)
            p = Process(target=search, args=(milvus, query_id))
            processes.append(p)
            p.start()
            time.sleep(0.2)
        for p in processes:
            p.join()

    def test_search_multi_table_L2(search, args):
        
        num = 10
        top_k = 10
        nprobe = 1
        tables = []
        idx = []
        for i in range(num):
            table = gen_unique_str("test_add_multitable_%d" % i)
            uri = "tcp://%s:%s" % (args["ip"], args["port"])
            param = {'table_name': table,
                     'dimension': dim,
                     'index_file_size': 10,
                     'metric_type': MetricType.L2}
            # create table
            milvus = get_milvus()
            milvus.connect(uri=uri)
            milvus.create_table(param)
            status, ids = milvus.add_vectors(table, vectors)
            assert status.OK()
            assert len(ids) == len(vectors)
            tables.append(table)
            idx.append(random.choice(ids))
            
        time.sleep(6)

        # start query from random table
        for i in range(num):
            table = tables[i]
            status, result = milvus.search_by_id(table, top_k, nprobe, idx[i])
            assert status.OK()
            assert check_result(result[0], idx[i])

    def test_search_multi_table_IP(search, args):
        '''
        target: test search multi tables of IP
        method: add vectors into 10 tables, and search
        expected: search status ok, the length of result
        '''
        num = 10
        top_k = 10
        nprobe = 1
        tables = []
        idx = []
        for i in range(num):
            table = gen_unique_str("test_add_multitable_%d" % i)
            uri = "tcp://%s:%s" % (args["ip"], args["port"])
            param = {'table_name': table,
                     'dimension': dim,
                     'index_file_size': 10,
                     'metric_type': MetricType.IP}
            # create table
            milvus = get_milvus()
            milvus.connect(uri=uri)
            milvus.create_table(param)
            status, ids = milvus.add_vectors(table, vectors)
            assert status.OK()
            assert len(ids) == len(vectors)
            tables.append(table)
            idx.append(random.choice(ids))

        time.sleep(6)
        
        # start query from random table
        for i in range(num):
            table = tables[i]
            status, result = milvus.search_by_id(table, top_k, nprobe, idx[i])
            assert status.OK()
            assert check_result(result[0], idx[i])

"""
******************************************************************
#  The following cases are used to test `search_by_id` function 
#  with invalid table_name top-k / nprobe / query_range
******************************************************************
"""

class TestSearchInvalid(object):
    nlist = 16384
    index_param = {"index_type": IndexType.IVF_SQ8, "nlist": nlist}
    logging.getLogger().info(index_param)

    def init_data(self, connect, table, nb=6000):
        '''
        Generate vectors and add it in table, before search vectors
        '''
        global vectors
        if nb == 6000:
            add_vectors = vectors
        else:  
            add_vectors = gen_vectors(nb, dim)
        status, ids = connect.add_vectors(table, add_vectors)
        sleep(add_interval_time)
        return add_vectors, ids

    """
    Test search table with invalid table names
    """
    @pytest.fixture(
        scope="function",
        params=gen_invalid_table_names()
    )
    def get_table_name(self, request):
        yield request.param

    @pytest.mark.level(2)
    def test_search_with_invalid_tablename(self, connect, get_table_name):
        table_name = get_table_name
        logging.getLogger().info(table_name)
        top_k = 1
        nprobe = 1 
        query_id = non_exist_id
        status, result = connect.search_by_id(table_name, top_k, nprobe, query_id)
        assert not status.OK()

    @pytest.mark.level(1)
    def test_search_with_invalid_tag_format(self, connect, table):
        top_k = 1
        nprobe = 1 
        query_id = non_exist_id
        with pytest.raises(Exception) as e:
            status, result = connect.search_by_id(table_name, top_k, nprobe, query_id, partition_tag_array="tag")

    """
    Test search table with invalid top-k
    """
    @pytest.fixture(
        scope="function",
        params=gen_invalid_top_ks()
    )
    def get_top_k(self, request):
        yield request.param

    @pytest.mark.level(1)
    def test_search_with_invalid_top_k(self, connect, table, get_top_k):
        top_k = get_top_k
        logging.getLogger().info(top_k)
        nprobe = 1
        query_id = non_exist_id
        if isinstance(top_k, int):
            status, result = connect.search_by_id(table, top_k, nprobe, query_id)
            assert not status.OK()
        else:
            with pytest.raises(Exception) as e:
                status, result = connect.search_by_id(table, top_k, nprobe, query_id)

    @pytest.mark.level(2)
    def test_search_with_invalid_top_k_ip(self, connect, ip_table, get_top_k):
    
        top_k = get_top_k
        logging.getLogger().info(top_k)
        nprobe = 1
        query_id = non_exist_id
        if isinstance(top_k, int):
            status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
            assert not status.OK()
        else:
            with pytest.raises(Exception) as e:
                status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
    
    """
    Test search table with invalid nprobe
    """
    @pytest.fixture(
        scope="function",
        params=gen_invalid_nprobes()
    )
    def get_nprobes(self, request):
        yield request.param

    @pytest.mark.level(1)
    def test_search_with_invalid_nprobe(self, connect, table, get_nprobes):
        
        top_k = 1
        nprobe = get_nprobes
        logging.getLogger().info(nprobe)
        query_id = non_exist_id
        if isinstance(nprobe, int):
            status, result = connect.search_by_id(table, top_k, nprobe, query_id)
            assert not status.OK()
        else:
            with pytest.raises(Exception) as e:
                status, result = connect.search_by_id(table, top_k, nprobe, query_id)

    @pytest.mark.level(2)
    def test_search_with_invalid_nprobe_ip(self, connect, ip_table, get_nprobes):
        '''
        target: test search fuction, with the wrong top_k
        method: search with top_k
        expected: raise an error, and the connection is normal
        '''
        top_k = 1
        nprobe = get_nprobes
        logging.getLogger().info(nprobe)
        query_id = non_exist_id
        if isinstance(nprobe, int):
            status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)
            assert not status.OK()
        else:
            with pytest.raises(Exception) as e:
                status, result = connect.search_by_id(ip_table, top_k, nprobe, query_id)

    """
    Test search table with invalid ids
    """
    @pytest.fixture(
        scope="function",
        params=gen_invalid_vector_ids()
    )
    def get_vector_ids(self, request):
        yield request.param

    @pytest.mark.level(1)
    def test_search_flat_with_invalid_vector_id(self, connect, table, get_vector_ids):
        '''
        target: test search fuction, with the wrong query_range
        method: search with query_range
        expected: raise an error, and the connection is normal
        '''
        vectors, ids = self.init_data(connect, table, nb=small_size)
        top_k = 1
        nprobe = 1
        query_id = get_vector_ids
        logging.getLogger().info(query_id)
        with pytest.raises(Exception) as e:
            status, result = connect.search_by_id(table, 1, nprobe, query_id)


    @pytest.mark.level(2)
    def test_search_flat_with_invalid_vector_id_ip(self, connect, ip_table, get_vector_ids):
        
        vectors, ids = self.init_data(connect, ip_table, nb=small_size)
        top_k = 1
        nprobe = 1
        query_id = get_vector_ids
        logging.getLogger().info(query_id)
        with pytest.raises(Exception) as e:
            status, result = connect.search_by_id(ip_table, 1, nprobe, query_id)


def check_result(result, id):
    if len(result) >= 5:
        # return id in [result[0].id, result[1].id, result[2].id, result[3].id, result[4].id]
        return id in [x.id for x in result[:5]]
    else:
        return id in (i.id for i in result)