ACTIVATED_PYTHON_BIN := $(shell which python)
PYTHON_ROOT := $(realpath $(ACTIVATED_PYTHON_BIN)/../..)
REPOSITORY_ROOT = $(realpath ../..)
OPENCV_VERSION := 4.12.0
OPENCV_DIR := $(REPOSITORY_ROOT)/OpenFace/opencv-$(OPENCV_VERSION)
OPENCV_ZIP := $(REPOSITORY_ROOT)/OpenFace/$(OPENCV_VERSION).zip
PYTHON3_INCLUDE_DIR := $(shell $(PYTHON_ROOT)/bin/python -c "from sysconfig import get_paths as gp; print(gp()['include'])")
PYTHON3_LIBRARY := $(shell find $(PYTHON_ROOT)/lib -name 'libpython3.9*.so' | head -n 1)
BOOST_ROOT := $(REPOSITORY_ROOT)/OpenFace/boost_1_59_0
BOOST_ZIP := boost_1_59_0.tar.gz
BOOST_DIR := $(REPOSITORY_ROOT)/OpenFace/boost_1_59_0
OPENFACE_ROOT := $(REPOSITORY_ROOT)/OpenFace/build


prepare_open_face_repository:
	cd $(REPOSITORY_ROOT) && \
	git clone --recursive https://github.com/TadasBaltrusaitis/OpenFace.git 

prepare_opencv_src:
	$(MAKE) $(OPENCV_DIR)

build_opencv: $(OPENCV_DIR)
	cd $(OPENCV_DIR) && \
	sudo rm -rf build && \
	sudo mkdir -p build && \
	cd build && \
	sudo apt-get install libva-dev ccache libavif-dev libopenjp2-7-dev && \
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
	sudo make -j$$(nproc)

build_boost: $(BOOST_DIR)
	cd $(REPOSITORY_ROOT)/OpenFace/boost_1_59_0 && \
	./bootstrap.sh --with-toolset=gcc \
    	cflags="-std=gnu89 -Wno-implicit-function-declaration -Wno-error" \
    	cxxflags="-std=gnu++98 -Wno-error"  && \
	./b2 toolset=gcc

build_openface:
	sudo mkdir -p $(REPOSITORY_ROOT)/OpenFace/build && \
	cd $(REPOSITORY_ROOT)/OpenFace/build && \
	sudo apt-get install libdlib-dev && \
	sudo cmake ..   \
		-DBoost_USE_STATIC_LIBS=OFF   \
		-DBoost_USE_MULTITHREADED=ON   \
		-DBoost_USE_STATIC_RUNTIME=OFF && \
	sudo make -j$(nproc)
	cp -r $(REPOSITORY_ROOT)/OpenFace/lib/3rdParty/OpenCV/classifiers $(REPOSITORY_ROOT)/OpenFace/build



$(OPENCV_DIR):
	cd $(REPOSITORY_ROOT)/OpenFace && \
	wget -nc https://github.com/opencv/opencv/archive/$(OPENCV_VERSION).zip -O $(OPENCV_ZIP) && \
	unzip -n $(OPENCV_ZIP)

$(BOOST_DIR):
	cd $(REPOSITORY_ROOT)/OpenFace && \
	wget -nc https://archives.boost.io/release/1.59.0/source/boost_1_59_0.tar.gz -O $(BOOST_ZIP) && \
	tar -xf $(BOOST_ZIP);

