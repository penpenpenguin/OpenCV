import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
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
    #新增人員視窗
    def addwin():
        #新增人員資料(personId)
        def info_input():
            m.face_init(base, key)
            m.face_use(gid, ' ')
            m.employee_add(name.get(), userData.get())
            m.name_list(gid)
            text.delete(1.0, "end")
            for n in m.names:
                text.insert(END, n+"\n")
            addtext['text'] = m.msg_add
                
            mime_text = MIMEText(f"已成功新增{name.get()}的初始資料","plain","utf-8") #plain是text類型
            mime_text["Subject"] = "新增人員資料"
            mime_text["To"] = "XX科技公司"
            mime_text = mime_text.as_string()
            m.send_gmail(gmail_add, gmail_pwd, to_addrs, mime_text)
        
        #刪除文字框內容
        def input_del():
            addentry1.delete(0, END)
            addentry2.delete(0, END)
            
        #新增人臉辨識(FaceId)
        def face_add(): 
    #        pid = m.employee_who(name.get())
            m.face_init(base, key)
            m.face_use(gid, m.employee_who(name.get()))
            m.face_shot('add', False)
            addtext['text'] = m.msg_add
            
            mime_text = MIMEText(f"已成功新增{name.get()}的人臉辨識","plain","utf-8") #plain是text類型
            mime_text["Subject"] = "新增人臉辨識"
            mime_text["To"] = "XX科技公司"
            mime_text = mime_text.as_string()
            m.send_gmail(gmail_add, gmail_pwd, to_addrs, mime_text)
        #-----    
        addWin = Toplevel(settingWin)
        addWin.title("新增人員視窗")
        addWin.geometry('500x300')
        
        menus(addWin)
        
        addframe = ttk.Frame(addWin)
        addframe1 = ttk.Frame(addframe)
        addlabel1 = ttk.Label(addframe1, text = "姓名：").grid(row=0,column=0)
        name = StringVar()
        addentry1 = Entry(addframe1, textvariable = name)
        addlabel2 = ttk.Label(addframe1, text = "居住地：").grid(row=1,column=0)
        userData = StringVar()
        addentry2 = Entry(addframe1, textvariable = userData)
        
        addframe2 = ttk.Frame(addframe)
        blank = ttk.Label(addframe2, text = "").pack(fill = 'x')
        addtext = ttk.Label(addframe2, text ="--", justify = CENTER, style = 'Content.TLabel')
        addtext.pack()
        
        addframe3 = ttk.Frame(addframe)
        addbtn1 = ttk.Button(addframe3, text = '新增資料', command = info_input).grid(row=0,column=0)
        addbtn2 = ttk.Button(addframe3, text = '新增臉部', command = face_add).grid(row=0,column=1)
        addbtn3 = ttk.Button(addframe3, text = '取消', command = input_del).grid(row=0,column=2)
        addbtn4 = ttk.Button(addframe3, text = '返回', command = addWin.destroy).grid(row=0,column=3)
        
        addframe.place(relx=0.5, rely=0.5, anchor = CENTER)
        addframe1.pack()
        addframe2.pack()
        addframe3.pack()
        addentry1.grid(row=0,column=1)
        addentry2.grid(row=1,column=1)
        
        color(addWin)
            
    #刪除人員視窗
    def removewin():
        #刪除員工資料
        def info_remove():
            m.employee_remove(employeelist.get())
            m.name_list(gid)
            text.delete(1.0, "end")
            for n in m.names:
                text.insert(END, n+"\n")
            rmtext['text'] = m.msg_remove
            
            mime_text = MIMEText(f"已成功刪除{employeelist.get()}的所有資料","plain","utf-8") #plain是text類型
            mime_text["Subject"] = "刪除人員資料"
            mime_text["To"] = "XX科技公司"
            mime_text = mime_text.as_string()
            m.send_gmail(gmail_add, gmail_pwd, to_addrs, mime_text)
        #-----   
        removeWin = Toplevel(settingWin)
        removeWin.title("刪除人員資料")
        removeWin.geometry('500x300')
        
        menus(removeWin)
        
        rmframe = ttk.Frame(removeWin)
        rmlabel = ttk.Label(rmframe, text = "請選擇要刪除的員工", justify = CENTER).pack()
        employeelist = ttk.Combobox(rmframe, values=m.names, state="readonly")
        employeelist.pack(fill='x')
        
        blank = ttk.Label(rmframe, text = "").pack(fill = 'x')
        rmtext = ttk.Label(rmframe, text ="--", justify = CENTER)
        rmtext.pack()
        
        rmbtn1 = ttk.Button(rmframe, text = '返回', command = removeWin.destroy).pack(side = RIGHT)
        rmbtn2 = ttk.Button(rmframe, text = '刪除資料', command = info_remove).pack(side = RIGHT)
        
        rmframe.place(relx=0.5, rely=0.5, anchor = CENTER)
        
        color(removeWin)

    #-----
    settingWin = Toplevel(window)
    settingWin.title("設定")
    settingWin.state('zoomed')
    settingWin.minsize(500,300)
    
    menus(settingWin)
    
    #main_frame
    stmain_frame = ttk.Frame(settingWin)
    stmain_frame.place(relx=0.5, rely=0.5, anchor = CENTER)
    blank = ttk.Label(stmain_frame, text = "", style = 'ThinBlank.TLabel').pack(fill = 'x')
    stlabel = ttk.Label(stmain_frame, text = "設定", justify = CENTER, style = 'Title.TLabel').pack()
    blank2 = ttk.Label(stmain_frame, text = "", style = 'ThinBlank.TLabel').pack(fill = 'x')
    blank3 = ttk.Label(stmain_frame, text = "").pack(fill = 'x')
    blank4 = ttk.Label(stmain_frame, text = "").pack(fill = 'x')
    stframe1 = LabelFrame(stmain_frame, text = "員工名單",font = tkFont.Font(family = '微軟正黑體', size = 12), padx = 5, pady = 5)
    text = Text(stframe1, height = 10, width = 25, wrap = NONE)
    m.name_list(gid)
    for n in m.names:
        text.insert(END, n+"\n")
    stsbar = ttk.Scrollbar(stframe1, orient = 'vertical', command = text.yview)
    stsbar.pack(side = RIGHT, fill = Y)
    text.pack(side = LEFT, fill = Y)
    text['yscrollcommand'] = stsbar.set
    
    stframe2 = ttk.Frame(stmain_frame)
    btn1 = ttk.Button(stframe2, text = "新增人員", command = addwin).pack()
    blank5 = ttk.Label(stframe2, text = "").pack(fill = 'x')
    btn2 = ttk.Button(stframe2, text = "刪除人員", command = removewin).pack()
    blank6 = ttk.Label(stframe2, text = "").pack(fill = 'x')
    btn3 = ttk.Button(stframe2, text = "返回", command = settingWin.destroy).pack()
    
    stframe1.pack(padx = 10, pady = 10, side = LEFT)
    stframe2.pack(side = LEFT)
    
    color(settingWin)
    color(stframe1)

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

