import ddddocr
import contextlib
import io


def number_detect(Num_list):
    nine_grids = [['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0','0']]
    
    #在使用ddddocr庫時重定向標準輸出，避免其輸出內容
    null = io.StringIO()
    ocr = ''
    with contextlib.redirect_stdout(null):
        ocr = ddddocr.DdddOcr()
    
    for pic in Num_list:
        col =  pic[1]
        row = pic[2]
        
        reImage = pic[0].resize((28,28))
        textI = ocr.classification(reImage)
        nine_grids[col][row] = textI
        if textI < '0' or textI > '9':
            return []
        
            
    return nine_grids




