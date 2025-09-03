1. create a new virtual environment (we use conda):

``` bash
conda create -n dance-dynamics python=3.9
conda activate dance-dynamics
```

2. Build dependencies

``` bash
cd /path/to/repository_root/lib/
make -j
```

3. Build OpenFace (see [openface](./openface/README.md))

3. Build Openpose (see [openpose](./openpose/README.md))