def employee_list():
    m.name_list(gid)
    
    listWin = Toplevel(window)
    listWin.title('員工名單')
    color(listWin)
    
    menus(listWin)
    
    columns = ('#1')
    epylist = ttk.Treeview(listWin, columns = columns, show = 'headings')
    epylist.column(columns, anchor = 'center')
    epylist.heading('#1', text='Name')
    for name in m.names:
        epylist.insert('', END, values=name)
    scrollbar = ttk.Scrollbar(listWin, orient = VERTICAL, command = epylist.yview)
    epylist.configure(yscroll = scrollbar.set)
    scrollbar.pack(side = RIGHT, fill = Y)
    epylist.pack(side = LEFT)
    
def menus(win):
    menubar = Menu(win)
    filemenu = Menu(menubar)
    menubar.add_cascade(label="選單", menu = filemenu)
    filemenu.add_command(label="Setting", command = setting)
    filemenu.add_separator()
    filemenu.add_command(label="EmployeeList", command = employee_list)
    filemenu.add_separator()
    filemenu.add_command(label="Back", command = win.destroy)
    filemenu.add_command(label="Exit", command = window.destroy)
    win.config(menu=menubar)

def color(win):
    win['bg']='#ebd6a3'

#-----
window = Tk()
window.title("XX公司打卡系統")
window.state('zoomed')
window.minsize(600,400)

