print("Running DetectionTestOutliners")

import sys,os,csv,shutil, config
import numpy as np
import matplotlib.pyplot as plt
from cmath import log

# Get the path to the folder
# if len(sys.argv) > 1:
#     folder_path = sys.argv[1]
#     print("Folder path:", folder_path)
# else:
#     print("No folder path provided. Please provide the path to the folder with data and csv folder with scv files.")
#     sys.exit(1)
folder_path = config.PATH_TO_SAVE_CROPPED_IMAGES_DOT
print("Folder path:", folder_path)

# Get the result folder name (optional, default is "results")
# folder_name = "results"  # Specify the folder name you want to create
if len(sys.argv) > 1:
    folder_name = sys.argv[1]
print("Result folder name:", folder_name)

# Get the number threshold (optional, default is 0.7)
# score_threshold = 0.7  # If score is greater than this, the sample is bad and should be deleted
if len(sys.argv) > 2:
    try:
        score_threshold = float(sys.argv[2])
    except ValueError:
        print("Invalid number threshold. Please provide a valid number.")
        sys.exit(1)
score_threshold = float(score_threshold)
print("Number threshold:", score_threshold)

NUM_OF_FEATURES = 25088  # Number of features

samples = []  # List to store samples, each sample has 512 features
histogramsData = []  # Data for each feature's histogram of samples (512 histograms with 32 values each)
histograms = []  # List to store one histogram for each feature
hbos = []  # List to store the score for each sample
outlier_indexes = []  # List of indexes of samples to be deleted
filenamesForSamples = []  # List to store image and CSV filenames, index same as samples (contains string name of image and string name of CSV file)

# Reserve space for each feature's histogram data
for i in range(NUM_OF_FEATURES):
    histogramsData.append([])

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        # Extract the frame number, face part, and face number from the image filename
        # frame = filename.split(".png")[0]
        # face = filename.split(".face_")[-1].split(".png")[0]

        # Generate the corresponding CSV filename
        csv_filename = filename+".csv" #f"{frame}.png{int(face)+1}.csv"

        # Append the image and CSV filenames to the list
        filenamesForSamples.append((filename, csv_filename))

# Iterate over each file in the folder/csv
for filename in os.listdir(os.path.join(folder_path, "csv")):
    if filename.endswith(".csv"):
        # Reserve space for one sample
        samples.append([])

        # For each row in the CSV file, insert the value to the respective histogram and sample
        file_path = os.path.join(folder_path, "csv", filename)
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                samples[len(samples) - 1].append(float(row[0]))
                histogramsData[i].append(float(row[0]))

# Compute histograms for each feature's data
for i, histogramData in enumerate(histogramsData):
    # Compute the histogram
    histogram, binEdges = np.histogram(histogramData, bins='auto')

    # Normalize the bin heights
    normalizedHist = histogram / np.max(histogram)

    # Save histogram
    histograms.append((normalizedHist, binEdges))

def get_bar_height(histogram_tuple, value):
    histogram, bin_edges = histogram_tuple
    bin_width = np.diff(bin_edges)[0]
    bin_index = int((value - bin_edges[0]) / bin_width)

    if bin_index >= len(histogram):
        bin_index = len(histogram) - 1

    bar_height = histogram[bin_index]
    return bar_height

# Calculate scores using HBOS algorithm
for j, sample in enumerate(samples):
    hbos.append(0)
    for i, p in enumerate(sample):
        hbos[j] += log(1.0 / get_bar_height(histograms[i], p)).real

# Find outlier samples based on the score threshold
threshold = np.percentile(hbos, score_threshold * 100)
for i, score in enumerate(hbos):
    if score > threshold:
        outlier_indexes.append(i)

# Copy the outlier images to the result folder
for index in outlier_indexes:
    # Check if the folder already exists
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print("Folder created:", folder_name)

    # copy file
    file_path = os.path.join(folder_path, filenamesForSamples[index][0])
    shutil.copy(file_path, folder_name)

    # Check if the file exists
    # if os.path.exists(file_path):
    #     os.remove(file_path)
    #     print("File deleted:", file_path)
    # else:
    #     print("File does not exist:", file_path)

with open(folder_name+'/results.txt', 'a+') as file:
    for index in outlier_indexes:
        file.write(str(hbos[index]/max(hbos)) + '\n')