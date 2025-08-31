# 1. Prepare Environment

**Step 1**: 
Clone this repository by

``` bash
git clone --recursive git@github.com:wwwwanhonghuang/dance-dynamics.git
```

> `--recursive' is neccessary


**Step 2**: 
prepare environment according document in [env-preparation-main](env-preparation/main.md)

**step 3**:
download an example video.

``` bash
cd /path/to/repository_root/
wget -O asset/dance1.mp4 "https://www.dropbox.com/scl/fi/c1pahr3g8pg6hvv8o40lj/dance1.mp4?rlkey=nhlsqx3olqh7cttozvg4grfww&st=9d1veax6&dl=1"
```

**step 4**:
In `/path/to/repository_root/`

``` bash
make make_project_dance1
```

**step 5**:
``` bash
cd /path/to/repository_root
cd projects/dance1
make run_openface
```

**step 6**: capture posees.


