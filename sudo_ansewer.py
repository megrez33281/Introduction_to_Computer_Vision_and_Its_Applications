

sudo_answer_list = []
def judge(sudo: list):
    #判定目前是否符合規則
    #若存在未填上的格子，列出其可能的數字(未填數字以0表示)
    err = set() #若有錯誤，記錄錯誤位置
    res = 1 #判定結果
    empty_block = {} #用dict紀錄沒有填的數字
    full = 1 #用以判定該sudo是否有未填數字(0代表有，1代表沒有)
    #rol判定
    for row in range(0, 9):
        nums = ""
        empty_list = []
        for col in range(0, 9):
            if sudo[row][col] == '0':
                empty_list.append([row, col])
                full = 0
            elif nums.find(sudo[row][col]) == -1:
                nums += sudo[row][col]
            else:
                err.add(str(row) + str(col))
                for index in range(0, col):
                    if sudo[row][index] == sudo[row][col]:
                        err.add(str(row) + str(index))
                res = 0
        if len(empty_list) > 0:
            possible_number = ""
            for n in range(1, 10):
                if nums.find(str(n)) == -1:
                    possible_number += str(n)
            for des in empty_list:
                key = str(des[0]) + str(des[1])
                empty_block[key] = possible_number
    

    #col判定
    for col in range(0, 9):
        nums = ""
        empty_list = []
        for row in range(0, 9):
            if sudo[row][col] == '0':
                full = 0
                empty_list.append([row, col])
            elif nums.find(sudo[row][col]) == -1:
                nums += sudo[row][col]
            else:
                err.add(str(row) + str(col))
                for index in range(0, row):
                    if sudo[index][col] == sudo[row][col]:
                        err.add(str(index) + str(col))
                res = 0
        
        if len(empty_list) > 0:
            possible_number = ""
            for n in range(1, 10):
                if nums.find(str(n)) == -1:
                    possible_number += str(n)
            for des in empty_list:
                key = str(des[0]) + str(des[1])
                original = empty_block[key]
                current = ""
                for ch in possible_number:
                    if original.find(ch) != -1:
                        current += ch
                empty_block[key] = current
           

    #九宮格判定
    nine_nums = ["", "", "", "", "", "", "", "", ""]
    empty_list = [[], [], [], [], [], [], [], [], []]
    for row in range(0, 9):
        for col in range(0, 9):
            index = int(row/3)*3 + int(col/3)
            if sudo[row][col] == '0':
                full = 0
                empty_list[index].append([row, col])

            elif nine_nums[index].find(sudo[row][col]) == -1:
                nine_nums[index] += sudo[row][col]
            else:
                err.add(str(row) + str(col))
                nine_row = int(index/3)*3
                nine_col = (index%3)*3
                for n_r in range(0,3):
                    for n_c in range(0,3):
                        if sudo[nine_row+ n_r][nine_col +n_c] == sudo[row][col] and (nine_row+ n_r != row or nine_col +n_c != col):
                            err.add(str(nine_row+ n_r) + str(nine_col +n_c))
                res = 0
    for ptr in range(0, 9):
        if len(empty_list[ptr]) > 0:
            possible_number = ""
            for n in range(1, 10):
                if nine_nums[ptr].find(str(n)) == -1:
                    possible_number += str(n)
            for des in empty_list[ptr]:
                key = str(des[0]) + str(des[1])
                original = empty_block[key]
                current = ""
                for ch in possible_number:
                    if original.find(ch) != -1:
                        current += ch
                empty_block[key] = current

    return res, err, empty_block, full


def sudo_answer(sudo: list, one_answer = 1):
    #one_answer若設為1，找出第一個答案即停止
    if one_answer == 1 and len(sudo_answer_list) > 0:
        return []
    answer_list = []
    res, err, empty_block, full = judge(sudo)
    if full == 0 and res == 1 and len(empty_block) > 0:
        #若傳入的sudo尚未填滿且目前內容皆為正確，便填入一個可能的格子
        key = ""
        min_len = 999
        for element in empty_block:
            if len(empty_block[element]) < min_len:
                key = element
                min_len = len(empty_block[element])
        possible_string = empty_block[key]
        for ch in possible_string:
            row = int(key[0])
            col = int(key[1])
            new_sudo = copySudo(sudo)
            new_sudo[row][col] = ch
            ans_list = sudo_answer(new_sudo, one_answer)
            for ans in ans_list:
                answer_list.append(ans)
    
    elif full == 1 and res == 1:
        #出口，當傳入的sudo經judge後符合規則，且已經填滿，即返回答案
        answer_list.append(sudo)
        sudo_answer_list.append(sudo)

    else:
        #出口，若傳入的sudo有錯誤或者無錯誤但未填滿且已經無法填入，便不返回答案
        return []

    return answer_list 

def copySudo(sudo: list):
    new_sudo = []
    for row in sudo:
        a_list = []
        for col in row:
            a_list.append(col)
        new_sudo.append(a_list)

    return new_sudo

def printSudo(sudo: list):
    for row in sudo:
        for col in row:
            print(col, end=' ')
        print()
    print()

if __name__ == '__main__':
    
    file = open("sudo4.txt", mode='r')
    content = file.readlines()
    sudo = []
    for line in content:
        line = line.replace("\n", "")
        sudo.append(line.split(" "))
    
    answers = sudo_answer(sudo, 1)
    for ans in answers:
        printSudo(ans)
