print("Running DetectionTestFeatures")

from ultralytics import YOLO
from PIL import Image
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import glob, os, sys, config, csv, numpy as np

folder_path = config.PATH_TO_SAVE_CROPPED_IMAGES_DOT
csv_file_path = config.PATH_TO_CSV_FILES

# Use glob to get a list of files in the folder (you can specify file extensions)
file_list = glob.glob(os.path.join(folder_path,"*"))
model = VGG16(weights='imagenet', include_top=False)
# model.summary()

# Iterate over each file in the folder
for file_path in file_list:
    if os.path.isfile(file_path):
        print("File To Find Features:", file_path)
        img_path = file_path
        img = image.load_img(img_path, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)

        # Predict features
        vgg16_feature = model.predict(img_data)

        # Print the shape of the features
        # print("Shape of VGG16 features:", vgg16_feature.shape)

        # Write header to the CSV file
        csv_path = os.path.join(csv_file_path,os.path.basename(img_path)+".csv")
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write each feature in a new row
            for feature in vgg16_feature.flatten():
                writer.writerow([feature])
        print("New Features Saved to File:",csv_path)

# Print the features
# print("VGG16 features:")
# for feature in vgg16_feature.flatten():
#     print(feature)

# if len(sys.argv) < 3:
#     print("Usage: python your_script.py path_to_model path_to_item")
# else:
#     argument1 = sys.argv[1]
#     print(f"The argument1 you provided is: {argument1}")
#     argument2 = sys.argv[2]
#     print(f"The argument2 you provided is: {argument2}")

# model = YOLO(argument1)
# results = model(argument2, imgsz=640, save=False)

# for pred in results:
#     input_image = Image.open(pred.path)
#     i = 0
#     for box in pred.boxes.xyxy:
#         x_min, y_min, x_max, y_max = box.tolist()
#         cropped_image = input_image.crop((x_min, y_min, x_max, y_max))
#         cropped_image.save(f"{folder_path}{os.path.basename(pred.path)}_{i}.jpg")
#         i+=1
