PYTHON_ROOT = /home/usayui3939/anaconda3/envs/dance-dynamics
REPOSITORY_ROOT = $(realpath ../../..)
OPENCV_VERSION := 4.12.0
OPENCV_DIR := $(REPOSITORY_ROOT)/OpenFace/opencv-$(OPENCV_VERSION)
OPENCV_ZIP := $(REPOSITORY_ROOT)/OpenFace/$(OPENCV_VERSION).zip
PYTHON3_INCLUDE_DIR := $(shell $(PYTHON_ROOT)/bin/python -c "from sysconfig import get_paths as gp; print(gp()['include'])")
PYTHON3_LIBRARY := $(shell find $(PYTHON_ROOT)/lib -name 'libpython3.9*.so' | head -n 1)


prepare_open_face_repository:
	cd $(REPOSITORY_ROOT) && \
	git clone --recursive https://github.com/TadasBaltrusaitis/OpenFace.git 

prepare_opencv_src:
	$(MAKE) $(OPENCV_DIR)

build_opencv: $(OPENCV_DIR)
	cd $(OPENCV_DIR) && \
	mkdir -p build && \
	cd build && \
	sudo cmake .. \
		-D CMAKE_BUILD_TYPE=RELEASE \
		-D CMAKE_INSTALL_PREFIX=/usr/local \
		-D BUILD_TIFF=ON \
		-D WITH_TBB=OFF \
		-D BUILD_opencv_python3=ON \
		-D PYTHON3_EXECUTABLE=$(PYTHON_ROOT)/bin/python \
		-D PYTHON3_INCLUDE_DIR=$(PYTHON3_INCLUDE_DIR) \
		-D PYTHON3_LIBRARY=$(PYTHON3_LIBRARY) \
		-D BUILD_opencv_python2=OFF \
		-D PYTHON2_EXECUTABLE="" \
		-D CMAKE_CXX_FLAGS="-Wno-error=changes-meaning" && \
	make -j$$(nproc)


$(OPENCV_DIR):
	cd $(REPOSITORY_ROOT)/OpenFace && \
	wget -nc https://github.com/opencv/opencv/archive/$(OPENCV_VERSION).zip -O $(OPENCV_ZIP) && \
	unzip -n $(OPENCV_ZIP)