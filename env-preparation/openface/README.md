## Build OpenFace from source

### Quick Building
``` bash
conda activate dance-dynamics
cd <repository-root>/docs/env-preparation/openface
make build_opencv
make build_openface
```
The makefile utilize find the python root by using `which python`, i.e., find the current python that is in active.

Though utilizing the activating one of Python interpreter should work, alternatively, you may modify `Makefile` under `<repository-root>/docs/env-preparation/openface` and change the `PYTHON_ROOT` to the real Python root of the Python interpreter that you prefer to use.


After building the OpenFace successfully,
download all '.dat' models from `https://www.dropbox.com/scl/fo/pq55xsw9eabf346vivmqn/AClMzt769mNe8ISrPjL9Bdo?dl=0&e=1&rlkey=7qq9uk66x877ck4nny45qdzn2`
and place them into `/path/to/repository_root/OpenFace/build/bin/model/patch_experts`

Run OpenFace demo:

``` bash
cd /path/to/repository_root/motion-capture
make run_openface_demo
```

The output files are in /path/to/repository_root/motion-capture/output
