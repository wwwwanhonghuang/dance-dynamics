> GPU version of Openpose can be more complex to be built. Please refers to [Openpose official instructions](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md) for details. 
> Unexpected errors may happens depends on specific GPU and versions of Cuda/Cudnn, etc.
> We provide the steps for building a GPU version of Openpose here. If it fails, we can consider modify the Makefile in `env-preparation/openpose/Makefile`, to set the `-DGPU_MODE=CUDA` to `-DGPU_MODE=CPU_ONLY`.

``` bash
conda activate dance-dynamics
pip install opencv-python
```

``` bash
cd /path/to/repository_root/env-preparation/openpose
make prepare_openpose_repository
make prebuild_openpose

```

cuDNN support has been disabled during the build due to compatibility issues with the newer cuDNN versions.

The CUDA architecture is automatically detected. If it fails. try modify the `Cuda.cmake` in openpose's 3rdparts/caffe/cmake/ folder, change 
the `86` (which means sm_86 arch.) in follow codes, into the correct one.
``` cmake
  if (NOT CUDA_gpu_detect_output)
    message(STATUS "Automatic GPU detection failed. Building for architectures 86.")
    set(${out_variable} "86" PARENT_SCOPE)
  else ()
```


`/usr/local/cuda/include/crt/math_functions.h` need to be patched to remove `error: exception specification is incompatible with that of previous function "xxxx" ` errors.

Add `noexcept(true);` to the end of each line of problematics function definitions.