import os
import pathlib
import cv2
import numpy as np
from pyzbar import pyzbar

directory = "./Dataset2"

# barcode_scanner = pyzbar.ImageScanner()
# barcode_scanner.parse_config('enable')

for file_name in os.listdir(directory):
    if file_name.endswith(".jpg"):
        path_to_file = os.path.join(directory, file_name)
        print(path_to_file)
        image = cv2.imread(path_to_file, cv2.IMREAD_GRAYSCALE)
        mask_image = np.zeros((image.shape[0], image.shape[1],1),np.uint8)
        mask_name = pathlib.Path(file_name).stem + "_mask.png"
        path_to_mask_file = os.path.join(directory, mask_name)

        # sharpened_image = 2 * image - cv2.GaussianBlur(image, (5, 5), 5)
        # sharpened_image = (sharpened_image * 255).astype(np.uint8)

        # sharpened_image = cv2.Laplacian(image, cv2.CV_16S, 5)
        # sharpened_image = cv2.convertScaleAbs(sharpened_image)

        # sharpened_image = cv2.bilateralFilter(image, 9, 150, 150)

        # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # sharpened_image = cv2.filter2D(image, -1, kernel)

        # Good behaviour!
        # frame = cv2.GaussianBlur(image, (15, 15), 5)
        # frame = cv2.bilateralFilter(image, 9, 150, 150)
        # sharpened_image = cv2.addWeighted(frame, -1, image, 2, 0)

        # image = sharpened_image

        barcodes = None
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        mask_x = image.shape[1]
        mask_y = image.shape[0]
        mask_w = 0
        mask_h = 0

        # mask_points = []

        for angle in np.arange(0, 180, 5):
            rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
            rotated_image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
            barcodes = pyzbar.decode(rotated_image)

            # if len(barcodes) > 0:
            #     image = rotated_image
            #     break

            for barcode in barcodes:
                points = barcode.polygon
                pts = np.array(points, np.int32)
                pts = pts.reshape((-1, 1, 2))

                inv_rot_mat = cv2.getRotationMatrix2D(image_center, -angle, 1.0)
                rotatedpolygon = cv2.transform(pts,inv_rot_mat)

                # cv2.polylines(mask_image, [rotatedpolygon], True, (255), 1)

                cv2.fillConvexPoly(mask_image, rotatedpolygon, (255))

                # x,y,w,h = cv2.boundingRect(rotatedpolygon)
                # cv2.rectangle(mask_image,(x,y),(x+w,y+h),(255),-1)

                # if x < mask_x:
                #     mask_x = x
                # if y < mask_y:
                #     mask_y = y
                # if w > mask_w:
                #     mask_w = w
                # if h > mask_h:
                #     mask_h = h

                # mask_points.append((x,y))
                # mask_points.append((x+w,y+h))

                # cv2.imshow("11111", mask_image)
                # cv2.waitKey(0)
                # cv2.destroyWindow("11111")

            # cv2.imshow(file_name, rotated_image)
            # cv2.waitKey(0)
            # cv2.destroyWindow(file_name)

        # cv2.rectangle(mask_image,(mask_x,mask_y),(mask_x+mask_w,mask_y+mask_h),(255),-1)

        # rect = cv2.minAreaRect(np.array(mask_points))
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)        
        # cv2.fillConvexPoly(mask_image, box, (255))

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

        # box = cv2.boxPoints(rect)
        # print(box)
        
        # print(barcodes)
        # print(len(barcodes))

        for barcode in barcodes:
            # print(barcode)
            # cv2.rectangle(image, (barcode.rect.left, barcode.rect.top), (barcode.rect.left, barcode.rect.top), (0, 255, 0), thickness=3)
            points = barcode.polygon

            # pts = np.array(points, np.int32)
            # pts = pts.reshape((-1, 1, 2))
            # cv2.polylines(image, [pts], True, (0, 255, 0), 3)
            print(barcode.data.decode("utf-8") + " - " + barcode.type)

        image = cv2.bitwise_and(image, mask_image)
        cv2.imshow(file_name, image)
        test_name = pathlib.Path(file_name).stem + "_test.png"
        path_to_test_file = os.path.join(directory, test_name)
        cv2.imwrite(path_to_test_file, image)
        # cv2.imshow("mask", mask_image)
        # cv2.imshow("sharpened_image", sharpened_image)
        cv2.waitKey(100)
        # cv2.destroyWindow("mask")
        # cv2.destroyWindow("sharpened_image")
        cv2.destroyWindow(file_name)

        # cv2.imwrite(path_to_mask_file, mask_image)

        # break
