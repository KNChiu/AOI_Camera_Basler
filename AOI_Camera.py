from pypylon import pylon
import cv2
import time


class CameraAPI():
    def __init__(self):
        pass
    
    def open_device(self):
        # 連結到相機
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        retryDelay = time.time() + 5    # 設定最高延遲時間
        while self.camera.IsOpen() != True and time.time() < retryDelay:
            self.camera.Open()          # 開啟相機
            if self.camera.IsOpen() != True:
                time.sleep(1)
                print('Retry open')

        # self.camera.Close()
        

    def start_grabbing(self):
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)               # 開啟相機串流(以最小的延遲持續抓取)
        self.converter = pylon.ImageFormatConverter()                               # 串流解碼
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed               # 轉換為BGR格式
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    
    def get_img_nummpy(self):
        grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)      # 設定串流
        if grabResult.GrabSucceeded():
            image = self.converter.Convert(grabResult)                                           # 取得串流影像
            grabResult.Release()
            return image.GetArray()
        
    def bmp_save(self, save_path, save_name):
        with self.camera.RetrieveResult(2000) as result:                            # 建立新的緩衝區
            img = pylon.PylonImage()

            img.AttachGrabResultBuffer(result)
            filename = str(save_path) + "\\" + str(save_name) + ".bmp"
            img.Save(pylon.ImageFileFormat_Bmp, filename)
            img.Release()                                                           # 釋放資源
    
    def stop_grabbing(self):
        self.camera.StopGrabbing()

    def close_device(self):
        self.camera.Close()


if __name__ == '__main__':
    AOICameraAPI = CameraAPI()
    
    AOICameraAPI.open_device()
    print("open_device")

    AOICameraAPI.start_grabbing()
    print("start_grabbing")

    cv2.namedWindow("showIMG",0)
    cv2.resizeWindow("showIMG", 500, 500) 

    while True:         
        start = time.time()
        numArray = AOICameraAPI.get_img_nummpy()
        if numArray is None:
            pass
        else:
            cv2.imshow("showIMG", numArray)
            print("FPS : " + str(round(1/(time.time() - start), 2)))
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('s'):
                AOICameraAPI.bmp_save(save_path = r"saveimg", save_name = time.strftime('%H%M%S', time.localtime()))
                print("bmp_save")
                time.sleep(0.1)

    AOICameraAPI.stop_grabbing()
    print("stop_grabbing")

    AOICameraAPI.close_device()
    print("close_device")

    print("finish")