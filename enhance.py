import cv2
import numpy as np

def img_enhance(img):
    #進行影像增強
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
    resized_image = cv2.resize(image, (2000,2000))
    
    #指定二值化閾值
    threshold_value = 128
    
    #二值化
    ret, binary_image = cv2.threshold(resized_image, threshold_value, 255, cv2.THRESH_BINARY)
    cv2.imwrite("binary_image.jpg", binary_image)
    
    #進行膨脹
    kernel_size = (3, 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    dilated_image = cv2.dilate(binary_image, kernel, iterations=1)
    cv2.imwrite("dilate_image.jpg", dilated_image)
    
    #進行侵蝕
    kernel_size = (5, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    erode_image = cv2.erode(dilated_image, kernel, iterations=1)
    cv2.imwrite("erode_image.jpg", erode_image)

    return erode_image

def line_dector(img):
    #去除邊框
    
    #圖片預處理
    #img = img_enhance(img)
    
    #利用sobel偵測 vertical 與 horzation 的邊框
    sobelX = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    sobelX = np.uint8(np.absolute(sobelX))
    cv2.imwrite("sobelX.jpg", sobelX)

    sobelY = cv2.Sobel(img, cv2.CV_64F, 0, 1)
    sobelY = np.uint8(np.absolute(sobelY))
    cv2.imwrite("sobelY.jpg", sobelY)
    
    sobelXY = cv2.bitwise_or(sobelX,sobelY)
    cv2.imwrite("sobelXY.jpg", sobelXY)
    
    
    #列出邊框大約的角度
    angle_list = [1,2,3,4,5,6,7,8,9,10,85,86,87,88,89,90,91,92,93,94,95]
    for angle in angle_list:
        #使用Hough直線變換檢測直線
        lines = cv2.HoughLinesP(sobelXY,1,(np.pi/180)*angle,200,minLineLength=150,maxLineGap=40)
        #在原圖上用白色繪製檢測到的直線以擦除邊框
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), 255, 30) 
    
    
    #re_image = Image.fromarray(np.uint8(img))
    #re_image.show()
    return img

def pureNumber(path):
    img = cv2.imread("sudoku10.jpg")
    enhance_image = img_enhance(img)
    non_ege_image = line_dector(enhance_image)
    
    return non_ege_image
    
if __name__ == '__main__':
    
    img = cv2.imread(r"sudoku1.jpg")
    enhance_image = img_enhance(img)
    non_dege_image = line_dector(img)
    
    '''pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    #enhance_image = Image.fromarray(enhance_image)
    image = cv2.imread("testII.png", cv2.IMREAD_GRAYSCALE)
    #re_image = Image.fromarray(re_image)
    #text = pytesseract.image_to_string(image, config='--psm 6')
    
    #enhance_image.show(title="enhance")'''