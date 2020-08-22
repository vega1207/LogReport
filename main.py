# coding=UTF-8
import glob
import os
import threading
import tkinter.messagebox
from threading import RLock
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory

from CustomerReportBuilding import *

LOCK = RLock()


class App():
  
  def __init__(self, root):
    self.root = root
    self.root.title('Report Generator V1.0.0 ©2020 VseA (Changshu) Co., Ltd')
    self.root.configure(bg="#c0ded9")
    self.root.wm_iconbitmap('icon.ico')
    self.root.geometry("560x330+400+150") 
    self.root.resizable(0,0)
    #======================================================Frame=================================================================    
    Mainframe = Frame(self.root,bd=10)
    Mainframe.grid()

    Tops = Frame(Mainframe,bd=0,width=100,height=350,relief=RIDGE)
    Tops.pack(side=TOP)

    Label(Tops, text='Excel Report Generator', font=('Arial', 20,'bold'),justify=CENTER).grid(padx=2)
    status = Label(Tops, text='waiting for your select...', bg="#c0ded9",font=('Arial', 12,'bold'),justify=CENTER)
    status.grid(pady=25)

    MembersPath = LabelFrame(Mainframe,bd=4, width =466,height=200,font=('Arial', 12),text='',relief=RIDGE)
    MembersPath.pack(side=TOP)

    ButtonFrame = LabelFrame(Mainframe,bd=2, width =466,height=20, font=('Arial', 12), text='',relief=RIDGE)
    ButtonFrame.pack(side=BOTTOM)

    margin = LabelFrame(Mainframe,bd=0, width =46,height=20, font=('Arial', 12), text='',relief=RIDGE)
    margin.pack(side=BOTTOM)

    #=======================================================Variables=================================================================    
    Entry_EOL = StringVar()
    Entry_Hipot = StringVar()
    Entry_GRR = StringVar()
    #=======================================================Function=================================================================
    def Reset():
      Entry_EOL.set("")
      Entry_Hipot.set("")
      Entry_GRR.set("")
      status['text'] ='waiting for your select...'
      status['bg'] = '#c0ded9'
      return

    def OpenEOLPath():
      EOLPath = askdirectory(initialdir=os.getcwd(),title='Please select a directory')
      if GetTotallfileNumber(EOLPath) >250:
        tkinter.messagebox.showinfo("Warnning","A total of files must less than or equal 250 in the folder!")
        return False
      else:
        if len(EOLPath)>0:
          Entry_EOL.set(EOLPath)
          return True
        else:
          return False

    def OpenHipotPath():
      HipotPath = askdirectory(initialdir=os.getcwd(),title='Please select a directory')
      if GetTotallfileNumber(HipotPath) >250:
        tkinter.messagebox.showinfo("Warnning","A total of files must less than or equal 250 in the folder!")
        return False
      else:
        if len(HipotPath)>0:
          Entry_Hipot.set(HipotPath)
          return True
        else:
          return False

    def OpenGRRPath():
      GRRPath = askdirectory(initialdir=os.getcwd(),title='Please select a directory')
      if GetTotallfileNumber(GRRPath) >250:
        tkinter.messagebox.showinfo("Warnning","A total of files must less than or equal 250 in the folder!")
        return False
      else:
        if len(GRRPath)>0:
          Entry_GRR.set(GRRPath)
          return True
        else:
          return False

    def GetTotallfileNumber(path=''):
      path_file_number=glob.glob(path +'/*.csv') #指定文件下个数
      return len(path_file_number)
    
    def Hipot_Builder():
      with LOCK:
        # start_time = time.process_time()
        HipotPath = Entry_Hipot.get()
        if len(HipotPath) >0:
          try:
            if HipotData_To_Report(HipotPath) ==None:
              # print("Total running time: ",time.process_time() - start_time)
              status['text'] ='Hipot report well done!'
              status['bg'] = 'green'
              return tkinter.messagebox.showinfo("Good","Hipot data finished!")
            else:
              return tkinter.messagebox.showinfo("Warnning","Some test items missed in the log!")
          except FileNotFoundError:
            status['text'] ='waiting for your select...'
            status['bg'] = '#c0ded9'
            tkinter.messagebox.showinfo("Warnning","Please select correctly path...")
            return False
        else:
          tkinter.messagebox.showinfo("Warnning","Please select the Hipot path!")
          return False

    def EOL_Builder():
      with LOCK:
        # start_time = time.process_time()
        EOLPath = Entry_EOL.get()
        if len(EOLPath) >0:
          try:
            if Customer_Report(EOLPath) ==None:
              # print("Total running time: ",time.process_time() - start_time)
              status['text'] ='EOL report well done!'
              status['bg'] = 'green'
              return tkinter.messagebox.showinfo("Good","EOL data finished!")
            else:
              return tkinter.messagebox.showinfo("Warnning","Some test items missed in the log!")
          except FileNotFoundError:
            status['text'] ='waiting for your select...'
            status['bg'] = '#c0ded9'
            tkinter.messagebox.showinfo("Warnning","Please select correctly path...")
            return False
        else:
          tkinter.messagebox.showinfo("Warnning","Please select the EOL path!")
          return False
    
    def GRR_Builder():
      with LOCK:
        # start_time = time.process_time()
        GRRPath = Entry_GRR.get()
        if len(GRRPath) >0:
          try:
            if GRR_Data(GRRPath) ==None:
              # print("Total running time: ",time.process_time() - start_time) 
              status['text'] ='GRR report well done!'
              status['bg'] = 'green'
              return tkinter.messagebox.showinfo("Good","GRR data finished!")
            else:
              return tkinter.messagebox.showinfo("Warnning","Some test items missed in the log!")
          except FileNotFoundError:
            status['text'] ='waiting for your select...'
            status['bg'] = '#c0ded9'
            tkinter.messagebox.showinfo("Warnning","Please select correctly path...")
            return False
        else:
          tkinter.messagebox.showinfo("Warnning","Please select the GRR path!")
          return False
      
    #=======================================================Threading=================================================================
    def EOLpathThreading():
      EOLPath = Entry_EOL.get()
      if len(EOLPath) ==0:
        status['text'] ='waiting for your select...'
        status['bg'] = '#c0ded9'
        tkinter.messagebox.showinfo("Warnning","Please select the EOL path!")
      else:
        status['text'] ='EOL report Ongoing...'
        status['bg'] = 'yellow'
        EOLpath_Threading = threading.Thread(target=EOL_Builder)
        EOLpath_Threading.start()

    def GRRpathThreading():
      GRRPath = Entry_GRR.get()
      if len(GRRPath) ==0:
        status['text'] ='waiting for your select...'
        status['bg'] = '#c0ded9'
        tkinter.messagebox.showinfo("Warnning","Please select the GRR path!")
      else:
        status['text'] ='GRR report Ongoing...'
        status['bg'] = 'yellow'
        GRRpath_Threading = threading.Thread(target=GRR_Builder)
        GRRpath_Threading.start()
      
    def HipotpathThreading():
      HipotPath = Entry_Hipot.get()
      if len(HipotPath) ==0:
        status['text'] ='waiting for your select...'
        status['bg'] = '#c0ded9'
        tkinter.messagebox.showinfo("Warnning","Please select the Hipot path!")
      else:
        status['text'] ='Hipot report Ongoing...'
        status['bg'] = 'yellow'
        Hipotpath_Threading = threading.Thread(target=Hipot_Builder)
        Hipotpath_Threading.start()
    
    #=======================================================Label & Entry=================================================================

    self.btnEOLPath = Button(MembersPath,padx=18,bd=7,font=('Arial', 10,'bold'),width=7,text="EOL Path", command=OpenEOLPath, bg="#c0ded9")
    self.btnEOLPath.grid(row=0,column=0,pady=2)  #
    self.txtNumberOne = Entry(MembersPath,font=('Arial', 13,'bold'), bd=7,text= Entry_EOL, width=34)
    self.txtNumberOne.grid(row=0,column=1)

    self.btnHipotPaht = Button(MembersPath,padx=18,bd=7,font=('Arial',10,'bold'),width=7,text="Hipot Path", command= OpenHipotPath, bg="#c0ded9")
    self.btnHipotPaht.grid(row=1,column=0,pady=2) #
    self.txtNumberTwo = Entry(MembersPath,font=('Arial', 13,'bold'), bd=7,text= Entry_Hipot, width=34)
    self.txtNumberTwo.grid(row=1,column=1)

    self.btnGRR = Button(MembersPath,padx=18,bd=7,font=('Arial',10,'bold'),width=7,text="GRR Path", command= OpenGRRPath, bg="#c0ded9")
    self.btnGRR.grid(row=2,column=0,pady=2) #
    self.txtNumerThree = Entry(MembersPath,font=('Arial', 13,'bold'), bd=7,text= Entry_GRR, width=34)
    self.txtNumerThree.grid(row=2,column=1)

    #=======================================================Button===========================================================================================================
    self.btnRest = Button(ButtonFrame,padx=18,bd=7,font=('Arial', 10,'bold'),width=7,text="Reset",command=Reset, bg="#c0ded9")
    self.btnRest.grid(row=10,column=3,padx=12)
    self.btnHipotStart = Button(ButtonFrame,padx=18,bd=7,font=('Arial', 10,'bold'),width=7,text="Hipot Builder",command=HipotpathThreading, bg="#c0ded9")
    self.btnHipotStart.grid(row=10,column=2,padx=12)
    self.btnGRRStart = Button(ButtonFrame,padx=18,bd=7,font=('Arial', 10,'bold'),width=7,text="GRR Builder",command=GRRpathThreading, bg="#c0ded9")
    self.btnGRRStart.grid(row=10,column=0,padx=12)
    self.btnEOLStart = Button(ButtonFrame,padx=18,bd=7,font=('Arial', 10,'bold'),width=7,text="EOL Builder",command= EOLpathThreading, bg="#c0ded9")
    self.btnEOLStart.grid(row=10,column=1,padx=12)

 
if __name__ == '__main__':
  root = Tk()
  app = App(root)
  root.mainloop()
