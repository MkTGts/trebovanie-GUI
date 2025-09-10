import sys
import os
import logging
from pathlib import Path

# 1. Установка рабочей директории (САМОЕ ПЕРВОЕ ДЕЙСТВИЕ)
if getattr(sys, 'frozen', False):
    # Режим EXE - рабочая директория = где лежит EXE файл
    os.chdir(os.path.dirname(sys.executable))
    os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']    
else:
    # Режим разработки - рабочая директория = где лежит скрипт
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

def resource_path(relative_path):
    """Получение правильного пути к ресурсам"""
    try:
        if getattr(sys, 'frozen', False):
            # Проверяем во временной папке PyInstaller
            try:
                base_path = sys._MEIPASS
                temp_path = os.path.join(base_path, relative_path)
                if os.path.exists(temp_path):
                    return temp_path
            except AttributeError:
                pass
        # Если не найдено, используем рабочую директорию
        return os.path.join(os.getcwd(), relative_path)
    except Exception as e:
        logging.error(f"Ошибка в resource_path: {e}")
        return relative_path




import logging
import os
import tkinter
from tkinter import ttk
from types import FunctionType
from datetime import datetime
from docxtpl import DocxTemplate
from docx2pdf import convert
from os import remove
from pypdf import PdfWriter


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="a",
    encoding="utf-8",
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)



class PDFFunctional:
    def __init__(self, context: dict, del_input_file=True):
        self.context = context
        self.types_pay = {
                    "Предоплата": "data\startPred.docx",
                    "По факту": "data\startFact.docx" 
                 }
        self.del_input_file = del_input_file


    def write_docx(self) -> None:  
        # иницилизация документа ворд
        try:
            doc = DocxTemplate(self.types_pay[self.context["pay"]])
            print("\n\n", self.types_pay[self.context["pay"]], "\n\n")
            doc.render(self.context)
            doc.save('temp\end.docx')
        except Exception as err:
            logger.error(f"Ошибка {err}. Класс PDFFunctial. Метод write_docx")


    # форматирует в пдф
    def convert_to_pdf(self) -> None:
        try:
            import sys
            import os
            from io import StringIO
            
            # Сохраняем оригинальные потоки
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            
            # Устанавливаем временные потоки
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            
            try:
                # Импортируем и выполняем после перенаправления
                from docx2pdf import convert
                convert("temp\end.docx", "temp\\1.pdf")
                
            finally:
                # Всегда восстанавливаем потоки
                sys.stdout = original_stdout
                sys.stderr = original_stderr
            
            # Удаляем файл
            if os.path.exists("temp\end.docx"):
                os.remove("temp\end.docx")
    
            logging.info("Сконвертировано в PDF успешно")
        except Exception as err:
            logger.error(f"Ошибка {err}. Класс PDFFunctial. Метод convert_to_pdf")

    # склеевает пдфы
    def mrg(self):
        try:
            from pypdf import PdfWriter
            merger = PdfWriter()

            merger.append("temp\\1.pdf")
            merger.append(self.context["payment"])
            self.res_file_name = f'res\{self.context["filename"]}.pdf'  # имя конечного склееного файла
            merger.write(self.res_file_name)
            merger.close()
            logging.info("Пдфы склеены Ok.")
        except Exception as err:
            logger.error(f"Ошибка {err}. Класс PDFFunctial. Метод mrg")


    # удаляет промежуточные пдф файлы
    def input_files_delitter(self):
        try:
            remove("temp\\1.pdf")
            #remove(self.types_pay[self.context["payment"]])
            remove(self.context["payment"])
        except Exception as err:
            logger.error(f"Ошибка {err}. Класс PDFFunctial. Метод input_files_delitter")


    def __call__(self, *args, **kwds):
        try:
            self.write_docx()
            self.convert_to_pdf()
            self.mrg()
            if not self.del_input_file:
                self.input_files_delitter()
        except Exception as err:
            logger.error(f"Ошибка {err}. Класс PDFFunctial")
    



