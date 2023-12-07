import sqlite3
import cv2
from datetime import datetime
import time
import requests
import os
from pygame import mixer
from gtts import gTTS
import re
import smtplib

base = 'https://japanwest.api.cognitive.microsoft.com/face/v1.0'   #API(網址)
key = ''    #金鑰
headers_stream = {} #stream請求標頭
headers_json = {}   #json請求標頭
headers = {}        #GET的請求標頭


def face_init(b, k):
    global base, key, headers_stream, headers_json, headers
    base = b    #API(網址)
    key = k     #金鑰
    headers_stream = {"Ocp-Apim-Subscription-Key": key,     #stream請求標頭
                      "Content-Type": "application/octet-stream"}
    headers_json = {"Ocp-Apim-Subscription-Key": key,       #json請求標頭
                    "Content-Type": "application/json"}
    headers = {"Ocp-Apim-Subscription-Key": key}            #GET的請求標頭
    
    
gid = ''    #群組id
pid = ''    #成員id


def face_use(g, p):
    global gid, pid
    gid = g
    pid = p
    

##

#新增name串列
def name_list(gid):
    global names
    names = []
    persons = person_list(gid)
    for p in persons:
        names.append(p['name'])
    return names
    
#語音
mixer.init()
if not os.path.isfile("tmp.mp3"):
    tts = gTTS(text = "不重要的語音檔", lang = "zh-tw")
    tts.save("tmp.mp3")
    print("已產生不重要的語音檔")
def bot_speak(text, lang):
    try :
        mixer.music.load("tmp.mp3")
        tts = gTTS(text = text, lang =lang)
        tts.save("speak.mp3")
        mixer.music.load("speak.mp3")
        mixer.music.play()
        while(mixer.music.get_busy()):
            continue
    except:
        print("播放失敗")
def bot_speak_re(sentence):
    s1 = re.sub(r"\[[^\]]*\]", "", sentence)#除去註解
    #print(s1)
    en_list = re.findall(r"[a-zA-Z]+", s1)
    s2 = re.sub(r"[a-zA-Z]+", "@English@", s1)
    all_list = s2.split("@")
    index = 0
    for text in all_list:
        if text != "English":
            bot_speak(text, "zh-tw")
        else:
            bot_speak(en_list[index],"en")
            index += 1
  
#寄email
def send_gmail(gmail_add,gmail_pwd,to_addrs,msg):
    smtp_gmail = smtplib.SMTP("smtp.gmail.com",587)#跟伺服器連線
    print(smtp_gmail.ehlo())
    print(smtp_gmail.starttls())#加密
    print(smtp_gmail.login(gmail_add, gmail_pwd))
    status = smtp_gmail.sendmail(gmail_add, to_addrs, msg)
    if not status:
        print("成功")
    else:
        print("失敗")
    smtp_gmail.quit()#結束連線
    
#新增人員資料(personId)
def employee_add(name, userData): 
    global msg_add
    gp_url = f"{base}/persongroups/{gid}/persons"
    
    body = {"name": name, "userData": userData}
    body = str(body).encode("utf-8")
    
    response = requests.post(gp_url, 
                             headers = headers_json, 
                             data = body)
    if response.status_code == 200:
        msg_add = "新增人員完成"
        print("新增人員完成：", response.json())
    else:
        msg_add = "新增失敗"
        print("新增失敗：", response.json())

        
#用名字找ID(新增FaceId、刪除人員會用到)
def employee_who(name): 
    persons = person_list(gid)
    for p in persons:
        if name == p['name']:
            return(p['personId'])
        
#刪除人員資料
def employee_remove(name):
    global msg_remove
    pid = employee_who(name)
    face_url = f"{base}/persongroups/{gid}/persons/{pid}"
    response2 = requests.delete(face_url, 
                                headers = headers_json)
    if response2.status_code == 200:
        msg_remove = "刪除人員完成"
        print("刪除人員完成")
    else:
        msg_remove = "抱歉，刪除失敗"
        print("刪除失敗", response2.json())

##
    