menus(window)

style = ttk.Style()
style.configure('TButton', font=("微軟正黑體", 12, 'bold'), foreground = '#1b2c5c', background = '#ebd6a3')
style.configure('TLabel', font=("微軟正黑體", 12, 'bold'), foreground = '#1b2c5c', background = '#ebd6a3')
style.configure('TFrame', background = '#ebd6a3')
style.configure('Title.TLabel', font=("微軟正黑體", 50, 'bold'), foreground = '#1b2c5c', background = '#ebd6a3')
style.configure('Blank.TLabel', font=("Gill Sans MT", 12, 'bold', 'italic'), foreground = '#ebd6a3', background = '#1b2c5c')
style.configure('ThinBlank.TLabel', font=("Gill Sans MT", 5, 'bold', 'italic'), foreground = '#ebd6a3', background = '#1b2c5c')

#main_frame
main_frame = ttk.Frame(window)
blank = ttk.Label(main_frame, text = "Welcome To", style = 'Blank.TLabel', anchor = 'center').pack(fill = 'x')
label = ttk.Label(main_frame, text = "XX公司打卡系統", style = 'Title.TLabel').pack()
blank2 = ttk.Label(main_frame, text = "Let's go!", style = 'Blank.TLabel', anchor = 'center').pack(fill = 'x')
blank3 = ttk.Label(main_frame, text = "").pack(fill = 'x')
label2 = ttk.Label(main_frame, text = "--")              #顯示訊息
label2.pack()

#sub1_frame
sub1_frame = ttk.Frame(main_frame)
sub1_frame.pack()
#frame1
frame1 = ttk.Frame(sub1_frame)
btn1 = ttk.Button(frame1, text = "上班", command = punchIn).pack()
text1 = Text(frame1, height = 15, width = 30, wrap = NONE)
text1.insert(END, m.db_check('punchin_db.sqlite'))    #最新資料顯示在上面
sbar1 = ttk.Scrollbar(frame1, orient = 'vertical', command = text1.yview)

#frame2
frame2 = ttk.Frame(sub1_frame)
btn2 = ttk.Button(frame2, text = "下班", command = punchOut).pack()
text2 = Text(frame2, height = 15, width = 30, wrap = NONE)
text2.insert(END, m.db_check('punchout_db.sqlite'))    #最新資料顯示在上面
sbar2 = ttk.Scrollbar(frame2, orient = 'vertical', command = text2.yview)

#sub2_frame
sub2_frame = ttk.Frame(main_frame)
blank4 = ttk.Label(sub2_frame, text = "").pack()
btn3 = ttk.Button(sub2_frame, text = "離開", command = window.destroy).pack(side = RIGHT)
btn4 = ttk.Button(sub2_frame, text = "設定", command = setting).pack(side = RIGHT)
sub2_frame.pack()

#-----
main_frame.place(relx=0.5, rely=0.5, anchor = CENTER)

frame1.pack(side = LEFT)
sbar1.pack(side = RIGHT, fill = Y)
text1.pack(side = LEFT, fill = Y)
text1['yscrollcommand'] = sbar1.set

frame2.pack(side = RIGHT)
sbar2.pack(side = RIGHT, fill = Y)
text2.pack(side = LEFT, fill = Y)
text2['yscrollcommand'] = sbar2.set

#-----
color(window)

#-----
window.mainloop()