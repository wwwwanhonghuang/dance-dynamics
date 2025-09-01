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

OPENPOSE_SRC_DIR := $(REPOSITORY_ROOT)/openpose

OPENPOSE_CAFFE_SRC_DIR := $(OPENPOSE_SRC_DIR)/3rdparty/caffe
REPOSITORY_LOCAL_LIB_ROOT := $(REPOSITORY_ROOT)/lib

PROTOBUF_INSTALL_DIR := $(REPOSITORY_LOCAL_LIB_ROOT)/install/protobuf

CAFFE_INSTALL_DIR := $(REPOSITORY_LOCAL_LIB_ROOT)/install/caffe


prepare_openpose_repository:
	cd $(REPOSITORY_ROOT) && \
	git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose && \
	cd openpose/ && \
	git submodule update --init --recursive --remote

prepare_opencv_src:
	$(MAKE) $(OPENCV_DIR)

prebuild_openpose:
	cd $(OPENPOSE_SRC_DIR) && \
	rm -rf build && mkdir build && cd build && \
	cmake .. \
		-DCMAKE_BUILD_TYPE=Release \
		-DGPU_MODE=CUDA \
		-DBUILD_PYTHON=ON \
		-DBUILD_CAFFE=ON \
		-DBUILD_EXAMPLES=ON \
		-DUSE_CUDNN=OFF \
		-DDOWNLOAD_BODY_MODEL=ON \
		-DDOWNLOAD_HAND_MODEL=ON \
		-DDOWNLOAD_FACE_MODEL=ON \
		-DCMAKE_CXX_STANDARD=14 \
		-DCMAKE_CXX_STANDARD_REQUIRED=ON \
		-DCMAKE_CXX_EXTENSIONS=OFF \
		-DPROTOBUF_INCLUDE_DIR=/usr/include \
		-DPROTOBUF_LIBRARY=/usr/lib/x86_64-linux-gnu/libprotobuf.so \
		-DProtobuf_PROTOC_EXECUTABLE=/usr/bin/protoc \
		-DCMAKE_CXX_STANDARD=17 \
		-DCMAKE_CXX_STANDARD_REQUIRED=ON \
		-DCMAKE_CXX_EXTENSIONS=OFF \
		-DCUDA_NVCC_FLAGS="-std=c++17" \

build_openpose:
	rm -rf $(OPENPOSE_SRC_DIR)/build && \
	mkdir -p $(OPENPOSE_SRC_DIR)/build && \
	cd $(OPENPOSE_SRC_DIR)/build && \
	cmake .. \
		-DCMAKE_BUILD_TYPE=Release \
		-DOpenCV_DIR=$(REPOSITORY_LOCAL_LIB_ROOT)/opencv \
		-DCaffe_DIR=$(CAFFE_INSTALL_DIR)/lib/cmake/Caffe \
		-DCaffe_INCLUDE_DIRS=$(CAFFE_INSTALL_DIR)/include \
		-DCaffe_LIBS=$(CAFFE_INSTALL_DIR)/lib/libcaffe.so \
		-DPROTOBUF_INCLUDE_DIR=$(PROTOBUF_INSTALL_DIR)/include \
		-DPROTOBUF_LIBRARY=$(PROTOBUF_INSTALL_DIR)/lib/libprotobuf.so \
		-DProtobuf_PROTOC_EXECUTABLE=$(PROTOBUF_INSTALL_DIR)/bin/protoc \
		-DBUILD_PYTHON=ON \
		-DBUILD_EXAMPLES=ON \
		-DUSE_CUDA=ON \
		-DCMAKE_INSTALL_PREFIX=$(REPOSITORY_LOCAL_LIB_ROOT)/install/openpose \
		-DBUILD_CAFFE=OFF && \
	make -j$$(nproc) && \
	make install
	cp -r $(OPENPOSE_SRC_DIR)/models $(REPOSITORY_LOCAL_LIB_ROOT)/install/openpose 



make_dependencies:
	$(MAKE) -C $(REPOSITORY_ROOT)/lib build_protobuf
	$(MAKE) -C $(REPOSITORY_ROOT)/lib build_abseil


build_caffe:
	cd $(OPENPOSE_CAFFE_SRC_DIR) && \
	rm -rf build && mkdir build && cd build && \
	cmake .. \
		-DCMAKE_BUILD_TYPE=Release \
		-DGPU_MODE=CUDA \
		-DBUILD_PYTHON=ON \
		-DBUILD_CAFFE=ON \
		-DBUILD_EXAMPLES=ON \
		-DUSE_CUDNN=OFF \
		-DDOWNLOAD_BODY_MODEL=ON \
		-DDOWNLOAD_HAND_MODEL=ON \
		-DDOWNLOAD_FACE_MODEL=ON \
		-DCMAKE_CXX_STANDARD=14 \
		-DCMAKE_CXX_STANDARD_REQUIRED=ON \
		-DCMAKE_CXX_EXTENSIONS=OFF \
		-DPROTOBUF_INCLUDE_DIR=$(PROTOBUF_INSTALL_DIR)/include \
		-DPROTOBUF_LIBRARY=$(PROTOBUF_INSTALL_DIR)/lib/libprotobuf.so \
		-DProtobuf_PROTOC_EXECUTABLE=$(PROTOBUF_INSTALL_DIR)/bin/protoc \
		\
		-DBOOST_ROOT=$(REPOSITORY_LOCAL_LIB_ROOT)/install/boost \
		-DBoost_NO_SYSTEM_PATHS=ON \
		-DBoost_NO_BOOST_CMAKE=TRUE \
		-DBoost_INCLUDE_DIR=$(REPOSITORY_LOCAL_LIB_ROOT)/install/boost/include \
		-DBoost_LIBRARY_DIR=$(REPOSITORY_LOCAL_LIB_ROOT)/install/boost/lib \
		-DBoost_PYTHON_LIBRARY=$(REPOSITORY_LOCAL_LIB_ROOT)/install/boost/lib/libboost_python39.so \
		-DBoost_PYTHON_INCLUDE_DIR=$(REPOSITORY_LOCAL_LIB_ROOT)/install/boost/include \
		\
		-DCMAKE_CXX_STANDARD=14 \
		-DCMAKE_CXX_STANDARD_REQUIRED=ON \
		-DCUDA_NVCC_FLAGS="-std=c++14" \
		-DCMAKE_INSTALL_PREFIX=$(CAFFE_INSTALL_DIR) && \
	make -j$$(nproc) && \
	make install

