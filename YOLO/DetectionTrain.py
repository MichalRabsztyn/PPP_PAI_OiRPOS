from functools import cache
from ultralytics import YOLO
import sys

argument = "yolov8n.pt"

if len(sys.argv) < 2:
    print("Usage: python your_script.py path_to_model | no path then use yolov8n.pt")
else:
    # Get a model path
    argument = sys.argv[1]
    print(f"The argument you provided is: {argument}")

# Load a mode
model = YOLO(argument)  # load a pretrained model (recommended for training)

# Use the model
model.train(data="data.yaml", epochs=5, imgsz=640, workers=0, batch=-1, cache=True, device='0')  # train the model
# metrics = model.val()  # evaluate model performance on the validation set
# results = model("valid/images/000000_jpg.rf.ac8509fb8d98bc79b466f61eb2f04c26.jpg")  # predict on an image
# path = model.export(format="onnx")  # export the model to ONNX format