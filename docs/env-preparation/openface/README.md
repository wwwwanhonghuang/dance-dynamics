## Build OpenFace from source

### Build OpenCV from source

1. Clone and prepare opencv 4.12.0 source and `build` folder
 
``` bash
cd <repository-root>
git clone --recursive https://github.com/TadasBaltrusaitis/OpenFace.git 
cd OpenFace
wget https://github.com/opencv/opencv/archive/4.12.0.zip
sudo unzip 4.12.0.zip
cd opencv-4.12.0
sudo mkdir build
cd build
```

2. prepare dependencies

- install `tbb`:
`sudo apt-get install libtbb-dev`


[optional] build tbb 2.0 from source

In `OpenFace/third_parts`:

``` bash
git clone -b 2020_U3 https://github.com/oneapi-src/oneTBB.git tbb-2020
cd tbb-2020
```

patch `build/Makefile.tbb` by appending `-Wno-error=changes-meaning` to the end of 
`CPLUS_FLAGS += $(PIC_KEY) $(DSE_KEY) $(DEFINE_KEY)__TBB_BUILD=1`.
i.e., the original line inside `build/Makefile.tbb` becomes `CPLUS_FLAGS += $(PIC_KEY) $(DSE_KEY) $(DEFINE_KEY)__TBB_BUILD=1 -Wno-error=changes-meaning`


``` bash
make -j$(nproc)
# create tbb install folder in mkdir -p /path/to/OpenFace/third_party/tbb-2020/tbb_install
mkdir -p ./tbb_install/lib
cp build/*_release/*.so* ./tbb_install/lib/
cp -r include ./tbb_install/
```

- install `openblas`

`sudo apt-get install libopenblas-dev`

3. Generate Makefile with `cmake`

For my case
, without tbb
``` bash
 sudo cmake -D CMAKE_BUILD_TYPE=RELEASE   -D CMAKE_INSTALL_PREFIX=/usr/local   -D BUILD_TIFF=ON   -D WITH_TBB=OFF   -D BUILD_opencv_python3=ON   -D PYTHON3_EXECUTABLE=/home/<user>/anaconda3/envs/dance-dynamics/bin/python   -D PYTHON3_INCLUDE_DIR=$(/home/<user>/anaconda3/envs/dance-dynamics/bin/python -c "from sysconfig import get_paths as gp; print(gp()['include'])")   -D PYTHON3_LIBRARY=$(find /home/<user>/anaconda3/envs/dance-dynamics/lib -name 'libpython3.9*.so' | head -n 1) -D BUILD_opencv_python2=OFF  -D PYTHON2_EXECUTABLE="" -D CMAKE_CXX_FLAGS="$CMAKE_CXX_FLAGS -Wno-error=changes-meaning" ..
```


``` bash
cd /path/to/OpenFace/
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build && cd build
cmake .. -DDLIB_USE_CUDA=OFF -DUSE_AVX_INSTRUCTIONS=ON
cmake --build . --config Release
sudo make install
```

4. make
`make -j$(nproc)`


5. build boost 1.59.0

``` bash
cd /path/to/OpenFace/
wget https://boostorg.jfrog.io/artifactory/main/release/1.59.0/source/boost_1_59_0.tar.gz
tar -xf boost_1_59_0.tar.gz
cd boost_1_59_0
./bootstrap.sh
./b2
cd ..
mv ./boost_1_59_0 ~/boost_1_59_0
```

6. build OpenFace

``` bash 

cmake ..   -DBOOST_ROOT=/home/xx/boost_1_59_0   -DBoost_NO_SYSTEM_PATHS=ON   -DBoo
st_INCLUDE_DIR=/home/xx/boost_1_59_0   -DBoost_LIBRARY_DIR_RELEASE=/home/xx/boost_1_59_0/stage/lib   -DBoost_LIBRARY_DIR_DEBUG=/home/xx/boost_1_59_0/stage/lib   -DBoost_USE
_STATIC_LIBS=OFF   -DBoost_USE_MULTITHREADED=ON   -DBoost_USE_STATIC_RUNTIME=OFF

make -j$(nproc)
```


6. prepare models

``` bash
cd /path/to/OpenFace/build/
mkdir -p ./bin/model/patch_experts

```

download '.dat' models from `https://www.dropbox.com/scl/fo/pq55xsw9eabf346vivmqn/AClMzt769mNe8ISrPjL9Bdo?dl=0&e=1&rlkey=7qq9uk66x877ck4nny45qdzn2`

and place them into `/path/to/OpenFace/build/bin/model/patch_experts`

7. Run demo

``` bash
cd /path/to/OpenFace/build/
./bin/FaceLandmarkVidMulti -f ../samples/multi_face.avi
```

the rendered results will store in `/path/to/OpenFace/build/processed`

