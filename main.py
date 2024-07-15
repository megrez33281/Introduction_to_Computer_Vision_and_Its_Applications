import enhance
import sudo_ansewer
import RowColScanner
import numberJudge
import cv2
import numpy as np
from PIL import Image



path = ""


if __name__ == '__main__':
    
    path = input("圖片路徑：")
    path = path.replace("'", "")
    preimg = Image.open(path)
    img = cv2.cvtColor(np.asarray(preimg), cv2.COLOR_RGB2BGR)
    enhance_image = enhance.img_enhance(img)
    cv2.imwrite('enhance.jpg', enhance_image)
    non_ege_image = enhance.line_dector(enhance_image)
    cv2.imwrite('line_earse.jpg', non_ege_image)
    Num_list = RowColScanner.findBorderHistogram(non_ege_image)
    nine_grids = numberJudge.number_detect(Num_list)
    if nine_grids != []:
        #此OCR目前狀況為可能將1認成7
        #sudo_ansewer.printSudo(nine_grids)
        ans = sudo_ansewer.sudo_answer(nine_grids)
        if ans != []:
            sudo_ansewer.printSudo(ans[0])
        else:
            print("圖片辨識出錯!")
        
    else:
        print("圖片辨識出錯!")
    
    input()
