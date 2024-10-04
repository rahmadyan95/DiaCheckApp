
import customtkinter as ctk
from tkinter import *
from customtkinter import *
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import tkinter as tk
import seaborn as sns
from CTkTable import *
import pandas as pd
from tkinter import ttk
from engine import prediction,generative_text
import time


class App (ctk.CTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Dashboard,Page1):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            

        # self.show_frame(Dashboard)
        self.show_frame(Dashboard)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self._set_appearance_mode('light')

        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.first_run = True

        self.box  = CTkLabel(self,width=1000,height=788,bg_color='white',fg_color='white',text='')
        self.box.place(x=0,y=0)

        self.innerbox = CTkLabel(self.box,height=745,width=960,fg_color='#AECBD6',corner_radius=10,text='')
        self.innerbox.place(x=20,y=20)

        self.right_box = CTkLabel(self.innerbox,height=745,width=480,fg_color='#BFD4DB',corner_radius=20,text='')
        self.right_box.place(x=490,y=0)

        self.title1 = CTkLabel(self.innerbox,text='Diabetes',font=('Arial Bold',38),text_color='white')
        self.title1.place(x=130,y=20)

        self.title2 = CTkLabel(self.innerbox,text='Prediction',font=('Arial Bold',38),text_color='white',
                               bg_color='transparent',fg_color='transparent',height=3)
        self.title2.place(x=130,y=60)

      

        logo_directory_home = os.path.join(self.script_dir, 'asset_app', 'book.png')
        logo_home = CTkImage(light_image=Image.open(logo_directory_home), size=(100,100))
        logo_placeholder_home = CTkButton(self.innerbox, image=logo_home, fg_color='transparent', text='',
                                        hover_color='#926565', height=90, width=100, state='disabled')
        logo_placeholder_home.place(x=15, y=10)

        self.long_line(self.innerbox,450,4,20,115,'white')

        self.input_box = CTkLabel(self.innerbox,height=590,width=440,fg_color='white',bg_color='transparent',corner_radius=10,text='')
        self.input_box.place(x=25,y=135)

        self.title3 = CTkLabel(self.input_box,text='Please Input Data Bellow',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        self.title3.place(x=20,y=20)

        self.long_line(self.input_box,390,4,20,50,'black')

        

        self.input_field()
        self.running_systemlog()

        self.terminal = CTkScrollableFrame(self.box,height=240,width=370,orientation='vertical',fg_color='gray10')
        self.terminal.place(x=20,y=130)
        


    def long_line(self,position,width,height,x_position,y_position,fgcolor) :
        long_line = CTkFrame(position,width=width,height=height,fg_color=fgcolor,corner_radius=0)
        long_line.place(x=x_position,y=y_position)

        


    def input_field(self):

        __title1 = CTkLabel(self.input_box,text='Input Your Gender',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title1.place(x=25,y=80)

        __title1_add = CTkLabel(self.input_box,text='0 = Female, 1 = Male',font=('Arial',14),text_color='grey',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title1_add.place(x=25,y=100)

        self.jenis_kelamin = CTkOptionMenu(self.input_box,values=['0','1'],height=35,width=100, corner_radius=5,fg_color='#AECBD6',
                                           font=('Arial Bold',16),text_color='white',button_color='grey20')
        self.jenis_kelamin.place(x=295,y=85)

        __title2 = CTkLabel(self.input_box,text='Input Your Age',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title2.place(x=25,y=140)

        __title1_add_2 = CTkLabel(self.input_box,text='Integer Input Only',font=('Arial',14),text_color='grey',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title1_add_2.place(x=25,y=160)

        self.umur = CTkEntry(self.input_box,height=35,width=100,text_color='white',fg_color='#AECBD6',font=('Arial Bold',16))
        self.umur.place(x=295,y=140)

        __title3 = CTkLabel(self.input_box,text='Have Hypertension ? ',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title3.place(x=25,y=200)

        __title1_add_3 = CTkLabel(self.input_box,text='Click to change',font=('Arial',14),text_color='grey',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title1_add_3.place(x=25,y=220)

        self.hipertensi = CTkCheckBox(self.input_box,height=35,width=100,text_color='white',fg_color='#AECBD6',onvalue=1,offvalue=0)
        self.hipertensi.place(x=330,y=200)

        __title4 = CTkLabel(self.input_box,text='Have heart disease ? ',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title4.place(x=25,y=260)

        __title1_add_4 = CTkLabel(self.input_box,text='Click to change',font=('Arial',14),text_color='grey',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title1_add_4.place(x=25,y=280)

        self.sakit_jantung = CTkCheckBox(self.input_box,height=35,width=100,text_color='white',fg_color='#AECBD6',onvalue=1,offvalue=0)
        self.sakit_jantung.place(x=330,y=260)

        __title5 = CTkLabel(self.input_box,text='Have Smoking ? ',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title5.place(x=25,y=320)

        __title1_add_5 = CTkLabel(self.input_box,text='Click to change',font=('Arial',14),text_color='grey',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title1_add_5.place(x=25,y=340)

        self.smoking = CTkCheckBox(self.input_box,height=35,width=100,text_color='white',fg_color='#AECBD6',onvalue=1,offvalue=0)
        self.smoking.place(x=330,y=320)

        # bmi

        __title6 = CTkLabel(self.input_box,text='Input Your BMI Score',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title6.place(x=25,y=380)

        __title1_add_6 = CTkLabel(self.input_box,text='Decimal Input Only',font=('Arial',14),text_color='grey',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title1_add_6.place(x=25,y=400)

        self.bmi = CTkEntry(self.input_box,height=35,width=100,text_color='white',fg_color='#AECBD6',font=('Arial Bold',16))
        self.bmi.place(x=295,y=380)

        # BMI

        'HbA1c_level'
        __title7 = CTkLabel(self.input_box,text='HbA1c_level',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title7.place(x=25,y=440)

        __title1_add_7 = CTkLabel(self.input_box,text='Decimal Input Only',font=('Arial',14),text_color='grey',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title1_add_7.place(x=25,y=460)

        self.HbA1c_level = CTkEntry(self.input_box,height=35,width=100,text_color='white',fg_color='#AECBD6',font=('Arial Bold',16))
        self.HbA1c_level.place(x=295,y=440)
        'blood_glucose_level'

        __title8 = CTkLabel(self.input_box,text='Input Your Glucose level',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title8.place(x=25,y=500)

        __title1_add_8 = CTkLabel(self.input_box,text='Integer Input Only',font=('Arial',14),text_color='grey',
                               bg_color='transparent',fg_color='transparent',height=3)
        __title1_add_8.place(x=25,y=520)

        self.glukosa = CTkEntry(self.input_box,height=35,width=100,text_color='white',fg_color='#AECBD6',font=('Arial Bold',16))
        self.glukosa.place(x=295,y=500)

    def running_systemlog(self):
        # BOX Placing
        self.box = CTkLabel(self.right_box,height=400,width=430,fg_color='white',bg_color='transparent',text='',corner_radius=10)
        self.box.place(x=20,y=20)

        start_button = CTkButton(self.box,text='Start Predicting',height=50,width=410,fg_color='#D2E7D6',corner_radius=10,text_color='black',
                                 font=('Arial Bold',18),command=self.pridiksi)
        start_button.place(x=10,y=10)

        title3 = CTkLabel(self.box,text='Terminal Log',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        title3.place(x=20,y=80)

        self.long_line(self.box,390,4,20,110,'black')

        # Box resulst 

        self.resBox = CTkLabel(self.right_box,width= 430, height= 120,fg_color='white',corner_radius=10,text='Please Input parameter')
        self.resBox.place(x=20,y=430)

        self.warning_status = CTkLabel(self.resBox,text='Please Input parameter',font=('Arial Bold',22),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        self.warning_status.place(x=95,y=50)
# 170
        self.suggestion_box = CTkLabel(self.right_box,width=430, height= 170,fg_color='white',corner_radius=10,text='Please Input parameter')
        self.suggestion_box.place(x=20,y=560)

        self.titlesuggest = CTkLabel(self.suggestion_box,text='Suggestion',font=('Arial Bold',18),text_color='grey10',
                               bg_color='transparent',fg_color='transparent',height=3)
        self.titlesuggest.place(x=20,y=15)

        self.value_box = CTkScrollableFrame(self.suggestion_box,width=370,bg_color='white',fg_color='white')
        self.value_box.place(x=20,y=40)

        self.value_suggest = CTkLabel(self.value_box,bg_color='transparent',fg_color='transparent',text='',
                              font=('consolas',12),text_color='grey10')
        self.value_suggest.pack(padx=1,pady=1,anchor=W)


    def pridiksi(self):

        ins = prediction()
        self.utils = ins.run_prediction()

        age=int(self.umur.get()),
        blood_glucose_level=int(self.glukosa.get()),
        HbA1c_level=float(self.HbA1c_level.get()),
        smoking_history=int(self.smoking.get()),
        bmi=float(self.bmi.get()),
        heart_disease=int(self.sakit_jantung.get()),
        hypertension=int(self.hipertensi.get()),
        gender=int(self.jenis_kelamin.get())
    
        status = ins.create_data_tuple(age=int(self.umur.get()),
        blood_glucose_level=int(self.glukosa.get()),
        HbA1c_level=float(self.HbA1c_level.get()),
        smoking_history=int(self.smoking.get()),
        bmi=float(self.bmi.get()),
        heart_disease=int(self.sakit_jantung.get()),
        hypertension=int(self.hipertensi.get()),
        gender=int(self.jenis_kelamin.get())
        )


        self.get_data()
        self.destroyall()
        self.terminal_log()

        self.warning = CTkLabel(self.resBox,width=410, height= 100,fg_color='white',bg_color='transparent',corner_radius=10,text='Please Input parameter')
        self.warning.place(x=10,y=10)

        self.info_text = CTkLabel(self.warning,fg_color='white',bg_color='transparent',corner_radius=10,text='',font=('Arial Bold',24),
                                  text_color='black')
        self.info_text.place(x=115,y=40)

        suggestion = generative_text()
        res = suggestion.generate_suggestion(age=age,hypertension_status=hypertension,
                                       smoking_status=smoking_history,bmi=bmi,
                                       hb_level=HbA1c_level,glucose_level=blood_glucose_level,status=status,lenght_word_cut=50,heart_disaes_status=heart_disease)

        if status == False :


            try : 
                logo_placeholder_True.destroy()
                self.value_suggest.destroy()

            except :
                pass
            
            self.warning.configure(fg_color='#95D2B3',bg_color='#95D2B3',text='')
            self.info_text.configure(text='No Diabetes Detected',fg_color='#95D2B3',bg_color='#95D2B3')
            logo_directory_home = os.path.join(self.script_dir, 'asset_app', 'checklist.png')

            self.value_suggest.configure(text=res)

            print(res)

            
                

            logo_home = CTkImage(light_image=Image.open(logo_directory_home), size=(90,90))
            logo_placeholder_False = CTkButton(self.warning, image=logo_home, fg_color='transparent', text='',
                                            hover_color='#926565', height=90, width=100, state='disabled')
            logo_placeholder_False.place(x=10, y=5)

        else : 
            self.warning.configure(fg_color='#FF6961',bg_color='#FF6961',text='')
            self.info_text.configure(text='Diabetes Detected',fg_color='#FF6961',bg_color='#FF6961')

            logo_directory_home = os.path.join(self.script_dir, 'asset_app', 'warning.png')

            try : 
                logo_placeholder_False.destroy()
                self.value_suggest.destroy()

            except :
                pass

            logo_home = CTkImage(light_image=Image.open(logo_directory_home), size=(90,90))
            logo_placeholder_True = CTkButton(self.warning, image=logo_home, fg_color='transparent', text='',
                                            hover_color='#926565', height=90, width=100, state='disabled')
            logo_placeholder_True.place(x=10, y=5)


    
    def get_data(self):
        data_dict = {
            "Age": self.umur.get(),
            "Blood Glucose Level": self.glukosa.get(),
            "HbA1c Level": self.HbA1c_level.get(),
            "Smoking History": self.smoking.get(),
            "BMI": self.bmi.get(),
            "Heart Disease": self.sakit_jantung.get(),
            "Hypertension": self.hipertensi.get(),
            "Gender": self.jenis_kelamin.get()
        }

        df = pd.DataFrame([data_dict])
        return df
    
    def destroyall(self):
        if self.first_run:
            print('OK')
            self.first_run = False
        else :
            self.labellog.destroy()
            self.label_24.destroy()
            self.preprocessing.destroy()
            self.label_25.destroy()
            self.label_2.destroy()
            self.label_3.destroy()
            self.label_27.destroy()
            self.label_28.destroy()
            self.label_4.destroy()
            self.label_30.destroy()

        


    def terminal_log(self):
        
        self.labellog = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',text='System Start',
                              font=('consolas',12),text_color='green')
        self.labellog.pack(padx=1,pady=1,anchor=W)

        self.label_24 = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',
                                text=f'===============================================================',font=('consolas',12))
        self.label_24.pack(padx=1,pady=1,anchor=W)

        data = self.get_data()


        self.label_24 = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',
                                text=f'{data}',font=('consolas',12))
        self.label_24.pack(padx=1,pady=1,anchor=W)

        self.label_30 = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',
                                text=f'===============================================================',font=('consolas',12))
        self.label_30.pack(padx=1,pady=1,anchor=W)

        

        self.preprocessing = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',
                                text=f'',font=('consolas',12))
        self.preprocessing.pack(padx=1,pady=1,anchor=W)

        self.label_25 = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',
                                text=f'===============================================================',font=('consolas',12))
        self.label_25.pack(padx=1,pady=1,anchor=W)


        status = [
            'Reading Dataset',
            'Encoding Starting',
            'Encoding Succesfull',
            'Standarization Dataset Starting',
            'Standarization Dataset Successfull',
            'Dimentional Reduction Starting',
            'Dimentional Reduction Succesfull',
            'Training Starting',
            'Training Sucessfull'
        ]

        for status in status :
            self.preprocessing.configure(text=f'{status}')
            self.terminal.update()
            time.sleep(0.7)


        



        self.label_2 = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',
                                text=f'Null Data Set Check:\n{self.utils[0]}',font=('consolas',12))
        self.label_2.pack(padx=1,pady=1,anchor=W)

        self.label_26 = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',
                                text=f'===============================================================',font=('consolas',12))
        self.label_26.pack(padx=1,pady=1,anchor=W)



        self.label_3 = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',text=f'XGBoost Accuracy {round((self.utils[1]*100),2)} %',
                              font=('consolas',12))
        self.label_3.pack(padx=1,pady=1,anchor=W)

        self.label_27 = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',
                                text=f'===============================================================',font=('consolas',12))
        self.label_27.pack(padx=1,pady=1,anchor=W)

        self.label_4 = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',text=f'XGBoost Classification Report:\n{self.utils[2]}',
                              font=('consolas',12))
        self.label_4.pack(padx=1,pady=1,anchor=W)

        self.label_28 = CTkLabel(self.terminal,bg_color='transparent',fg_color='transparent',
                                text=f'===============================================================',font=('consolas',12))
        self.label_28.pack(padx=1,pady=1,anchor=W)

        
class Page1(ctk.CTkFrame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self._set_appearance_mode('light')


if __name__ == '__main__' :
    app = App()
    app.title('Diabetes Prediction')
    app.geometry("1000x788")
    app._set_appearance_mode("dark")
    app.resizable(False,False)
    app.mainloop()