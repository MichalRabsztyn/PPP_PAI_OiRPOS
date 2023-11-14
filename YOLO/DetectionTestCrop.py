print("Running DetectionTestCrop")

from ultralytics import YOLO
from PIL import Image
import os, sys

if len(sys.argv) < 6:
    print("Usage: python your_script.py path_to_model path_to_data path_to_results")
else:
    model = sys.argv[1]
    folder = sys.argv[2]
    resultFolder = sys.argv[3]
    resultsFolder = sys.argv[4]
    resultsName = sys.argv[5]

print(f"The model you provided is: {model}")
print(f"The folder you provided is: {folder}")
print(f"The resultFolder you provided is: {resultFolder}")

model = YOLO(model)
results = model(folder, imgsz=640, save=False, project=resultsFolder, name=resultsName)

for pred in results:
    input_image = Image.open(pred.path)
    i = 0
    for box in pred.boxes.xyxy:
        x_min, y_min, x_max, y_max = box.tolist()
        cropped_image = input_image.crop((x_min, y_min, x_max, y_max))
        cropped_image.save(f"{resultFolder}/{os.path.basename(pred.path)}_{i}.png")
        i+=1

# for pred in results:
#     x_min, y_min, x_max, y_max = pred.boxes.xyxy[0].tolist()
#     cropped_image = input_image.crop((x_min, y_min, x_max, y_max))
#     cropped_image.show()

    # print(pred.boxes)
    # print(pred.boxes.xyxy[0])
    # x1, y1, x2, y2 = map(int, pred[0:4])  # Get the coordinates of the bounding box
    # cropped_image = input_image.crop((x1, y1, x2, y2))  # Crop the image
    # cropped_image.show()  # Display or save the cropped image
