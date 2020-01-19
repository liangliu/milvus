# docker run --gpus all -d -p 19122:19121 registry.zilliz.com/milvus/engine:PR-956-gpu-centos7-release
# docker run --gpus all -d -p 19122:19121 -p 19530:19530 registry.zilliz.com/milvus/engine:master-gpu-centos7-release
# docker run --gpus all -d -p 19121:19121 registry.zilliz.com/milvus/engine:PR-1073-gpu-centos7-release
# name='PR-1073-cpu-ubuntu18.04-release'
# name='PR-1073-gpu-centos7-release'
name='PR-1096-gpu-centos7-release'

docker ps | grep ${name} | awk '{print $1}' | xargs docker stop 
docker run --gpus all -d -p 19121:19121 registry.zilliz.com/milvus/engine:${name}

# [[0.1,0,0.1,0.1, '0.01'], [0.1,0,0.1,0.1, 0.56]]