0 unzip the ppdb:

$ cd data/
$ gunzip ppdb-1.0-s-lexical.gz

1 Build docker images:

$ bash build_docker.sh

2 Run docker:

$ bash run_docker.sh

3 Get into docker interactively:

$ docker exec -it qa /bin/bash

4. Run the example:

$ cd /home/py
$ python example.py