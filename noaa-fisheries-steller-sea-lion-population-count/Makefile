current_dir := $(shell pwd)
data_dir := /home/bchnge/volume/data/noaa-fisheries-steller-sea-lion-population-count/


enter_cuda :
	nvidia-docker run --name ds -it -v $(current_dir):/notebooks -v $(data_dir):/data bchnge/ds

startnb :
	nvidia-docker run -d --name dsnb -it -p 8888:8888 -v $(current_dir):/notebooks -v $(data_dir):/data bchnge/ds /bin/sh  -c "jupyter notebook --allow-root --ip 0.0.0.0"