class Trebovanie:
    name_ = "Создание требовнаия"
    ver = "0.1.5"
    
    def __init__(self):
        self.root = tkinter.Tk()  # инициализация окна
        self.root.title(f"{__class__.name_} | {__class__.ver}")  # заголовок
        self.root.geometry("450x580+650+180")  # размер окна
        self.input_file_path = ""  # инициализация переменной под путь к исходному файлу
        self.label = tkinter.Label(self.root, text="Файл не выбран")  # название выбранного файла, если он выбран
        self.label.place(x=120, y=8)  # положение инф о выбранном файле


    def select_file(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=(("PDF-файлы", "*.pdf"), ("Все файлы", "*.*"))
        )

        if file_path and file_path.endswith(".pdf"):
            view_file_path = file_path.split("/")[-1]  
            if len(view_file_path) >= 35:
                view_file_path = view_file_path[0:35] + "..."


            self.label.config(text=f"Выбранный файл: {view_file_path}")
            self.input_file_path = file_path  # выбран верный файл
        else:
            self.label.config(text="Файл не выбран")


    def refresh_files(self) -> None:
        self.files = [file for file in os.listdir("input") if file.lower().endswith(".pdf")]
        self.combobox = ttk.Combobox(values=self.files)  # инициплизация выпадающего окна со списком файлов
        self.combobox.place(x=10, y=5) #ack(anchor="nw", padx=6, pady=6) 


    def choose_org(self):
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


    def choose_type_treb(self):
        type_treb_list = {"fact": "По факту", "predop": "Предоплата"}
        self.type_treb = tkinter.StringVar(value=type_treb_list["predop"])

        self.header_type_treb = ttk.Label(text="Тип оплаты", font=("Arial", 14))
        self.header_type_treb.place(x=240, y=250)

        predop_btn = ttk.Radiobutton(text=type_treb_list["predop"], value=type_treb_list["predop"], variable=self.type_treb)
        predop_btn.place(x=240, y=290)

        fact_btn = ttk.Radiobutton(text=type_treb_list["fact"], value=type_treb_list["fact"], variable=self.type_treb)
        fact_btn.place(x=240, y=320)


    def choose_del_input_file(self):
        self.var_res_del_input_file = tkinter.IntVar()
        self.checkbox_del_input_file = tkinter.Checkbutton(self.root, text="Удалить исходный файл", variable=self.var_res_del_input_file, onvalue=0, offvalue=1)
        self.checkbox_del_input_file.place(x=20, y=30)

    
    def _all_chooses(self):
        self.choose_org()
        self.choose_type_treb()
        self.choose_del_input_file()


    def _return_text_month(self, data: str) -> str:
        '''if data.isdigit():
            if 1 <= int(data) <= 12:
                import calendar
                return calendar.month_name[int(data)]'''
        months = [
                "января", "февраля", "марта", "апреля", "мая", "июня",
                "июля", "августа", "сентября", "октября", "ноября", "декабря"
            ]
        try:
            return months[int(data.lstrip("0")) - 1]
        except Exception as err:
            print(f"ошибка {err}")
            return data

    

    def _frame_pay_day(self):
        self.frame_pay_day = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label0 = ttk.Label(self.frame_pay_day, text="День оплаты")
        name_label0.pack(anchor="nw")
        self.pay_day = ttk.Entry(self.frame_pay_day)
        self.pay_day.pack(anchor="nw")
        self.frame_pay_day.place(x=20, y=75)

    
    def _frame_pay_month(self):
        self.frame_pay_month = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label1 = ttk.Label(self.frame_pay_month, text="Номер месяца оплаты")
        name_label1.pack(anchor="nw")
        self.pay_month = ttk.Entry(self.frame_pay_month)
        self.pay_month.pack(anchor="nw")
        self.frame_pay_month.place(x=20, y=140)

    
    def _frame_pay_sum(self):
        self.frame_pay_sum = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label2 = ttk.Label(self.frame_pay_sum, text="Сумма")
        name_label2.pack(anchor="nw")
        self.pay_sum = ttk.Entry(self.frame_pay_sum)
        self.pay_sum.pack(anchor="nw")
        self.frame_pay_sum.place(x=20, y=205)


    def _frame_pay_addres(self):
        self.frame_pay_addres = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label3 = ttk.Label(self.frame_pay_addres, text="Кому платим                      ")
        name_label3.pack(anchor="nw")
        self.pay_addres = ttk.Entry(self.frame_pay_addres)
        self.pay_addres.pack(anchor="nw")
        self.frame_pay_addres.place(x=20, y=270)


    def _frame_pay_info(self):
        self.frame_pay_info = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label4 = ttk.Label(self.frame_pay_info, text="Информация по платежу")
        name_label4.pack(anchor="nw")
        self.pay_info = ttk.Entry(self.frame_pay_info)
        self.pay_info.pack(anchor="nw")
        self.frame_pay_info.place(x=20, y=335)

    
    def _frame_pay_comment(self):
        self.frame_pay_comment = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label5 = ttk.Label(self.frame_pay_comment, text="Комментарий")
        name_label5.pack(anchor="nw")
        self.pay_comment = ttk.Entry(self.frame_pay_comment)
        self.pay_comment.pack(anchor="nw")
        self.frame_pay_comment.place(x=20, y=400)

    
    def _frame_pay_chet(self):
        self.frame_pay_chet = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label6 = ttk.Label(self.frame_pay_chet, text="Номер счета")
        name_label6.pack(anchor="nw")
        self.pay_chet = ttk.Entry(self.frame_pay_chet)
        self.pay_chet.pack(anchor="nw")
        self.frame_pay_chet.place(x=20, y=465)
        
    
    def _frame_pay_date(self):
        self.frame_pay_date = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label7 = ttk.Label(self.frame_pay_date, text="Дата счета")
        name_label7.pack(anchor="nw")
        self.pay_date = ttk.Entry(self.frame_pay_date)
        self.pay_date.pack(anchor="nw")
        self.frame_pay_date.place(x=240, y=365)

    
    def _frame_pay_filename(self):
        self.frame_pay_filename = ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
        name_label8 = ttk.Label(self.frame_pay_filename, text="Название для конечного файла")
        name_label8.pack(anchor="nw")
        self.pay_filename = ttk.Entry(self.frame_pay_filename)
        self.pay_filename.pack(anchor="nw")
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
        self.btn = ttk.Button(text=text, command=command)
        self.btn.place(x=x, y=y)


    def _all_buttons(self):
        self.button(text="Создать требование", command=self.create_treb, x=150, y=540)
        self.button(text="Выбрать файл", command=self.select_file, x=20, y=5)


    def _get_manger_name(self):
        with open("data/manager_name", "r", encoding="utf-8") as file:
            return file.read()


    def get_response_datas(self):
        return {
            "payment": self.input_file_path,
            "pay": self.type_treb.get(),  # тип требования
            "organization": self.org.get(),  # организация
            "day": self.pay_day.get(),
            "month": self._return_text_month(data=self.pay_month.get()),
            "sum": self.pay_sum.get(),
            "contr_ag": self.pay_addres.get(),
            "info": self.pay_info.get(),
            "comment": self.pay_comment.get(),
            "num": self.pay_chet.get(),
            "date_num": self.pay_date.get(),
            "filename": self.pay_filename.get(),
            "date_res": datetime.strftime(datetime.now(), "%d.%m.%Y"),
            "manager_name": self._get_manger_name()
        }
    

    def create_treb(self):
        make_result_pdf_file = PDFFunctional(context=self.get_response_datas(), del_input_file=self.var_res_del_input_file.get())

        if self.input_file_path.endswith(".pdf"):
            try:
                make_result_pdf_file()

                self.label.config(text="Файл не выбран")
                self.input_file_path = ""

                import tkinter.messagebox as msgbox
                msgbox.showinfo("Success", "Требование успешно создано")
            except Exception as err:
                logger.error(f"Ошибка {err}. Класс Trebovanie.")
                
                import tkinter.messagebox as msgbox
                msgbox.showerror("Error", f"Произошла ошибка:\n{err}\n\nПодробности в logs.log")
        else:
            import tkinter.messagebox as msgbox
            msgbox.showinfo("Warning", "Не выбран PDF-файл")



    def __call__(self, *args, **kwds):
        try:
            self._all_chooses()
            self._all_frames()
            self._all_buttons()
            self.root.mainloop()

        except Exception as err:
            logger.error(f"Ошибка при вызове основного метода: {err}")




def main():
    temp_dir = ["data", "input", "res", "temp"]
    dirs = os.listdir()

    for d in temp_dir:
        if d not in dirs:
            os.mkdir(d)


    treb = Trebovanie()
    treb()


if __name__ == "__main__":
    main()