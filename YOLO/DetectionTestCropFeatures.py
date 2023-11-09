import glob, os, config

folder_path = config.PATH_TO_SAVE_CROPPED_IMAGES_DOT

# Use glob to get a list of files in the folder (you can specify file extensions)
file_list = glob.glob(os.path.join(folder_path,"*"))

# Iterate over each file in the folder
for file_path in file_list:
    if os.path.isfile(file_path):
        print("File:", file_path)
