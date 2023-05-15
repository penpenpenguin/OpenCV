from tkinter import *
from tkinter import messagebox
import face_module as m   #匯入自訂模組
from email.mime.text import MIMEText
import requests


base = 'https://japanwest.api.cognitive.microsoft.com/face/v1.0'
key = '8fc02b711ebb45a69764a84b5e9c969a'
gid = 'gp01'
headers = {"Ocp-Apim-Subscription-Key": key}

#寄email
gmail_add = "bunny123test@gmail.com"
gmail_pwd = "mailTesting"
to_addrs = ["mfpss97176@gmail.com"]


m.face_init(base, key)
m.face_use(gid, '')

#設定
def setting():
    #新增人員資料(personId)
    def info_input():
        m.face_init(base, key)
        m.face_use(gid, ' ')
        m.employee_add(name.get(), userData.get())
        m.name_list(gid)
        text.delete(1.0, "end")
        for n in m.names:
            text.insert(END, n+"\n")
        label3['text'] = m.msg_add
            
        mime_text = MIMEText(f"已成功新增{name.get()}的初始資料","plain","utf-8") #plain是text類型
        mime_text["Subject"] = "新增人員資料"
        mime_text["To"] = "XX科技公司"
        mime_text = mime_text.as_string()
        m.send_gmail(gmail_add, gmail_pwd, to_addrs, mime_text)
    
    #刪除文字框內容
    def input_del():
        entry1.delete(0, END)
        entry2.delete(0, END)
        
    #新增人臉辨識(FaceId)
    def face_add(): 
#        pid = m.employee_who(name.get())
        m.face_init(base, key)
        m.face_use(gid, m.employee_who(name.get()))
        m.face_shot('add', False)
        label3['text'] = m.msg_add
        
        mime_text = MIMEText(f"已成功新增{name.get()}的人臉辨識","plain","utf-8") #plain是text類型
        mime_text["Subject"] = "新增人臉辨識"
        mime_text["To"] = "XX科技公司"
        mime_text = mime_text.as_string()
        m.send_gmail(gmail_add, gmail_pwd, to_addrs, mime_text)
        
    #刪除員工資料
    def info_remove():
        m.employee_remove(name.get())
        m.name_list(gid)
        text.delete(1.0, "end")
        for n in m.names:
            text.insert(END, n+"\n")
        label3['text'] = m.msg_remove
        
        mime_text = MIMEText(f"已成功刪除{name.get()}的所有資料","plain","utf-8") #plain是text類型
        mime_text["Subject"] = "刪除人員資料"
        mime_text["To"] = "XX科技公司"
        mime_text = mime_text.as_string()
        m.send_gmail(gmail_add, gmail_pwd, to_addrs, mime_text)
    
    
    #-----
    settingWin = Toplevel(window)
    settingWin.state('zoomed')
    
    #main_frame
    main_frame = Frame(settingWin)
    label = Label(main_frame, text = "設定", justify = CENTER)
    
    #sub1_frame
    sub1_frame = Frame(main_frame)
    
    
    #sub1_frame1
    sub1_frame1 = Frame(sub1_frame)
    label1 = Label(sub1_frame1, text = "姓名：　") 
    name = StringVar()
    entry1 = Entry(sub1_frame1, textvariable = name)
    #sub1_frame2
    sub1_frame2 = Frame(sub1_frame)
    label2 = Label(sub1_frame2, text = "居住地：")
    userData = StringVar()
    entry2 = Entry(sub1_frame2, textvariable = userData)
    #sub1_frame4
    sub1_frame4 = Frame(sub1_frame)
    label3 = Label(sub1_frame4, text ="--", justify = CENTER)   #顯示訊息
    #sub1_frame3
    sub1_frame3 = Frame(sub1_frame)
    btn1 = Button(sub1_frame3, text = "新增人員", command = info_input)
    btn5 = Button(sub1_frame3, text = "刪除人員", command = info_remove)
    btn2 = Button(sub1_frame3, text = "新增臉部", command = face_add)
    btn3 = Button(sub1_frame3, text = "取消", command = input_del)
    btn4 = Button(sub1_frame3, text = "返回", command = settingWin.destroy)
      
    #sub2_frame
    sub2_frame = Frame(main_frame)
    #blank
    blank1 = Label(sub2_frame, text = " ")
    #sub2_frame1
    sub2_frame1 = Frame(sub2_frame)
    sbar = Scrollbar(sub2_frame1)
    label4 = Label(sub2_frame1, text = "員工列表", justify = CENTER)
    text = Text(sub2_frame1, height = 7, width = 7, wrap = NONE)
    m.name_list(gid)
    for n in m.names:
        text.insert(END, n+"\n")
    
    
    #----- 
    #main_frame
    main_frame.place(relx=0.5, rely=0.5, anchor = CENTER)
    label.pack()
    
    #sub1_frame
    sub1_frame.pack(side = RIGHT)
    #sub1_frame1
    sub1_frame1.pack()
    label1.pack(side = LEFT)
    entry1.pack(side = LEFT)
    #sub1_frame2
    sub1_frame2.pack()
    label2.pack(side = LEFT)
    entry2.pack(side = LEFT)
    #sub1_frame4
    sub1_frame4.pack()
    label3.pack()
    #sub1_frame3
    sub1_frame3.pack()
    btn1.pack(side = LEFT)
    btn5.pack(side = LEFT)
    btn2.pack(side = LEFT)
    btn3.pack(side = LEFT)
    btn4.pack(side = LEFT)
    
    #sub2_frame
    sub2_frame.pack(side = LEFT)
    #blank
    blank1.pack(side = RIGHT)
    #sub2_frame1
    sub2_frame1.pack()
    label4.pack()
    sbar.pack(side = RIGHT, fill = Y)
    text.pack(side = LEFT, fill = Y)
    sbar['command'] = text.yview 
    text['yscrollcommand'] = sbar.set 

    

