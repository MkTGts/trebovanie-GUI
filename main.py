import logging
import os
import tkinter
from tkinter import ttk
from types import FunctionType
from datetime import datetime


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="a",
    encoding="utf-8",
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)


class Trebovanie:
    name_ = "Создание требовнаия"
    ver = "0.0.2"
    
    def __init__(self):
        self.root = tkinter.Tk()  # инициализация окна
        self.root.title(f"{__class__.name_} | {__class__.ver}")  # заголовок
        self.root.geometry("450x580+650+180")  # размер окна

        self.files = [file for file in os.listdir() if file.lower().endswith(".pdf")]  # список pdf файлов в директории
        self.combobox = ttk.Combobox(values=self.files)  # инициплизация выпадающего окна со списком файлов
        self.combobox.place(x=10, y=5)#pack(anchor="nw", padx=6, pady=6)  # позиционирование


    def refresh_files(self) -> None:
        self.files = [file for file in os.listdir() if file.lower().endswith(".pdf")]
        self.combobox = ttk.Combobox(values=self.files)  # инициплизация выпадающего окна со списком файлов
        self.combobox.place(x=10, y=5) #ack(anchor="nw", padx=6, pady=6) 

    
    def create_treb(self):
        pass


    def choos_org(self):
        org_list = {"lic": "ИП Ликинов", "sin": 'ООО ТД "Синтез"', "top": "ООО Топка", "est": "ООО Эстейт", "har_sv": "ИП Харитонов С.В."}  # список организаций
        self.org = tkinter.StringVar(value=org_list["lic"])  # какая организация будет выбираться изначально по умолчанию

        self.header_org = ttk.Label(text="Организация", font=("Arial", 14)) 
        self.header_org.place(x=240, y=40)

        lic_btn = ttk.Radiobutton(text=org_list["lic"], value=org_list["lic"], variable=self.org)
        lic_btn.place(x=240, y=80)
    
        sin_btn = ttk.Radiobutton(text=org_list["sin"], value=org_list["sin"], variable=self.org)
        sin_btn.place(x=240, y=110)

        top_btn = ttk.Radiobutton(text=org_list["top"], value=org_list["top"], variable=self.org)
        top_btn.place(x=240, y=140)

        est_btn = ttk.Radiobutton(text=org_list["est"], value=org_list["est"], variable=self.org)
        est_btn.place(x=240, y=170)

        har_sv_btn = ttk.Radiobutton(text=org_list["har_sv"], value=org_list["har_sv"], variable=self.org)
        har_sv_btn.place(x=240, y=200)


    def choos_type_treb(self):
        type_treb_list = {"fact": "По факту", "predop": "Предоплата"}
        self.type_treb = tkinter.StringVar(value=type_treb_list["predop"])

        self.header_type_treb = ttk.Label(text="Тип оплаты", font=("Arial", 14))
        self.header_type_treb.place(x=240, y=250)

        predop_btn = ttk.Radiobutton(text=type_treb_list["predop"], value=type_treb_list["predop"], variable=self.type_treb)
        predop_btn.place(x=240, y=290)

        fact_btn = ttk.Radiobutton(text=type_treb_list["fact"], value=type_treb_list["fact"], variable=self.type_treb)
        fact_btn.place(x=240, y=320)

    
    def _all_chooses(self):
        self.choos_org()
        self.choos_type_treb()

    

    def _frame_pay_day(self):
        self.frame_pay_day = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label0 = ttk.Label(self.frame_pay_day, text="День оплаты")
        name_label0.pack(anchor="nw")
        name_entry0 = ttk.Entry(self.frame_pay_day)
        name_entry0.pack(anchor="nw")
        self.frame_pay_day.place(x=20, y=40)

    
    def _frame_pay_month(self):
        self.frame_pay_month = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label1 = ttk.Label(self.frame_pay_month, text="Номер месяца оплаты")
        name_label1.pack(anchor="nw")
        name_entry1 = ttk.Entry(self.frame_pay_month)
        name_entry1.pack(anchor="nw")
        self.frame_pay_month.place(x=20, y=105)

    
    def _frame_pay_sum(self):
        self.frame_pay_sum = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label2 = ttk.Label(self.frame_pay_sum, text="Сумма")
        name_label2.pack(anchor="nw")
        name_entry2 = ttk.Entry(self.frame_pay_sum)
        name_entry2.pack(anchor="nw")
        self.frame_pay_sum.place(x=20, y=170)


    def _frame_pay_addres(self):
        self.frame_pay_addres = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label3 = ttk.Label(self.frame_pay_addres, text="Кому платим")
        name_label3.pack(anchor="nw")
        name_entry3 = ttk.Entry(self.frame_pay_addres)
        name_entry3.pack(anchor="nw")
        self.frame_pay_addres.place(x=20, y=235)


    def _frame_pay_info(self):
        self.frame_pay_info = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label4 = ttk.Label(self.frame_pay_info, text="Информация по платежу")
        name_label4.pack(anchor="nw")
        name_entry4 = ttk.Entry(self.frame_pay_info)
        name_entry4.pack(anchor="nw")
        self.frame_pay_info.place(x=20, y=300)

    
    def _frame_pay_comment(self):
        self.frame_pay_comment = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label5 = ttk.Label(self.frame_pay_comment, text="Комментарий")
        name_label5.pack(anchor="nw")
        name_entry5 = ttk.Entry(self.frame_pay_comment)
        name_entry5.pack(anchor="nw")
        self.frame_pay_comment.place(x=20, y=365)

    
    def _frame_pay_chet(self):
        self.frame_pay_chet = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label6 = ttk.Label(self.frame_pay_chet, text="Номер счета")
        name_label6.pack(anchor="nw")
        name_entry6 = ttk.Entry(self.frame_pay_chet)
        name_entry6.pack(anchor="nw")
        self.frame_pay_chet.place(x=20, y=430)
        
    
    def _frame_pay_date(self):
        self.frame_pay_date = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label7 = ttk.Label(self.frame_pay_date, text="Дата счета")
        name_label7.pack(anchor="nw")
        name_entry7 = ttk.Entry(self.frame_pay_date)
        name_entry7.pack(anchor="nw")
        self.frame_pay_date.place(x=240, y=365)

    
    def _frame_pay_filename(self):
        self.frame_pay_filename = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label8 = ttk.Label(self.frame_pay_filename, text="Название для конечного файла")
        name_label8.pack(anchor="nw")
        name_entry8 = ttk.Entry(self.frame_pay_filename)
        name_entry8.pack(anchor="nw")
        self.frame_pay_filename.place(x=240, y=430)

    
    def _all_frames(self):
        self._frame_pay_day()
        self._frame_pay_month()
        self._frame_pay_sum()
        self._frame_pay_addres()
        self._frame_pay_info()
        self._frame_pay_comment()
        self._frame_pay_chet()
        self._frame_pay_date()
        self._frame_pay_filename()


    
    def button(self, text: str, command: FunctionType, x: int, y: int):
        self.btn_create_treb = ttk.Button(text=text, command=command)
        self.btn_create_treb.place(x=x, y=y)


    def _all_buttons(self):
        self.button(text="Создать требование", command=self.create_treb, x=150, y=520)
        self.button(text="Обновить список фалов", command=self.refresh_files, x=170, y=5)



    def __call__(self, *args, **kwds):
        self._all_chooses()
        self._all_frames()
        self._all_buttons()
        self.root.mainloop()



def main():
    treb = Trebovanie()
    treb()


if __name__ == "__main__":
    main()