import os
import pathlib
import cv2
import numpy as np
from pyzbar import pyzbar

directory = "./MuensterDB800x600gedreht"

for file_name in os.listdir(directory):
    if file_name.endswith(".jpg"):
        path_to_file = os.path.join(directory, file_name)
        print(path_to_file)
        image = cv2.imread(path_to_file, cv2.IMREAD_GRAYSCALE)
        mask_image = np.zeros((image.shape[0], image.shape[1],1),np.uint8)
        mask_name = pathlib.Path(file_name).stem + "_mask.png"
        path_to_mask_file = os.path.join(directory, mask_name)
        
        barcodes = None
        image_center = tuple(np.array(image.shape[1::-1]) / 2)

        for angle in np.arange(0, 180, 5):
            rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
            rotated_image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
            barcodes = pyzbar.decode(rotated_image)

            for barcode in barcodes:
                points = barcode.polygon
                pts = np.array(points, np.int32)
                pts = pts.reshape((-1, 1, 2))

                inv_rot_mat = cv2.getRotationMatrix2D(image_center, -angle, 1.0)
                rotatedpolygon = cv2.transform(pts,inv_rot_mat)

                cv2.fillConvexPoly(mask_image, rotatedpolygon, (255))

        contours,hierarchy = cv2.findContours(mask_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        mask_image = np.zeros((image.shape[0], image.shape[1],1),np.uint8)
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            print(rect[2])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.fillConvexPoly(mask_image, box, (255))

        if len(contours) > 0:
            print(path_to_mask_file)
            cv2.imwrite(path_to_mask_file, mask_image)

        for barcode in barcodes:
            points = barcode.polygon
            print(barcode.data.decode("utf-8") + " - " + barcode.type)

        image = cv2.bitwise_and(image, mask_image)

        test_name = pathlib.Path(file_name).stem + "_test.png"
        path_to_test_file = os.path.join(directory, test_name)
        cv2.imwrite(path_to_test_file, image)

        cv2.imshow(file_name, image)
        cv2.waitKey(100)
        cv2.destroyWindow(file_name)

