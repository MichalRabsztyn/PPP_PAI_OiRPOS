print("Running DetectionTestCrop")

from ultralytics import YOLO
from PIL import Image
import os, sys, config

if len(sys.argv) < 2:
    print("Usage: python your_script.py path_to_model")
else:
    model = sys.argv[1]

print(f"The argument1 you provided is: {model}")
argument2 = config.UPLOADED_FILES_PATH
print(f"The argument2 you provided is: {argument2}")

model = YOLO(model)
results = model(argument2, imgsz=640, save=False)

for pred in results:
    input_image = Image.open(pred.path)
    i = 0
    for box in pred.boxes.xyxy:
        x_min, y_min, x_max, y_max = box.tolist()
        cropped_image = input_image.crop((x_min, y_min, x_max, y_max))
        cropped_image.save(f"{config.PATH_TO_SAVE_CROPPED_IMAGES}{os.path.basename(pred.path)}_{i}.png")
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
