from functools import cache
from ultralytics import YOLO
import sys

if len(sys.argv) < 3:
    print("Usage: python your_script.py path_to_model path_to_item")
else:
    argument1 = sys.argv[1]
    print(f"The argument1 you provided is: {argument1}")
    argument2 = sys.argv[2]
    print(f"The argument2 you provided is: {argument2}")

    model = YOLO(argument1)
    results = model(argument2, imgsz=640, save=True) #, stream=True)

    # Process results generator
    # for result in results:
    #     boxes = result.boxes  # Boxes object for bbox outputs
    #     masks = result.masks  # Masks object for segmentation masks outputs
    #     keypoints = result.keypoints  # Keypoints object for pose outputs
    #     probs = result.probs  # Probs object for classification outputs
    #     print(boxes,masks,keypoints,probs)
