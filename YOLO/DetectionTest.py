from functools import cache
from ultralytics import YOLO
import sys

if len(sys.argv) < 5:
    print("Usage: python your_script.py path_to_model path_to_item path_to_save")
else:
    model = sys.argv[1]
    folder = sys.argv[2]
    resultsFolder = sys.argv[3]
    resultsName = sys.argv[4]

print(f"The model you provided is: {model}")
print(f"The folder you provided is: {folder}")
print(f"The results Folder you provided is: {resultsFolder}")
print(f"The results Name you provided is: {resultsName}")

model = YOLO(model)
results = model(folder, imgsz=640, save=True, project=resultsFolder, name=resultsName) #, stream=True)

# Process results generator
# for result in results:
#     boxes = result.boxes  # Boxes object for bbox outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     print(boxes,masks,keypoints,probs)
