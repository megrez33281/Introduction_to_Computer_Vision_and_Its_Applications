import numpy as np
import cv2
from PIL import Image


def extractPeek(array_vals, min_vals=5*255, min_rect=20):
    #進行邊界判斷
    #min_vals：每行/列的相加值之邊界判斷
    extrackPoints = []
    startPoint = None
    endPoint = None
    for i,point in enumerate(array_vals):
        if point>min_vals and startPoint == None:
            startPoint = i
        elif point<min_vals and startPoint != None:
            endPoint = i

        if startPoint != None and endPoint != None:
            extrackPoints.append((startPoint, endPoint)) 
            startPoint = None
            endPoint = None
            
    if endPoint == None and startPoint != None:
        endPoint = len(array_vals)-1  #當到達底部且沒找到邊界時將底部視為邊界
        extrackPoints.append((startPoint, endPoint))
    #刪除寬度不符合的點
    for point in extrackPoints:
        if point[1] - point[0] < min_rect:
            extrackPoints.remove(point) 
    return extrackPoints

def SignalExtract(array_vals, min_vals=5, min_rect=20):
    #進行單個圖片的最後一次橫切
    #min_vals：每行/列的相加值之邊界判斷
    startPoint = None
    endPoint = None
    for i,point in enumerate(array_vals):
        if point>min_vals and startPoint == None:
            startPoint = i
        elif point>min_vals and startPoint != None: 
            endPoint = i #找到最後一個大於min_vals之位置
      
    if endPoint == None and startPoint != None:
        endPoint = len(array_vals)-1  #當到達底部且沒找到邊界時將底部視為邊界
    
    return [startPoint, endPoint]  

def findBorderHistogram(img):
    #切割出所有數字並計算對應位置
    #回傳為(圖片, 列座標, 行座標)
    #img = cv2.imread(path)
    #img = enhance.line_dector(img)
    img = cv2.bitwise_not(img)#轉為黑底白字
    img = np.uint8(img)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img = img.convert('L')#轉為灰階模式

    #將外圍的部分去除
    hori_vals = np.sum(img, axis=1) #得到橫軸和的陣列用以判斷是否為邊界
    hori_points = extractPeek(hori_vals) #得到行座標
    img = img.crop((0, hori_points[0][0], img.width, hori_points[-1][1]))
    vertical_vals = np.sum(img, axis=0)
    vertical_points = extractPeek(vertical_vals) #得到列座標
    img = img.crop((vertical_points[0][0], 0, vertical_points[-1][1], img.height))


    #行掃描
    hori_vals = np.sum(img, axis=1) #得到橫軸和的陣列用以判斷是否為邊界
    hori_points = extractPeek(hori_vals) #得到行座標    
    
    #用來補丁
    max_height = 0
    max_width = 0
    
    #進行行切割
    RowImg_list = []
    for hori_point in hori_points:
        RowImg = img.crop((0, hori_point[0], img.width, hori_point[1])) #提取橫切割區域
        #儲存行圖片並記錄y座標
        RowImg_list.append([RowImg, hori_point[0], hori_point[1]])
        max_height = max(max_height, RowImg.height)

    #進行列切割
    NumImg_list = []
    for RowImg,y0,y1 in RowImg_list:
        vec_vals = np.sum(RowImg,axis=0) #得到縱軸和之陣列用以判斷邊界
        vec_points = extractPeek(vec_vals, min_rect=20)
        for vec_point in vec_points:
            IndividualImg = RowImg.crop((vec_point[0], 0, vec_point[1], RowImg.height))#依左上角以及右下角座標提取            
            #再進行一次行切割得到最適合大小
            hori_vals = np.sum(IndividualImg, axis=1) #得到橫軸和的陣列用以判斷是否為邊界
            start_point, end_point = SignalExtract(hori_vals) #得到行座標
            IndividualImg = IndividualImg.crop((0, start_point, IndividualImg.width, end_point))
            max_width = max(max_width, IndividualImg.width)
            NumImg_list.append([IndividualImg, vec_point[0], y0, vec_point[1], y1])
    
    #打補釘與計算每個數字的對應位置
    img_width = img.width
    img_height = img.height
    size = max(max_height, max_width)
    size += 10
    for num in range(0, len(NumImg_list)):
        NumImg = patch(NumImg_list[num][0], size)
        #轉回白底黑字
        NumImg = np.array(NumImg, dtype=np.uint8)
        NumImg = cv2.bitwise_not(NumImg)
        NumImg = Image.fromarray(NumImg)
        NumImg = NumImg.convert("L")
        
        #計算該數字在九宮格的對應位置
        middleX = int((NumImg_list[num][1] + NumImg_list[num][3]) / 2)
        middleY = int((NumImg_list[num][2] + NumImg_list[num][4]) / 2)
        row = int((middleY/img_height)*9)
        column = int((middleX/img_width)*9)
        #將圖片大小縮小到28*28更好辨識
        #NumImg = NumImg.resize((28,28))
        NumImg_list[num] = [NumImg, row, column]
        
    return NumImg_list 


def patch(image, size):
    #將圖片擴充到對應size
    new_image = Image.new("RGB", (size, size), color="black")

    #將原圖放在新圖片中心
    x_offset = (new_image.width - image.width) // 2
    y_offset = (new_image.height - image.height) // 2
    new_image.paste(image, (x_offset, y_offset))
    return new_image

if __name__ == '__main__':
    path = r"sudoku10.jpg"
    #temp = Image.open(path)
    #temp.show()
    #print()
    #Num_list = findBorderHistogram(path)


