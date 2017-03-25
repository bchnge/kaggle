current_dir := $(shell pwd)

#nvidia-docker run -v $(current_dir):$(current_dir) -w $(current_dir) bchnge/ds

all : get-clusters get-summary build-nn

get-clusters : distances.py
	nvidia-docker run -v $(current_dir):$(current_dir) -w $(current_dir) bchnge/ds python distances.py > clusters.results

get-summary : summary.py clusters.results
	nvidia-docker run -v $(current_dir):$(current_dir) -w $(current_dir) bchnge/ds python summary.py > summary.results

build-nn : some_example.py
	nvidia-docker run -v $(current_dir):$(current_dir) -w $(current_dir) bchnge/ds python some_example.py > nn.result
