# Changelog

Please mark all change in change log and use the issue from GitHub

# Milvus 0.7.0 (TBD)

## Bug
- \#715 - Milvus crash when searching and building index simultaneously using SQ8H
- \#744 - Don't return partition table for show_tables
- \#770 - Server unittest run failed on low-end server
- \#805 - IVFTest.gpu_seal_test unittest failed
- \#831 - Judge branch error in CommonUtil.cpp
- \#977 - Server crash when create tables concurrently
- \#995 - table count set to 0 if no tables found
- \#1010 - improve error message when offset or page_size is equal 0
- \#1022 - check if partition name is legal
- \#1028 - check if table exists when show partitions
- \#1029 - check if table exists when try to delete partition
- \#1066 - optimize http insert and search speed
- \#1067 - Add binary vectors support in http server
- \#1152 - Error log output continuously after server start

## Feature
- \#216 - Add CLI to get server info
- \#343 - Add Opentracing
- \#665 - Support get/set config via CLI
- \#759 - Put C++ sdk out of milvus/core
- \#766 - If partition tag is similar, wrong partition is searched
- \#771 - Add server build commit info interface
- \#788 - Add web server into server module
- \#813 - Add push mode for prometheus monitor
- \#815 - Support MinIO storage
- \#823 - Support binary vector tanimoto/jaccard/hamming metric
- \#910 - Change Milvus c++ standard to c++17
- \#1204 - Add api to get table data information

## Improvement
- \#738 - Use Openblas / lapack from apt install
- \#758 - Enhance config description
- \#791 - Remove Arrow
- \#834 - add cpu mode for built-in Faiss
- \#848 - Add ready-to-use config files to the Milvus repo for enhanced user experince
- \#860 - Remove redundant checks in CacheMgr's constructor
- \#908 - Move "primary_path" and "secondary_path" to storage config
- \#931 - Remove "collector" from config
- \#966 - Update NOTICE.md
- \#1002 - Rename minio to s3 in Storage Config section
- \#1078 - Move 'insert_buffer_size' to Cache Config section
- \#1297 - Hide partition_name parameter, avid user directly access partition table
- \#1310 - Add default partition tag for a table

## Task

# Milvus 0.6.0 (2019-12-07)

## Bug
- \#228 - memory usage increased slowly during searching vectors
- \#246 - Exclude src/external folder from code coverage for jenkin ci
- \#248 - Reside src/external in thirdparty
- \#316 - Some files not merged after vectors added
- \#327 - Search does not use GPU when index type is FLAT
- \#331 - Add exception handle when search fail
- \#340 - Test cases run failed on 0.6.0
- \#353 - Rename config.h.in to version.h.in
- \#374 - sdk_simple return empty result
- \#377 - Create partition success if tag name only contains spaces
- \#397 - sdk_simple return incorrect result
- \#399 - Create partition should be failed if partition tag existed
- \#412 - Message returned is confused when partition created with null partition name
- \#416 - Drop the same partition success repeatally
- \#440 - Query API in customization still uses old version
- \#440 - Server cannot startup with gpu_resource_config.enable=false in GPU version
- \#458 - Index data is not compatible between 0.5 and 0.6
- \#465 - Server hang caused by searching with nsg index
- \#485 - Increase code coverage rate
- \#486 - gpu no usage during index building
- \#497 - CPU-version search performance decreased
- \#504 - The code coverage rate of core/src/scheduler/optimizer is too low
- \#509 - IVF_PQ index build trapped into dead loop caused by invalid params
- \#513 - Unittest DELETE_BY_RANGE sometimes failed
- \#523 - Erase file data from cache once 
