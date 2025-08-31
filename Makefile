VIDEO_FILE_PATHS ?=
MAKE_PROJECT_PY := ./make_project.py
PROJECT_NAME :=

REPOSITORY_ROOT ?= $(PWD)
NORMALIZED_REPOSITORY_ROOT := $(shell realpath $(REPOSITORY_ROOT))


PROJECT_ASSET_DIR := ${NORMALIZED_REPOSITORY_ROOT}/projects/${PROJECT_NAME}/asset

make_project:
	@mkdir -p $(PROJECT_ASSET_DIR)
	# Convert each input path to absolute and build quoted list
	@ABS_PATHS=""; \
	VIDEO_ARGS=""; \
	IFS=','; \
	for v in $$VIDEO_FILE_PATHS; do \
	    REAL=$$(realpath "$$v"); \
	    ABS_PATHS="$$ABS_PATHS \"$$REAL\""; \
		VIDEO_ARGS="$$VIDEO_ARGS -f \"$$REAL\""; \
	done; \
	echo "Absolute VIDEO_FILE_PATHS: $$ABS_PATHS"; \
	python $(MAKE_PROJECT_PY) --input_video_files $$VIDEO_FILE_PATHS --out_dir ${NORMALIZED_REPOSITORY_ROOT}/projects/${PROJECT_NAME}; \
	$(MAKE) _generate_project_makefile \
		OUTPUT_FILE=${NORMALIZED_REPOSITORY_ROOT}/projects/${PROJECT_NAME}/Makefile \
		PROJECT_ROOT=${NORMALIZED_REPOSITORY_ROOT}/projects/${PROJECT_NAME} \
		OPENFACE_ROOT=${NORMALIZED_REPOSITORY_ROOT}/OpenFace/build \
		VIDEO_FILE_PATHS="$$ABS_PATHS" \
		MOTION_OUT_DIR=${NORMALIZED_REPOSITORY_ROOT}/projects/${PROJECT_NAME}/motion \
		VIDEO_ARGS="$$VIDEO_ARGS" ; \
	for v in $$VIDEO_FILE_PATHS; do \
	    cp "$$v" "$(PROJECT_ASSET_DIR)/"; \
	done

make_project_dance1:
	$(MAKE) make_project \
		OUT_DIR=$(realpath data/dance_1) \
		VIDEO_FILE_PATHS=asset/dance1.mp4 \
		PROJECT_NAME=dance1


_generate_project_makefile:
	envsubst < ${NORMALIZED_REPOSITORY_ROOT}/templates/project_makefile.mf > $(OUTPUT_FILE)
	@echo "Generated preprocessing configuration at $(OUTPUT_FILE)"
 