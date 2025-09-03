# Ask Python directly
ACTIVATED_PYTHON_BIN := $(shell which python)
PYTHON_VERSION := $(shell $(ACTIVATED_PYTHON_BIN) -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')")
PYTHON_INCLUDE := $(shell $(ACTIVATED_PYTHON_BIN) -c "import sysconfig; print(sysconfig.get_path('include'))")
PYTHON_LIBDIR  := $(shell $(ACTIVATED_PYTHON_BIN) -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))")

REPOSITORY_ROOT := $(realpath ..)
REPOSITORY_LOCAL_LIB_ROOT := $(REPOSITORY_ROOT)/lib/
OPENCV_VERSION := 4.12.0

# Python include & library paths
PYTHON3_INCLUDE_DIR := $(shell python -c "from sysconfig import get_paths as gp; print(gp()['include'])")
PYTHON3_LIBRARY := $(shell find $(PYTHON_ROOT)/lib -name 'libpython3.9*.so' | head -n 1)
PROTOBUF_INSTALL_DIR := $(REPOSITORY_LOCAL_LIB_ROOT)/install/protobuf


all: install_conda_dependencies build_abseil build_protobuf build_opencv

install_conda_dependencies:
	conda install -c conda-forge libstdcxx-ng --update-deps

# Clone Abseil source
prepare_abseil_src:
	@mkdir -p $(REPOSITORY_LOCAL_LIB_ROOT)
	if [ ! -d "$(REPOSITORY_LOCAL_LIB_ROOT)/abseil-cpp" ]; then \
		git clone --recursive https://github.com/abseil/abseil-cpp.git $(REPOSITORY_LOCAL_LIB_ROOT)/abseil-cpp; \
	else \
		echo "Abseil source already exists."; \
	fi

# Build Abseil library
build_abseil: prepare_abseil_src
	@mkdir -p $(REPOSITORY_LOCAL_LIB_ROOT)/abseil-cpp/build
	cd $(REPOSITORY_LOCAL_LIB_ROOT)/abseil-cpp/build && \
	cmake -DCMAKE_POSITION_INDEPENDENT_CODE=ON .. && \
	make -j$$(nproc)

build_protobuf:
	if [ ! -d "$(REPOSITORY_LOCAL_LIB_ROOT)/protobuf" ]; then \
		git clone -b v3.21.12 https://github.com/protocolbuffers/protobuf.git $(REPOSITORY_LOCAL_LIB_ROOT)/protobuf; \
	fi
	cd $(REPOSITORY_LOCAL_LIB_ROOT)/protobuf && \
	git submodule update --init --recursive && \
	./autogen.sh && \
	./configure --prefix=$(PROTOBUF_INSTALL_DIR) && \
	make -j$$(nproc) && \
	make install

build_opencv:
	mkdir -p $(REPOSITORY_LOCAL_LIB_ROOT)
	if [ ! -f "$(REPOSITORY_LOCAL_LIB_ROOT)/opencv.zip" ]; then \
		wget https://github.com/opencv/opencv/archive/$(OPENCV_VERSION).zip -O $(REPOSITORY_LOCAL_LIB_ROOT)/opencv.zip; \
	fi
	if [ ! -d "$(REPOSITORY_LOCAL_LIB_ROOT)/opencv-$(OPENCV_VERSION)" ]; then \
		unzip -q $(REPOSITORY_LOCAL_LIB_ROOT)/opencv.zip -d $(REPOSITORY_LOCAL_LIB_ROOT); \
	fi
	cd $(REPOSITORY_LOCAL_LIB_ROOT)/opencv-$(OPENCV_VERSION) && \
	mkdir -p build && cd build && \
	cmake .. \
		-DCMAKE_BUILD_TYPE=RELEASE \
		-DCMAKE_INSTALL_PREFIX=$(REPOSITORY_LOCAL_LIB_ROOT)/install/opencv \
		-DBUILD_TIFF=ON \
		-DWITH_TBB=OFF \
		-DBUILD_opencv_python3=ON \
		-DPYTHON3_EXECUTABLE=$(PYTHON_ROOT)/bin/python \
		-DPYTHON3_INCLUDE_DIR=$(PYTHON3_INCLUDE_DIR) \
		-DPYTHON3_LIBRARY=$(PYTHON3_LIBRARY) \
		-DBUILD_opencv_python2=OFF \
		-DPYTHON2_EXECUTABLE="" \
		-DCMAKE_CXX_FLAGS="-Wno-error=changes-meaning" && \
	make -j$$(nproc) && \
	make install

build_boost:
	cd ${REPOSITORY_LOCAL_LIB_ROOT} && \
	if [ ! -d "boost" ]; then \
		git clone --recursive https://github.com/boostorg/boost.git ; \
	fi && \
	cd boost && \
	rm -rf bin.v2 stage && \
	git pull && git submodule update --init --recursive && \
	./bootstrap.sh --prefix=${REPOSITORY_LOCAL_LIB_ROOT}/install/boost \
		--with-python=$(ACTIVATED_PYTHON_BIN)  \
		--with-libraries=python,system,thread,filesystem && \
	./b2 -j$$(nproc) \
		--with-system \
		python=$(shell python -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')") \
		include=${PYTHON3_INCLUDE_DIR} \
		library-path=${PYTHON_LIBDIR} \
		link=shared threading=multi runtime-link=shared install