def face_add(img):
    global msg_add
    # 將 img 編碼為 jpg 格式，[1]返回資料, [0]返回是否成功
    img_encode = cv2.imencode(".jpg", img)[1]
    img_bytes = img_encode.tobytes()                    # 再將資料轉為 bytes, 此即為要傳送的資料
    face_url = f"{base}/persongroups/{gid}/persons/{pid}/persistedFaces"
    # 新增臉部資料的請求路徑
    response = requests.post(face_url,                  # POST 請求
                             headers = headers_stream, 
                             data = img_bytes) 
    if response.status_code == 200:
        msg_add = "新增臉部成功，請等待一段時間後再進行臉部辨識"
        print("新增臉部成功") #, response.json())
        #訓練臉部資料
        train_url = f"{base}/persongroups/{gid}/train"
        train_response = requests.post(train_url, headers=headers)
        if train_response.status_code == 202:
            print("開始訓練...")
        else:
            print("訓練失敗", response.json())
    else:
        msg_add = "新增臉部失敗，請確認填寫資料有無錯誤"
        print("新增臉部失敗", response.text) #, response.json())
        
        
def face_detect(img):
    detect_url = f"{base}/detect?returnFaceId=true" # 臉部偵測的請求路徑
    # 將 img 編碼為 jpg 格式，[1]返回資料, [0]返回是否成功
    img_encode = cv2.imencode('.jpg', img)[1]
    img_bytes = img_encode.tobytes()                # 再將資料轉為 bytes, 此即為要傳送的資料
    response = requests.post( detect_url, 
                             headers = headers_stream, 
                             data = img_bytes)
    if response.status_code == 200:
        face = response.json()
        if not face:
            print("照片中沒有偵測到人臉")
        else:
            faceId = face[0]['faceId']              #取得FaceId
            return faceId
        
        
def face_identify(faceId):
    idy_url = f'{base}/identify'                    #臉部偵測的請求路徑
    body = str({'personGroupId': gid,
                'faceIds': [faceId]})
    response = requests.post(idy_url,               #臉部驗證請求POST
                             headers = headers_json, 
                             data = body) 
    if response.status_code == 200:
        person = response.json()
        if not person[0]['candidates']:
            return None                             #若查無此人，回傳None
        else:
            personId = person[0]['candidates'][0]['personId'] # 取得 personId
            print(personId)
            return personId
        
        
msg_punchInOut = ""
def face_who(img, work):
    global msg_punchInOut
    faceId = face_detect(img)                       #執行臉部偵測，取得faceId
    personId = face_identify(faceId)                #用faceId進行臉部辨識，找出群組中最像的人，取得personId
    msg_punchInOut = ""
    if personId == None:
        msg_punchInOut = "查無相符身分"
        print("查無相符身分")
    else:
        persons = person_list(gid)                  #取得群組的成員清單
        for p in persons:                           #走訪清單中的每一個成員
            if personId == p['personId']:           #取出personId做比對
                msg_punchInOut = f"{p['name']}"
                print(p['name'])                    #取得姓名
                if work:
                    db_save('punchin_db.sqlite', p['name'], work) #存入資料庫
                    db_check('punchin_db.sqlite')           #查看資料庫
                else:
                    db_save('punchout_db.sqlite', p['name'], work) #存入資料庫
                    db_check('punchout_db.sqlite')           #查看資料庫
                    
               
                
def person_list(gid):
    pson_url = base + f"/persongroups/{gid}/persons" # 查看群組人員的請求路徑
    response = requests.get(pson_url,                # HTTP GET
                            headers=headers)
    if response.status_code == 200:
        print("查詢人員完成")
        return response.json()
    else:
        print("查詢人員失敗：", response.json())      # 印出創建失敗原因
               

#msg_work = ""
def db_save(db, name, work):
    global msg_work
    connect = sqlite3.connect(db)                   #與資料庫連線
    #新建myTable資料表(如果尚未建立的話)
    sql = ' create table if not exists mytable \
            ("姓名" TEXT, "打卡時間" TEXT)'
    connect.execute(sql)                            #執行SQL語法
    #取得時間
    worktime = datetime(2021, 5, 31, 9, 1, 0)
    worktime = worktime.hour*60*60 + worktime.minute*60 + worktime.second
    now = datetime.now()
    now = now.hour*60*60 + now.minute*60 + now.second
    #取得現在時間
    save_time = str(datetime.now().strftime("%Y-%m-%d %H.%M.%S"))
    #新增一筆資料
    sql = f'insert into mytable values("{name}", "{save_time}")'
    connect.execute(sql) #執行SQL語法
    connect.commit()     #更新資料庫
    connect.close()      #關閉資料庫
    #判斷上下班
    if work:
        #判斷是否遲到
        if (worktime - now) > 0:
            msg_work = "準時上班"
        else:
            msg_work = "上班遲到"
    else:
        msg_work = "下班"

    
