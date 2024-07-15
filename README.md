## 說明
    可以對數獨題目的照片進行影像分析，並分析出答案
    詳情請參見Group3 SudoAnswer


## 操作說明
1. 程式入口：main.py
2. 在與main.py同目錄下會生成圖片經過不同處理時的結果
    * 二值化：
    ![二值化](ReadmeImage/binary_image.jpg)

    * 膨脹：
    ![膨脹](ReadmeImage/dilate_image.jpg)

    * 侵蝕：
    ![侵蝕](ReadmeImage/erode_image.jpg)

    * sobelX：
    ![sobelX](ReadmeImage/sobelX.jpg)

    * sobelY：
    ![sobelY](ReadmeImage/sobelY.jpg)

    * sobelXY：
    ![sobelXY](ReadmeImage/sobelXY.jpg)

    * 擦除邊框後效果：
    ![擦除邊框](ReadmeImage/line_earse.jpg)

3. demo影片：
    [![數獨圖片答案產生 - demo](https://img.youtube.com/vi/GUGQ33RJa5s/maxresdefault.jpg)](https://youtu.be/GUGQ33RJa5s)

## 依賴
* numpy
* cv2 (opencv-python)
* PIL
* ddddocr