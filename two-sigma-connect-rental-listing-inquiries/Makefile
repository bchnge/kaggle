current_dir := $(shell pwd)
data_dir := /home/bchnge/volume/Data/two-sigma-connect-rental-listing-inquiries

#nvidia-docker run -v $(current_dir):$(current_dir) -w $(current_dir) bchnge/ds

all : get-clusters get-summary build-nn


get-clusters : distances.py
	nvidia-docker run -v $(current_dir):$(current_dir) -v $(data_dir):$(current_dir)/data -w $(current_dir) bchnge/ds python distances.py > clusters.results

get-summary : summary.py clusters.results
	nvidia-docker run -v $(current_dir):$(current_dir) -v $(data_dir):$(current_dir)/data -w $(current_dir) bchnge/ds python summary.py > summary.results

build-nn : some_example.py
	nvidia-docker run -v $(current_dir):$(current_dir) -v $(data_dir):$(current_dir)/data -w $(current_dir) bchnge/ds python some_example.py > nn.result
