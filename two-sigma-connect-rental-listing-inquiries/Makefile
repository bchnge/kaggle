current_dir := $(shell pwd)
data_dir := /home/bchnge/volume/Data/two-sigma-connect-rental-listing-inquiries

#nvidia-docker run -v $(current_dir):$(current_dir) -w $(current_dir) bchnge/ds

all : get-clusters get-summary build-nn

start-nb :
	nvidia-docker run -d -it -p 8888:8888 -v $(current_dir)/notebooks:$(current_dir)/notebooks -w $(current_dir)/notebooks bchnge/ds /bin/sh -c "jupyter notebook"

get-clusters : scripts/distances.py
	nvidia-docker run -v $(current_dir):$(current_dir) -v $(data_dir):$(current_dir)/data -w $(current_dir) bchnge/ds python scripts/distances.py > results/clusters.results

get-summary : scripts/summary.py
	nvidia-docker run -v $(current_dir):$(current_dir) -v $(data_dir):$(current_dir)/data -w $(current_dir) bchnge/ds python scripts/summary.py > results/summary.results

build-nn : scripts/some_example.py
	nvidia-docker run -v $(current_dir):$(current_dir) -v $(data_dir):$(current_dir)/data -w $(current_dir) bchnge/ds python scripts/some_example.py > results/nn.result



