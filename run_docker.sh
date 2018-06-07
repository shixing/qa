docker run -d --rm\
       --name es\
       -v /Users/xingshi/Workspace/misc/sentinel/qa:/home/ \
       --net=host \
       -p 9200:9200 \
       elasticsearch;

docker run -dit --rm\
       --name qa\
       -v /Users/xingshi/Workspace/misc/sentinel/qa:/home/ \
       --net=host\
       qa /bin/bash;

docker ps

