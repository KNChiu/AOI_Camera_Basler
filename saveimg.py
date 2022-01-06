"""This sample shows how grabbed images can be saved using pypylon only (no
need to use openCV).
Available image formats are     (depending on platform):
 - pylon.ImageFileFormat_Bmp    (Windows)
 - pylon.ImageFileFormat_Tiff   (Linux, Windows)
 - pylon.ImageFileFormat_Jpeg   (Windows)
 - pylon.ImageFileFormat_Png    (Linux, Windows)
 - pylon.ImageFileFormat_Raw    (Windows)
"""
from pypylon import pylon
import platform

import time
import cv2

num_img_to_save = 12
img = pylon.PylonImage()
tlf = pylon.TlFactory.GetInstance()

cam = pylon.InstantCamera(tlf.CreateFirstDevice())
cam.Open()
cam.StartGrabbing()

imgMode = 'bmp'
start = time.time()

for i in range(num_img_to_save):
    with cam.RetrieveResult(2000) as result:

        # Calling AttachGrabResultBuffer creates another reference to the
        # grab result buffer. This prevents the buffer's reuse for grabbing.
        img.AttachGrabResultBuffer(result)

        if imgMode == 'jpeg':
            if platform.system() == 'Windows':
                # The JPEG format that is used here supports adjusting the image
                # quality (100 -> best quality, 0 -> poor quality).
                ipo = pylon.ImagePersistenceOptions()
                # quality = 90 - i * 10
                ipo.SetQuality(100)

                filename = "saveimg\saved_pypylon_img_%d.jpeg" % i
                img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)
            else:
                filename = "saveimg\saved_pypylon_img_%d.png" % i
                img.Save(pylon.ImageFileFormat_Png, filename)
        elif imgMode == 'bmp':
            filename = "saveimg\saved_pypylon_img_%d.bmp" % i
            img.Save(pylon.ImageFileFormat_Bmp, filename)

        # In order to make it possible to reuse the grab result for grabbing
        # again, we have to release the image (effectively emptying the
        # image object).
        img.Release()
    
    # print("ok")
    img1 = cv2.imread('saveimg\saved_pypylon_img_' + str(i) + '.' + str(imgMode))
    print(img1.shape)

cam.StopGrabbing()
cam.Close()
print("存12張jpeg+讀取: "+str(time.time() - start))