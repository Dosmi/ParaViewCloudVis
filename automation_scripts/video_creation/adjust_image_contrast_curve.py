import cv2
import numpy as np
import os
from os import listdir

# points of the colour-correction curve
# in this example y = f(x)
# so f(0) = 0, f(127) = 50 f(255) = 255
lut_in = [0, 127, 255]
lut_out = [0, 50, 255]

# get the path/directory
folder_dir = "."
for frame_img in os.listdir(folder_dir):
    # check if the image ends with png
    if (frame_img.endswith(".png")):
        print(frame_img)

        image = cv2.imread(frame_img)

        lut_8u = np.interp(np.arange(0, 256), lut_in, lut_out).astype(np.double)
        image_contrasted = cv2.LUT(image, lut_8u)
        image_contrasted = image
        rows,cols,_ = image.shape

        # for i in range(rows):
        #     for j in range(cols):
        #         print(image_contrasted[i,j])
                # image_contrasted = image_contrasted[i,j] * image[i,j]
        # image_contrasted[...,0] = cv2.multiply(image_contrasted[...,0], image[...,0])/25.0
        # image_contrasted[...,1] = cv2.multiply(image_contrasted[...,1], image[...,1])/25.0
        # image_contrasted[...,2] = cv2.multiply(image_contrasted[...,2], image[...,2])/25.0

        # image_contrasted = cv2.multiply(image_contrasted.astype(float)/255, image.astype(float)/255)

        cv2.imwrite('outputfolder/'+frame_img+'_curvecorrected.png',
                    image_contrasted,
                    [cv2.IMWRITE_PNG_COMPRESSION, 0])