#-----
def punchIn():
    m.face_init(base, key)
    m.face_use(gid, ' ')
    m.face_shot('who', True)
    #關掉視窗後更新
    label2['text'] = f'{m.msg_punchInOut}{m.msg_work}'
    #語音
    m.bot_speak_re(m.msg_punchInOut + m.msg_work)
    text1.delete(1.0,"end")
    text1.insert(END, m.db_check('punchin_db.sqlite'))
    

def punchOut():
    m.face_init(base, key)
    m.face_use(gid, ' ')
    m.face_shot('who', False)
    #關掉視窗後更新
    label2['text'] = f'{m.msg_punchInOut}{m.msg_work}'
    m.bot_speak_re(m.msg_punchInOut + m.msg_work)
    text2.delete(1.0,"end")
    text2.insert(END, m.db_check('punchout_db.sqlite'))
    
    
#-----
window = Tk()
window.title("XX公司打卡系統")
window.state('zoomed')

#main_frame
main_frame = Frame(window)
label = Label(main_frame, text = "XX公司打卡系統")

#sub2_frame
sub2_frame = Frame(main_frame)
label2 = Label(sub2_frame, text = "--")              #顯示訊息

#sub1_frame
sub1_frame = Frame(main_frame)
#frame1
frame1 = Frame(sub1_frame)
sbar1 = Scrollbar(frame1)
btn1 = Button(frame1, text = "上班", command = punchIn)
text1 = Text(frame1, height = 15, width = 30, wrap = NONE)
text1.insert(END, m.db_check('punchin_db.sqlite'))    #最新資料顯示在上面
#blank
blank = Label(sub1_frame, text = " ")
#frame2
frame2 = Frame(sub1_frame)
sbar2 = Scrollbar(frame2)
btn2 = Button(frame2, text = "下班", command = punchOut)
text2 = Text(frame2, height = 15, width = 30, wrap = NONE)
text2.insert(END, m.db_check('punchout_db.sqlite'))    #最新資料顯示在上面

#sub3_frame
sub3_frame = Frame(main_frame)
btn3 = Button(sub3_frame, text = "設定", command = setting)
btn4 = Button(sub3_frame, text = "離開", command = window.destroy)



#-----
#main_frame
main_frame.place(relx=0.5, rely=0.5, anchor = CENTER)
label.pack()

#sub2_frame
sub2_frame.pack()
label2.pack()

#sub1_frame
sub1_frame.pack()
#frame1
frame1.pack(side = LEFT)
btn1.pack()
sbar1.pack(side = RIGHT, fill = Y)
text1.pack(side = LEFT, fill = Y)
sbar1['command'] = text1.yview 
text1['yscrollcommand'] = sbar1.set 
#blank
blank.pack(side = LEFT)
#frame2
frame2.pack(side = RIGHT)
btn2.pack()
sbar2.pack(side = RIGHT, fill = Y)
text2.pack(side = LEFT, fill = Y)
sbar2['command'] = text2.yview 
text2['yscrollcommand'] = sbar2.set

#sub3_frame
sub3_frame.pack()
btn4.pack(side = RIGHT)
btn3.pack(side = RIGHT)

#-----
window.mainloop()