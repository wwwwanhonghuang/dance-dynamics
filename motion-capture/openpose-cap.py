import sys
import cv2
import os
from openpose import pyopenpose as op  # Make sure PYTHONPATH includes OpenPose build/python
import datetime
from pathlib import Path
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--openpose_model_path", type=str)
parser.add_argument("-i", "--input", default="./data/dance1.mp4", type=str)
parser.add_argument("--frame_save_path", default=None, type=str)

args = parser.parse_args()
openpose_model_path = args.openpose_model_path
input_file = args.input

frame_save_path = args.frame_save_path

if input_file.isdigit():
    use_webcam = True
else:
    use_webcam = False
    
    
if frame_save_path is None:
    if use_webcam:
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        frame_save_path = f'openpose_out_{timestamp}'
    else:
        filepath = Path(input_file)
        frame_save_path = f'openpose_out_{filepath.stem}'
else:
    os.makedirs(frame_save_path, exist_ok=True)

# Set OpenPose params
params = {
    "model_folder": openpose_model_path,
    "model_pose": "BODY_25",
    "hand": True,
    "hand_detector": 0, 
    "hand_scale_number": 6, 
    "hand_scale_range": 0.4,
    "num_gpu": 1, 
    "num_gpu_start": 0,
    "scale_gap": 0.1,
    "scale_number": 1,
    "render_threshold": 0.05,
    "disable_multi_thread": False, 
    "hand_net_resolution": "284x284",
}

# Initialize OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# Load video
cap = cv2.VideoCapture(input_file)
if not use_webcam:
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f'models path: {openpose_model_path}')
frame_id = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame
    
    datum = op.Datum()
    datum.cvInputData = frame

    datums = op.VectorDatum()  # Correct C++ vector wrapper
    datums.append(datum)

    opWrapper.emplaceAndPop(datums)

        
    # Access keypoints
    pose_keypoints = datum.poseKeypoints
    face_keypoints = datum.faceKeypoints
    hand_keypoints = datum.handKeypoints
    np.savez(os.path.join(frame_save_path, f"{frame_id}.npz"), 
             pose_keypoints=pose_keypoints, face_keypoints=face_keypoints, hand_keypoints=hand_keypoints)

    if use_webcam:
        print(f"Frame {frame_id} processed.")
    else:
        print(f'Processed {frame_id + 1} / {total_frames} frames')
        
    frame_id += 1
    
    # Optionally display
    if pose_keypoints is not None:
        cv2.imshow("OpenPose", datum.cvOutputData)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
