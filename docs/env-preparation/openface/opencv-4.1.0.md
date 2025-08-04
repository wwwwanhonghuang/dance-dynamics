git clone --recursive https://github.com/TadasBaltrusaitis/OpenFace.git 
mkdir -p OpenFace/opencv-4.1.0/build
cd OpenFace/opencv-4.1.0/build

Generate Makefile with `cmake`:

For my case:
``` bash
 sudo cmake   -D CMAKE_BUILD_TYPE=RELEASE   -D CMAKE_INSTALL_PREFIX=/usr/local   -D BUILD_TIFF=ON   -D WITH_TBB=ON   -D BUILD_opencv_python3=ON   -D PYTHON3_EXECUTABLE=/home/usayui3939/anaconda3/envs/dance-dynamics/bin/python   -D PYTHON3_INCLUDE_DIR=$(/home/usayui3939/anaconda3/envs/dance-dynamics/bin/python -c "from sysconfig import get_paths as gp; print(gp()['include'])")   -D PYTHON3_LIBRARY=$(find /home/usayui3939/anaconda3/envs/dance-dynamics/lib -name 'libpython3.9*.so' | head -n 1) -D BUILD_opencv_python2=OFF  -D PYTHON2_EXECUTABLE=""  ..
```
edit `opencv-4.1.0/build/3rdparty/ade/ade-0.1.1d/sources/ade/include/ade/typed_graph.hpp`:
And at the top, near other includes, add this line:
`#include <cstdint>`



