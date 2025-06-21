# Prepare Protobuf
For ubuntu system,
``` python
sudo apt-get install libprotobuf-dev protobuf-compiler
```
may work.

If the openpose Makefile generation with CMake cannot find the protobuf library,
try manually specify the path in the cmake-gui.

Alternatively, 
build protobuf manually, manually specify the path in the cmake-gui.

## Build Protobuf from Source
``` bash
git clone https://github.com/protocolbuffers/protobuf.git
cd protobuf
git submodule update --init --recursive 
mkdir build && cd build
cmake -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=/usr/local .. 
make -j$(nproc)
sudo make install
sudo ldconfig
```