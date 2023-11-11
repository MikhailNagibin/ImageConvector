"""импорт нужных модулей"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import Image
import sys
import os

"""размеры всех основных окон"""
X, Y = 700, 700


"""главное окно"""



class Main_window(QMainWindow):
    def __init__(self, position):
        super().__init__()
        self.position = str(position).split(".")[-1][7:-1].split(", ")
        self.font = QFont()
        self.font.setPointSize(12)
        self.instructionwind = Instraction()
        self.nofolder = NotFound()
        self.initUI()

    """создание интерфейса основного окна"""

    def initUI(self):
        self.setGeometry(int(self.position[0]), int(self.position[1]) + 40, X, Y)
        self.setFixedSize(X, Y)
        self.setWindowTitle("convector")
        self.setStyleSheet(
            "background-color: rgb(50,50,50);border: 3px solid rgb(230,230,230);"
            "color: white;"
        )

        self.choose = QPushButton(self)
        self.choose.setText("Выбрать изображение")
        self.choose.setFont(self.font)
        self.choose.resize(X, 30)
        self.choose.move(0, (Y - 30) // 2 - 3)
        self.choose.clicked.connect(self.file)
        self.choose.setStyleSheet("background-color: rgb(100, 100, 100)")

        self.status_text = QLabel(self)
        self.status_text.resize(X - 150, 30)
        self.status_text.move(0, 0)
        self.status_text.setFont(self.font)

        self.instructionbtn = QPushButton(self)
        self.instructionbtn.resize(150 + 3, 30)
        self.instructionbtn.setText("Инструкция")
        self.instructionbtn.move(X - 150 - 3, 0)
        self.instructionbtn.clicked.connect(self.instructionwind.ran)
        self.instructionbtn.setStyleSheet("background-color: rgb(100, 100, 100)")
        self.instructionbtn.setFont(self.font)

        self.instruction = QLabel(self)
        self.instruction.resize(X, 100)
        self.instruction.move(0, (Y - 30) // 2 - 100)
        self.instruction.setText(
            "     В этом приложении можно выбрать изображение и конвектировать \n"
            "                                это изображение в другой формат.\n"
            "                                 Для этого нажмите на кнопку"
        )
        self.instruction.setFont(self.font)

        self.folderbtn = QPushButton(self)
        self.folderbtn.resize(X, 30)
        self.folderbtn.move(0, 456)
        self.folderbtn.setFont(self.font)
        self.folderbtn.clicked.connect(self.folder)
        self.folderbtn.setText("Выбрать папку")
        self.folderbtn.setStyleSheet("background-color: rgb(100, 100, 100)")

        self.instruction_part2 = QLabel(self)
        self.instruction_part2.resize(X, 100)
        self.instruction_part2.move(0, 359)
        self.instruction_part2.setText(
            "             Так же нажав на кнопку ниже вы можете выбрать папку с \n"
            "    изображениями, которые можно конвектировать в другой формат.\n "
            "Полученные изобажения будут храниться в отдельно созданной папке"
        )
        self.instruction_part2.setFont(self.font)
        self.btn_in_use = [self.choose, self.folderbtn]
        self.count = 0

    """переход на окно с конвертацией одного изображения в случаее нажатия кнопки 'self.choose'"""

    def file(self):
        self.file_name = QFileDialog.getOpenFileName()
        if self.file_name != ("", "") and self.file_name[0].split(".")[-1].upper() in [
            "BMP",
            "ESP",
            "GIF",
            "IM",
            "JPEG",
            "JPG",
            "MSP",
            "PCX",
            "PNG",
            "PPM",
            "TIFF",
            "WEBP",
            "ICO",
            "PSD",
            "TIF",
            "FAX",
        ]:
            self.hide()
            self.position = self.pos()
            self.changer = Changer(self.file_name, self.position)
            self.changer.show()
        else:
            self.status_text.setText("Выбирите другой файл")
            self.status_text.setStyleSheet("background-color: rgb(255, 0, 0)")

    """переход на окно с конвертацией папки с изображениями при нажатии на кнопку 'self.folderbtn'"""

    def folder(self):
        self.folder = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        if self.folder != "":
            self.hide()
            self.position = self.pos()
            self.folder_changer = FolderChanger(self.position, self.folder)
            self.folder_changer.show()
        else:
            self.status_text.setText("Выбирите папку")


"""окно преобразования изображения"""


class Changer(QMainWindow):
    def __init__(self, file, position):
        super().__init__()
        self.file_name = file
        self.file_path = file
        self.position = str(position).split(".")[-1][7:-1].split(", ")
        self.resultwind = Result()
        self.waringwind = Waring()
        self.nofolder = NotFound()
        self.font = QFont()
        self.font.setPointSize(9)
        self.unitUI()

    """создание интерфейса окна"""

    def unitUI(self):
        self.setGeometry(int(self.position[0]), int(self.position[1]) + 40, X, Y)
        self.setFixedSize(X, Y)
        self.setWindowTitle("convector")
        self.setStyleSheet(
            "background-color: rgb(50,50,50);"
            "border: 3px solid rgb(230,230,230);"
            "color: white;"
        )

        self.txt = QLabel(self)
        self.txt.resize(350, 40)
        self.txt.move(0, 0)
        self.txt.setText(
            f"Вы выбрали изображение формата {self.file_name[0].split('.')[-1]}"
        )
        self.txt.setFont(self.font)

        self.ex = QPushButton(self)
        self.ex.setText("Выбрать другой файл")
        self.ex.resize(350 + 3, 40)
        self.ex.move(350 - 3, 0)
        self.ex.clicked.connect(self.exit)
        self.ex.setFont(self.font)

        self.new_folderbtn = QPushButton(self)
        self.new_folderbtn.setText("Выбирете папку")
        self.new_folderbtn.resize(X // 2, 40)
        self.new_folderbtn.move(0, 40 - 3)
        self.new_folderbtn.clicked.connect(self.new_folder)
        self.new_folderbtn.setFont(self.font)
        self.new_folderbtn.setStyleSheet(
            "background-color: rgb(100, 100, 100);color: rgb(255, 255, 255);"
        )

        self.new_foldertext = QLabel(self)
        self.new_foldertext.setText(
            self.file_path[0][: -self.file_path[0][::-1].index("/") - 1]
        )
        self.new_foldertext.resize(X // 2 + 3, 40)
        self.new_foldertext.move(X // 2 - 3, 40 - 3)
        self.new_foldertext.setFont(self.font)

        self.text = QLabel(self)
        self.text.resize(250, 50)
        self.text.move(X - 250, 80 - 6)
        self.text.setText(
            "выберите новый тип изображения\n нажав на одну из кнопок ниже"
        )
        self.text.setFont(self.font)

        self.new_name = QLabel(self)
        self.new_name.setText("Выберите новое имя\nизображению в поле ниже")
        self.new_name.resize(230, 50)
        self.new_name.move(50, 80 - 6)
        self.new_name.setFont(self.font)

        self.new_file_name = QLineEdit(self)
        self.new_file_name.setText(self.file_name[0].split("/")[-1].split(".")[0])
        self.new_file_name.resize(330, 40)
        self.new_file_name.move(0, 130 - 9)
        self.new_file_name.setFont(self.font)

        try:
            self.pixmap = QPixmap(self.file_name[0])
            q = str(self.pixmap.size()).split("(")[1][:-1].split(", ")
            if int(q[0]) < int(q[1]):
                self.pixmap = self.pixmap.scaledToHeight(Y - 300)
            else:
                self.pixmap = self.pixmap.scaledToWidth(X - 200)
            self.image = QLabel(self)
            self.image.resize(self.pixmap.size())
            self.image.move(50, 225)
            self.image.setPixmap(self.pixmap)
        except Exception:
            pass

        self.bpm = QPushButton(self)
        self.gif = QPushButton(self)
        self.im = QPushButton(self)
        self.jpeg = QPushButton(self)
        self.msp = QPushButton(self)
        self.pcx = QPushButton(self)
        self.png = QPushButton(self)
        self.ppm = QPushButton(self)
        self.tiff = QPushButton(self)
        self.webp = QPushButton(self)
        self.ico = QPushButton(self)
        self.pdf = QPushButton(self)

        self.files_typs = [
            "BMP",
            "GIF",
            "IM",
            "JPEG",
            "MSP",
            "PCX",
            "PNG",
            "PPM",
            "TIFF",
            "WEBP",
            "ICO",
            "PDF",
        ]
        self.box_of_buttons = [
            self.bpm,
            self.gif,
            self.im,
            self.jpeg,
            self.msp,
            self.pcx,
            self.png,
            self.ppm,
            self.tiff,
            self.webp,
            self.ico,
            self.pdf,
        ]

        self.btn_in_use = [self.ex, self.new_folderbtn]
        self.count = 0

        self.multy = ["GIF", "PDF", "TIFF"]

        st = 140

        for el in self.box_of_buttons:
            el.setText(self.files_typs[self.box_of_buttons.index(el)])
            if (
                el.text().upper() != self.file_name[0].split(".")[-1].upper()
                and not (
                    el.text() == "JPEG"
                    and self.file_name[0].split(".")[-1].lower() == "jpg"
                )
                and not (
                    el.text() == "TIFF"
                    and self.file_name[0].split(".")[-1].lower() == "tif"
                )
            ):
                el.resize(100, 30)
                el.setStyleSheet(
                    "background-color: rgb(100, 100, 100);color: rgb(255, 255, 255);"
                )
                el.move(X - 100, st)
                st += 40
                el.setFont(self.font)
                self.btn_in_use.append(el)
                if el.text() in self.multy:
                    el.clicked.connect(self.multy_page)
                else:
                    el.clicked.connect(self.one_page)
            else:
                el.hide()
        self.btn_in_use[0].setStyleSheet(
            "background-color: rgb(255,255, 0);color: rgb(0,0, 255);"
        )

    """переход на главное окно"""

    def exit(self):
        self.hide()
        self.position = self.pos()
        self.main = Main_window(self.position)
        self.main.show()

    """конвертация изображений в формат, не поддерживающий многостроничные файлы"""

    def one_page(self):
        form = self.sender().text()
        try:
            imege = Image.open(self.file_name[0])
            i = 0
            imege.convert("RGB")
            imege.seek(i)
            imege.save(f"{self.creat_new_name()}.{form}", format=form)
            while True:
                i += 1
                try:
                    imege.seek(i)
                    imege.save(f"{self.creat_new_name()}({i + 1}).{form}", format=form)
                except EOFError:
                    break
            imege.close()
        except FileNotFoundError or FileNotFoundError:
            self.nofolder.ran()
            return
        except Exception:
            self.waringwind.ran()
            return
        self.resultwind.ran()

    """конвертация изображений в формат, который поддерживает многостроничные файлы"""

    def multy_page(self):
        try:
            form = self.sender().text()
            img = Image.open(self.file_name[0])
            s = []
            name = ""
            for el in self.file_name[0].split("/")[:-1]:
                name += el + "/"
            i = 0
            a = []
            img.seek(i)
            img.save(f"{name}asd.png", "png")
            s.append(Image.open(f"{name}asd.png"))
            a.append(f"{name}asd.png")
            while True:
                i += 1
                try:
                    img.seek(i)
                    img.save(f"{name}asd{i}.png", "png")
                    s.append(Image.open(f"{name}asd{i}.png"))
                    a.append(f"{name}asd{i}.png")
                except EOFError:
                    break
                except Exception:
                    self.waringwind.ran()
                    for el in a:
                        os.unlink(el)
                    return
            print(self.creat_new_name())
            s[0].save(
                f"{self.creat_new_name()}.{form}",
                form,
                save_all=True,
                append_images=s[1:],
            )
            img.close()
            for el in a:
                os.unlink(el)
        except FileNotFoundError or FileNotFoundError:
            self.nofolder.ran()
            return
        except Exception:
            self.waringwind.ran()
            return
        self.resultwind.ran()

    """новое имя файла"""

    def creat_new_name(self):
        return self.new_foldertext.text() + "/" + self.new_file_name.text()

    """запись новой папки, в которую будет загружаться файл"""

    def new_folder(self):
        time = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        if time != "":
            self.file_path = time + "/" + self.new_file_name.text()
            self.new_foldertext.setText(time)

    """обработка клавиатуры"""

    def keyPressEvent(self, event):
        self.btn_in_use[self.count % len(self.btn_in_use)].setStyleSheet(
            "background-color: rgb(100, 100, 100);color: rgb(255, 255, 255);"
        )
        if event.key() == Qt.Key_Down:
            self.new_file_name.setReadOnly(True)
            self.count += 1
            self.new_file_name.setReadOnly(False)
        elif event.key() == Qt.Key_Up:
            self.new_file_name.setReadOnly(True)
            self.count -= 1
            self.new_file_name.setReadOnly(False)
        elif event.key() == Qt.Key_Enter - 1:
            self.btn_in_use[self.count % len(self.btn_in_use)].click()
        self.btn_in_use[self.count % len(self.btn_in_use)].setStyleSheet(
            "background-color: rgb(255,255, 0);color: rgb(0, 0, 255);"
        )


"""окно преобразования папки с изображениями"""


class FolderChanger(QMainWindow):
    def __init__(self, pos, folder):
        super().__init__()
        self.position = str(pos).split(".")[-1][7:-1].split(", ")
        self.folder_path = folder
        self.files = os.listdir(folder).copy()
        self.flag = True
        self.resultwind = Result()
        self.waringwind = Waring()
        self.startingwind = Starting()
        self.notfoundwind = NotFound()
        self.font = QFont()
        self.font.setPointSize(9)
        self.start()

    """создание интерфейса"""

    def start(self):
        self.setGeometry(
            int(self.position[0]),
            int(self.position[1]) + 40,
            X,
            Y,
        )
        self.setFixedSize(X, Y)
        self.setWindowTitle("convector")
        self.setStyleSheet(
            "background-color: rgb(50,50,50);"
            "border: 3px solid rgb(230,230,230);"
            "color: white;"
        )

        self.change_file = QPushButton(self)
        self.change_file.resize(200, 40)
        self.change_file.move(X - 200, 0)
        self.change_file.setText("Выбрать другой файл")
        self.change_file.clicked.connect(self.exit)
        self.change_file.setFont(self.font)

        self.text1 = QLabel(self)
        self.text1.resize(350, 30)
        self.text1.setText("Выбирите название новой папки в поле снизу")
        self.text1.setFont(self.font)

        self.new_folder_name = QLineEdit(self)
        self.new_folder_name.resize(350, 30)
        self.new_folder_name.move(0, 30 - 3)
        self.new_folder_name.setText(self.create_name())
        self.new_folder_name.setFont(self.font)

        self.new_folder_name_btn = QPushButton(self)
        self.new_folder_name_btn.resize(350, 30)
        self.new_folder_name_btn.move(0, 60 - 6)
        self.new_folder_name_btn.setText("Или выбирите уже существующую папку")
        self.new_folder_name_btn.clicked.connect(self.new_folder)
        self.new_folder_name_btn.setFont(self.font)

        self.text = QLabel(self)
        self.text.resize(250, 50)
        self.text.move(X - 250, 40 - 3)
        self.text.setText(
            "выберите новый тип изображения\n нажав на одну из кнопок ниже"
        )
        self.text.setFont(self.font)

        self.bpm = QPushButton(self)
        self.gif = QPushButton(self)
        self.im = QPushButton(self)
        self.jpeg = QPushButton(self)
        self.msp = QPushButton(self)
        self.pcx = QPushButton(self)
        self.png = QPushButton(self)
        self.ppm = QPushButton(self)
        self.tiff = QPushButton(self)
        self.webp = QPushButton(self)
        self.ico = QPushButton(self)
        self.pdf = QPushButton(self)

        self.files_typs = [
            "BMP",
            "GIF",
            "IM",
            "JPEG",
            "MSP",
            "PCX",
            "PNG",
            "PPM",
            "TIFF",
            "WEBP",
            "ICO",
            "PDF",
        ]
        self.box_of_buttons = [
            self.bpm,
            self.gif,
            self.im,
            self.jpeg,
            self.msp,
            self.pcx,
            self.png,
            self.ppm,
            self.tiff,
            self.webp,
            self.ico,
            self.pdf,
        ]

        self.multy = ["GIF", "PDF", "TIFF"]

        st = 110
        self.btn_in_use = [self.change_file, self.new_folder_name_btn]
        for i in range(len(self.box_of_buttons)):
            self.box_of_buttons[i].resize(100, 30)
            self.box_of_buttons[i].setText(self.files_typs[i])
            self.box_of_buttons[i].move(X - 100, st)
            self.btn_in_use.append(self.box_of_buttons[i])
            st += 50
            self.box_of_buttons[i].setFont(self.font)
            if self.box_of_buttons[i].text() in self.multy:
                self.box_of_buttons[i].clicked.connect(self.multy_page)
            else:
                self.box_of_buttons[i].clicked.connect(self.one_page)
        self.btn_in_use[0].setStyleSheet(
            "background-color: rgb(255,255, 0);color: rgb(0, 0, 255)"
        )
        for el in self.btn_in_use[1:]:
            el.setStyleSheet("background-color: rgb(100, 100, 100)")
        self.count = 0

    """запись пути уже существующей папки, для записи файлов в неё"""

    def new_folder(self):
        self.t = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        if self.t != "":
            self.new_folder_name.setText(self.t.split("/")[-1])
            self.flag = False

    """переход на главный экран"""

    def exit(self):
        self.hide()
        self.position = self.pos()
        self.main = Main_window(self.position)
        self.main.show()

    """запись имени для новой папки"""

    def create_name(self):
        i = 1
        while True:
            self.name = self.folder_path + f"({i})"
            if self.name.split("/")[-1] not in os.listdir(
                self.folder_path[: -self.folder_path[::-1].index("/")][:-1]
            ):
                return self.name.split("/")[-1]
            i += 1

    """создание новой папки"""

    def create_folder(self):
        if self.flag:
            os.mkdir(self.creat_new_name_of_folder())

    """запись пути папки"""

    def creat_new_name_of_folder(self):
        ans = ""
        for el in self.folder_path.split("/")[:-1]:
            ans += el + "/"
        return ans + self.new_folder_name.text()

    """создание файлов в формат, который не поддерживает многостроничные файлы"""

    def one_page(self):
        try:
            self.startingwind.ran()
            form = self.sender().text()
            self.create_folder()
            for el in self.files:
                try:
                    im = Image.open(f"{self.folder_path}/{el}")
                    i = 0
                    im.seek(i)
                    im.save(
                        f'{self.creat_new_name_of_folder()}/{el.split(".")[0]}.{form}',
                        format=form,
                    )
                    while True:
                        i += 1
                        try:
                            im.seek(i)
                            im.save(
                                f'{self.creat_new_name_of_folder()}/{el.split(".")[0]}({i + 1}).{form}',
                                format=form,
                            )
                        except EOFError:
                            break
                        except Exception:
                            self.waringwind.ran()
                    im.close()
                except:
                    pass
            self.resultwind.ran()
        except FileNotFoundError or FileNotFoundError:
            self.nofolder.ran()
            return
        except Exception:
            self.waringwind.ran()
            return
        self.resultwind.ran()

    """создание файлов в формате, который поддерживает многстроничные файлы"""

    def multy_page(self):
        self.startingwind.ran()
        try:
            form = self.sender().text()
            f = True
            self.create_folder()
            self.flag = False
            folder = self.creat_new_name_of_folder() + "/"
            for el in self.files:
                try:
                    a = []
                    img = Image.open(f"{self.folder_path}/{el}")
                    i = 0
                    s = []
                    img.seek(i)
                    img.save(f"timefile{i}.png")
                    s.append(Image.open(f"timefile{i}.png"))
                    a.append(f"timefile{i}.png")
                    while True:
                        i += 1
                        try:
                            img.seek(i)
                            img.save(f"timefile{i}.png", "png")
                            s.append(Image.open(f"timefile{i}.png"))
                            a.append(f"timefile{i}.png")
                        except EOFError:
                            break
                        except Exception:
                            self.waringwind.ran()
                            break
                    s[0].save(
                        f'{folder}{el.split(".")[0]}.{form}',
                        form,
                        save_all=True,
                        append_images=s[1:],
                    )
                    img.close()
                    for el1 in a:
                        os.unlink(el1)
                except Exception:
                    self.waringwind.ran()

        except FileNotFoundError or FileNotFoundError:
            self.nofolder.ran()
            return
        except Exception:
            self.waringwind.ran()
            return
        self.resultwind.ran()

    """обработка клавиатуры"""

    def keyPressEvent(self, event):
        self.btn_in_use[self.count % len(self.btn_in_use)].setStyleSheet(
            "background-color: rgb(100, 100, 100);" "color: rgb(255, 255, 255);"
        )
        if event.key() == Qt.Key_Down:
            self.count += 1
        elif event.key() == Qt.Key_Up:
            self.count -= 1
        elif event.key() == Qt.Key_Enter - 1:
            self.btn_in_use[self.count % len(self.btn_in_use)].click()
        self.btn_in_use[self.count % len(self.btn_in_use)].setStyleSheet(
            "background-color: rgb(255, 255, 0);" "color: rgb(0, 0, 255);"
        )


"""всплывающее окно, которое появляется, 
когда программа закончила конвектироввать изображение или пакпу с изображениями"""


class Result:
    """создание интерфейса"""

    def __init__(self):
        self.result = QMessageBox()
        self.result.setWindowTitle("Convector")
        self.result.setText("операция выполненна успешно")
        self.result.setIcon(QMessageBox.Information)
        self.result.setStandardButtons(QMessageBox.Ok)
        self.result.setStyleSheet(
            "background-color: rgb(50,50,50);"
            "border: 1px solid rgb(230,230,230);"
            "color: white;"
        )

    """запуск окна"""

    def ran(self):
        self.result.exec_()


"""всплывающее окно, которое появляется, когда программа не смогла преобразовать изображение"""


class Waring(Result):
    """создание интерфейса окна"""

    def __init__(self):
        super().__init__()
        self.result.setText("при выполнении операции произошла ошибка")
        self.result.setIcon(QMessageBox.Warning)


"""вспывающее окно, которое появляется, когда пользователь начнёт преобразование папки с изображениями"""


class Starting(Result):
    """создание интерфейса окна"""

    def __init__(self):
        super().__init__()
        self.result.setText("Операция начинается.\nЭто может занять какое-то время")


"""вплывающее окно, которое появиться , когда пользователь нажмёт на кнопку 'инструкция' на главном экране"""


class Instraction(Result):
    """создание интерфейса окна"""

    def __init__(self):
        super().__init__()
        self.result.setText(
            "В этом приложении кнопки выделены серым цветом. \n"
            "По кнопкам окон конвертации можно перемещаться \n"
            'стрелками вверх и вниз и нажимать на кнопку клаввишой "Ввод". \n'
            "Выделенная кнопка - активная\n"
            "В случае выбора папки с изобрадениями, \n"
            "новая папка создаться в той же директории, что и изначальная папка"
        )
        self.result.setIcon(QMessageBox.Information)


"""всплывающее окно, которое появляется, если пользователь выбрал не существующую папку в качестве пакпи в которую 
надо сохранить файл"""


class NotFound(Result):
    """создание интерфейса окна"""

    def __init__(self):
        super().__init__()
        self.result.setText("Паки или изображения не существует не существует")
        self.result.setIcon(QMessageBox.Warning)


"""обработка ошибок, которые могут случится при выполнении программы"""


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


"""запуск программы"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Main_window("PyQt5.QtCore.QPoint(609, 127)")
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())