from tkinter import *
from tkinter import messagebox,filedialog,scrolledtext
from tkinter.ttk import *
import re
import requests
import ctypes
import os
import atexit

#解决高分辨率下模糊的问题
#调用api设置成由应用程序缩放
ctypes.windll.shcore.SetProcessDpiAwareness(1)
#调用api获得当前的缩放因子
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)

Path=''

def GetText():
    global bm
    global Path
    Clean()
    global text
    text=entry.get()
    text=text.strip()
    global font
    font=combobox.get()
    if font=='艺术':
        fonts='1.ttf'
    elif font=='连笔':
        fonts='zql.ttf'
    elif font=='商务':
        fonts='8.ttf'
    elif font=='楷书':
        fonts='6.ttf'
    elif font=='潇洒':
        fonts='bzcs.ttf'
    elif font=='草体':
        fonts='lfc.ttf'
    elif font=='行书':
        fonts='2.ttf'
    elif font=='个性':
        fonts='3.ttf'
    if text=='':
      messagebox.showerror('错误','输入不可为空！')
      return 0
    else:
        data={
            'word':text,
            'sizes':60,
            'fonts':fonts
        }
        w=requests.post('http://www.uustv.com/',data=data)
        w.encoding='utf-8'
        html=w.text 
        r='<div class="tu">.*?<img src="(.*?)"/></div>'
        image=re.findall(r,html)
        global imagedata
        imagedata=requests.get('http://www.uustv.com/'+image[0]).content
        Path='{}.gif'.format(text+'  '+font)
        f=open(Path,'wb')
        f.write(imagedata)
        bm=PhotoImage(file=Path)
        label4=Label(Write,image=bm)
        label4.bm=bm
        label4.grid(row=3,column=1,sticky='W')

@atexit.register
def Clean():
    if Path!='':
        os.remove(os.getcwd()+'\\'+Path)

def Exit():
    Clean()
    win.quit()
    win.destroy()
    exit()

def SaveGif():
    if GetText()==0:
        return
    SavePath=str(filedialog.asksaveasfilename(title='保存文件',defaultextension='.jpg',initialfile='{}.jpg'.format(text+'  '+font),filetypes=[('JPG', '.jpg')]))
    f=open(SavePath,'wb')
    f.write(imagedata)
    messagebox.showinfo('保存结果','保存成功！')

def ShowInfo():
    messagebox.showinfo('作者','YangguangZhou \n https://jzhome.vercel.app/')

win=Tk()
win.title('书法大师')
win.iconbitmap('resources/logo.ico')
#win.geometry("935x412")
win.resizable(0,0)

tabControl=Notebook(win)
tab1=Frame(tabControl) 
tabControl.add(tab1,text='书法')
tab2=Frame(tabControl)
tabControl.add(tab2,text='帮助')
tabControl.pack(expand=1,fill="both")

Write=LabelFrame(tab1,text='书法')
Write.grid(row=0,column=0,padx=8,pady=4)
label=Label(Write,text='文字：',font=('楷体',20))
label.grid(row=1,column=0,sticky='W')
entry=Entry(Write,font=('楷体',20))
entry.grid(row=1,column=1,sticky='W')
entry.insert(END,'书法大师')
label2=Label(Write,text='字体：',font=('楷体',20))
label2.grid(row=2,column=0,sticky='W')
combobox=Combobox(Write,font=('楷体',15),width=5,state='readonly')
combobox['value']=('艺术','连笔','商务','楷书','潇洒','草体','行书','个性')
combobox.current(0)
combobox.grid(row=2,column=1,sticky='W')
label3=Label(Write,text='书法作品：',font=('楷体',20))
label3.grid(row=3,column=0,sticky='W')
GetText()
label4=Label(Write,image=bm)
label4.bm=bm
label4.grid(row=3,column=1,sticky='W')
EnterImage=PhotoImage(file="resources/enter.gif")
EnterButton=Button(Write,image=EnterImage,command=GetText)
EnterButton.grid(row=4,column=2)
SaveImage=PhotoImage(file="resources/save.gif")
SaveButton=Button(Write,image=SaveImage,command=SaveGif)
SaveButton.grid(row=4,column=3)
InfoImage=PhotoImage(file="resources/info.gif")
InfoButton=Button(Write,image=InfoImage,command=ShowInfo)
InfoButton.grid(row=4,column=4)
ExitImage=PhotoImage(file="resources/exit.gif")
ExitButton=Button(Write,image=ExitImage,command=Exit)
ExitButton.grid(row=4,column=5)

Help=LabelFrame(tab2,text='帮助')
Help.grid(row=0,column=0,padx=8,pady=4)
h=scrolledtext.ScrolledText(Help,width=66,height=12,font=('楷体',12),relief=FLAT)
ht='''使用说明：\n
1、在文本框内输入文字
2、选择自己想要的字体
3、点击“确定”生成书法作品
4、点击“保存”按钮将书法作品保存到电脑上\n'''
h.config(state=DISABLED)
h.grid(row=1,column=0)
h.config(state=NORMAL)
h.insert(END,ht)
DemoImage=PhotoImage(file="resources/demo/demo.gif")
h.image_create('8.0',image=DemoImage)
h.config(state=DISABLED)
InfoButton2=Button(Help,image=InfoImage,command=ShowInfo)
InfoButton2.grid(row=2,column=2)
ExitButton2=Button(Help,image=ExitImage,command=Exit)
ExitButton2.grid(row=2,column=3)

win.mainloop()
