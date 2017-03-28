current_dir := $(shell pwd)
data_dir := /home/bchnge/volume/Data/two-sigma-connect-rental-listing-inquiries

#nvidia-docker run -v $(current_dir):$(current_dir) -w $(current_dir) bchnge/ds

all : get-clusters get-summary build-nn

start-nb :
	nvidia-docker run -d --name dsnb -it -p 8888:8888 -v $(current_dir)/src:$(current_dir)/src -v $(current_dir)/notebooks:$(current_dir)/notebooks -v $(data_dir):$(current_dir)/data -w $(current_dir)/notebooks bchnge/ds /bin/sh -c "jupyter notebook"

stop-nb :
	nvidia-docker rm -f  dsnb

get-clusters : scripts/distances.py
	nvidia-docker run -v $(current_dir):$(current_dir) -v $(data_dir):$(current_dir)/data -w $(current_dir) bchnge/ds python scripts/distances.py > logs/clusters.log

get-summary : scripts/summary.py
	nvidia-docker run -v $(current_dir):$(current_dir) -v $(data_dir):$(current_dir)/data -w $(current_dir) bchnge/ds python scripts/summary.py > logs/summary.log

build-nn : scripts/some_example.py
	nvidia-docker run -v $(current_dir):$(current_dir) -v $(data_dir):$(current_dir)/data -w $(current_dir) bchnge/ds python scripts/some_example.py > logs/nn.log

clear :
	sudo rm features/* logs/* 