#text_db = ""
def db_check(db):
    #global text_db
    try:
        connect = sqlite3.connect(db)       # 與資料庫連線
        connect.row_factory = sqlite3.Row   # 設定成 Row 物件
        sql = 'select * from mytable'       # 選取資料表中所有資料的 SQL 語法
        cursor = connect.execute(sql)       # 執行 SQL 語法得到 cursor 物件
        dataset = cursor.fetchall()         # 取得所有資料
        col1 = dataset[0].keys()[0]     # 取得第一筆資料的第一個欄位名稱
        col2 = dataset[0].keys()[1]     # 取得第一筆資料的第二個欄位名稱
        text_db = f'{col1} \t{col2} \
                \n----\t  ----\n'
        text_data = ''
        print(f'{col1} \t{col2}')
        print('----\t  ----')
        for data in dataset:
            text_data = f'{data[0]} \t{data[1]}\
                        \n{text_data}'
            print(f'{data[0]} \t{data[1]}')
        print("")
        text_db += text_data 
    except:
        text_db = ''
        print("讀取資料庫錯誤")
    connect.close()
    return text_db
    
    
#------------------------------#
def face_shot(function, work):
    global img
    isCnt = False                               #用來判斷是否正在進行倒數計時中
    face_detector = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml")  #建立臉部辨識物件
    capture = cv2.VideoCapture(0)               #開啟編號0的攝影機
    snapshot = 0
    while capture.isOpened() and snapshot == 0:                   #判斷攝影機是否開啟成功
        success, img = capture.read()           #讀取攝影機影像
        if not success:
            print("讀取影像失敗")
            continue
        img_copy = img.copy()                   #複製影像
        faces = face_detector.detectMultiScale( #從攝影機影像中偵測人臉
            img, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(200,200)) 
        if len(faces) == 1:                     #如果偵測到一張人臉
            if isCnt == False:
                t1 = time.time()                #紀錄現在的時間
                isCnt = True                    #告訴程式目前進入倒數狀態
            cnter = 3 - int(time.time() - t1)   #更新倒數計時器-----------3秒
            for (x, y, w, h) in faces:          #畫出人臉位置
                cv2.rectangle(                  #繪製矩形
                    img_copy, 
                    (x, y), 
                    (x+w, y+h), 
                    (0, 255, 255), 2) 
                cv2.putText(                    #繪製倒數數字
                    img_copy, 
                    str(cnter), 
                    (x+int(w/2), y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1, 
                    (0, 255, 255), 2) 
            if cnter == 0:                      #倒數結束
                isCnt = False                   #告訴程式離開倒數狀態
                filename = datetime.now().strftime(
                    "%Y-%m-%d %H.%M.%S")        #時間格式化
                cv2.imwrite(filename + ".jpg", img) #儲存影像檔案
                #=============================================================================#
                if function == "add":           #打卡系統新增人員
                    face_add(img) 
                    snapshot += 1
                elif function == "who":         #進行人臉身分識別功能
                    face_who(img, work)
                    snapshot += 1
                #=============================================================================#
        else:                                   #如果不是一張人臉
            isCnt = False                       #設定非倒數狀態

        cv2.imshow("Frame", img_copy)           #顯示影像
        k = cv2.waitKey(1)                      #讀取按鍵輸入(若無會回傳-1)
        if k == ord("q") or k == ord("Q"):      #如果按下q結束while迴圈
            print("exit")                       #結束程式
            cv2.destroyAllWindows()             #關閉視窗
            capture.release()                   #關閉攝影機
            break                               #離該無窮迴圈，結束程式
        
    cv2.destroyAllWindows()                     #關閉視窗
    capture.release()                           #關閉攝影機
