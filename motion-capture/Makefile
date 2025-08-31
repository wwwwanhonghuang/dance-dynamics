OPENFACE_ROOT := $(realpath ../OpenFace/build)
SAMPLES_DIR := $(realpath ../OpenFace/samples)
OUT_DIR ?= $(shell pwd)/output

VIDEO_FILE_PATH ?= "$(SAMPLES_DIR)/multi_face.avi"

run_openface_demo:
	mkdir -p $(OUT_DIR)
	@echo "OUT_DIR=$(OUT_DIR)"
	cd $(OPENFACE_ROOT) && \
	./bin/FaceLandmarkVidMulti -f "$(SAMPLES_DIR)/multi_face.avi" -out_dir $(OUT_DIR)

