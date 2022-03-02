import os
import pathlib
import cv2

directory = "muenster barcodeDB_detection_masks/Detection"

for file_name in os.listdir(directory):
    if file_name.endswith(".png"):
        path_to_file = os.path.join(directory, file_name)
        print(path_to_file)
        image = cv2.imread(path_to_file, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(path_to_file, image)