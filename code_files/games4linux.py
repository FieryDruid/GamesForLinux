#!/usr/bin/env python
import os
import sys  # sys нужен для передачи argv в QApplication

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import *

from .theme import Ui_MainWindow  # Это наш конвертированный файл дизайна


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле theme.py
        super().__init__()
        F1 = 'export DXVK_HUD=full'
        os.system("bash -c '%s'" % F1)
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.text = ''
        self.text2 = 'wine' #строки text теперь атрибуты класса и могут вызываться в любой функции
        self.text3 = ''

        Font_install = 'mkdir -p ~/.local/share/fonts'
        os.system("bash -c '%s'" % Font_install)
        Font_install_2 = 'cp /home/'+os.getlogin()+'/GamesForLinux/code_files/Font/Franxurter-Totally.ttf ~/.local/share/fonts'
        os.system("bash -c '%s'" % Font_install_2)
        Font_install_3 = 'fc-cache -f -v'
        os.system("bash -c '%s'" % Font_install_3)
        self.runner_directory = '/home/' + os.getlogin() + '/GamesForLinux/code_files/runner/'
        print(self.runner_directory)
        for item in os.listdir(self.runner_directory):  # для каждого файла в директории
            self.comboBox_2.addItem(item)   # добавить файл в comboBox
            
        self.prefix_locate_directory = '/home/' + os.getlogin() + '/GamesForLinux/code_files/prefix_locate/'
        for item in os.listdir(self.prefix_locate_directory):  # для каждого файла в директории
            self.listWidget_2.addItem(item)   # добавить файл в listWidget
            
        self.icons_directory = '/home/' + os.getlogin() + '/GamesForLinux/code_files/icon'
        for item in os.listdir(self.icons_directory):  # для каждого файла в директории
            self.listWidget_3.addItem(item)

    def connect_methods(self):
        buttons = ('create_prefix_button', 'select_wine_button', 'load_prefix_button', 'winetricks',
                    'wine_config', 'select_exe_button', 'install_exe_button', 'install_script_button',
                    'delete_item_button', 'search_button', 'backspace_button', 'run_button', 'delete_button')

        for button in buttons:
            button_object = getattr(self, button)
            button_object.connect(getattr(self, f'_{button}'))

    def _click_create_prefix_button(self):
        self.directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.label.setText(self.directory)

    def _click_select_wine_button(self):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)

        message_box.setWindowTitle("Информация")
        message_box.setText("Wine")
        message_box.setInformativeText("Выбрать системный wine?")

        okButton = message_box.addButton('  Да  ', QMessageBox.AcceptRole)
        message_box.addButton('Нет', QMessageBox.RejectRole)
        okButton.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(233, 15, 131, 255), "
            "stop:1 rgba(25, 206, 246, 255));"
        )
        message_box.setStyleSheet("border-radius:5px;"
                                  "background-color: rgb(48, 48, 48);"
                                  "color: rgb(255, 255, 255);"
                                  "font:11pt;"
                                  "font-weight:900;")

        message_box.exec()

        label_2_text = 'wine'
        if message_box.clickedButton() != okButton:
            existing_directory = QtWidgets.QFileDialog.getExistingDirectory()
            label_2_text = str(existing_directory)

        self.label_2.setText(label_2_text)

    def _check_prefix_locate_dir(self, dir_name):
        if not os.path.exists(dir_name):
            os.path.mkdir(dir_name)

    def _click_load_prefix_button(self):
        if not self.directory:
            raise ValueError('Директория префикса отсутствует')

        prefix_name = QFileInfo(self.directory).fileName()
        if self.text2 == 'wine':
            if prefix_name:
                combo_box = self.comboBox.currentText()
                prefix_locate_dir = os.path.join(os.path.dirname(__file__), 'prefix_locate')
                self._check_prefix_locate_dir(prefix_locate_dir)

                file_path = os.path.join(prefix_locate_dir, prefix_name)
                wine_path = os.path.join(os.path.dirname(__file__), 'winetricks')
                file_rows = [
                    '#!/bin/sh',
                    f"""WINEARCH="{combo_box}" WINEPREFIX="{self.text}" WINE="{wine_path}" &""",
                    f"""WINEARCH="{combo_box}" WINEPREFIX="{self.text}" WINE="{wine_path}" &""",
                ]
                f = open(f, mode="w", encoding="utf_8")
                f.write(
                    'WINEARCH=' + self.combo_box + ' WINEPREFIX=' + '"' + self.text + '"' + ' ' + '/bin/wine ' + ' winecfg &' + '\n')
                f.write(self.text + '/drive_c/' + '\n')
                f.write('WINEARCH=' + self.combo_box + ' WINEPREFIX=' + '"' + self.text + '"' + ' ' + '/bin/wine' + ' "')
                f.close()
                f2 = '/home/' + os.getlogin() + '/GamesForLinux/code_files/prefix_locate_delete/' + self.nameprefix
                f2 = open(f2, mode="w", encoding="utf_8")
                f2.write('#!/bin/sh' + '\n')
                f2.write('rm -r ' + '"' + self.text + '"')
                f2.close()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setWindowTitle("Информация")
                msg.setText("\nОшибка, поле имени пусто!")

                okButton = msg.addButton('Ок', QMessageBox.AcceptRole)
                okButton.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(233, 15, 131, 255), stop:1 rgba(25, 206, 246, 255));")
                msg.setStyleSheet("border-radius:5px;"
                                  "background-color: rgb(48, 48, 48);"
                                  "color: rgb(255, 255, 255);"
                                  "font:11pt;"
                                  "font-weight:900;")
                msg.exec()
        self.name = QFileInfo(str(self.directory)).fileName()
        print(self.name)
        self.nameprefix = self.name
        if self.text2 != 'wine':
            if self.nameprefix != "":
                self.combo_box = self.comboBox.currentText()
                f = '/home/' + os.getlogin() + '/GamesForLinux/code_files/prefix_locate/' + self.nameprefix
                f = open(f, mode="w", encoding="utf_8")
                f.write('#!/bin/sh' + '\n')
                f.write(
                    'WINEARCH=''"' + self.combo_box + '"' + ' WINEPREFIX=' + '"' + self.text + '"' ' WINE=' + self.text2 + '/bin/wine' + ' /home/' + os.getlogin() + '/GamesForLinux/code_files/winetricks &' + '\n')
                f.write(
                    'WINEARCH=' + self.combo_box + ' WINEPREFIX=' + '"' + self.text + '"' + ' ' + self.text2 + '/bin/wine' + ' winecfg &' + '\n')
                f.write(self.text + '/drive_c/' + '\n')
                f.write(
                    'WINEARCH=' + self.combo_box + ' WINEPREFIX=' + '"' + self.text + '"' + ' ' + self.text2 + '/bin/wine' + ' "')
                f.close()
                f2 = '/home/' + os.getlogin() + '/GamesForLinux/code_files/prefix_locate_delete/' + self.nameprefix
                f2 = open(f2, mode="w", encoding="utf_8")
                f2.write('#!/bin/sh' + '\n')
                f2.write('rm -r ' + '"' + self.text + '"')
                f2.close()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setWindowTitle("Информация")
                msg.setText("\nОшибка, поле имени пусто!")

                okButton = msg.addButton('Ок', QMessageBox.AcceptRole)
                okButton.setStyleSheet(
                    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(233, 15, 131, 255), stop:1 rgba(25, 206, 246, 255));")
                msg.setStyleSheet("border-radius:5px;"
                                  "background-color: rgb(48, 48, 48);"
                                  "color: rgb(255, 255, 255);"
                                  "font:11pt;"
                                  "font-weight:900;")
                msg.exec()
        self.listWidget_2.clear()
        self.prefix_locate_directory = '/home/' + os.getlogin() + '/GamesForLinux/code_files/prefix_locate/'
        for self.item_2 in os.listdir(self.prefix_locate_directory):  # для каждого файла в директории
            self.listWidget_2.addItem(str(self.item_2))  # добавить файл в listWidget

    def _click_install_exe_button(self):
        try:
            self.selectItem_3 = self.listWidget_2.currentItem().text()
            self.f_3 = self.prefix_locate_directory + self.selectItem_3
            self.f_3 = open(self.f_3, mode="r", encoding="utf_8")
            print(self.f_3)
            e = str(self.f_3.readlines()[4])
            e = e.replace("\n", "")
            # exe_file='/home/'+os.getlogin()+'/GamesForLinux/code_files/wine-create-shortcut'+" "+'"'+self.text3+'"'
            # print(exe_file)
            # os.system("bash -c '%s'" % exe_file)
            installexe = e + self.text3 + '"'
            os.system("bash -c '%s'" % installexe)
            print(installexe)
            self.selectItem_4 = self.listWidget_2.currentItem().text()
            self.f_4 = self.prefix_locate_directory + self.selectItem_4
            self.f_4 = open(self.f_4, mode="r", encoding="utf_8")
            self.str2 = str(self.f_4.readlines()[4])
            self.selectItem_5 = self.listWidget_2.currentItem().text()
            self.f_5 = self.prefix_locate_directory + self.selectItem_5
            self.f_5 = open(self.f_5, mode="r", encoding="utf_8")
            path = self.f_5.readlines()[3]
            path.replace("\n", "")
            self.str2 = self.str2.replace("\n", "")
            print(self.str2)
            self.directory_10 = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберете папку приложения", path)
            directory_11 = QtWidgets.QFileDialog.getOpenFileNames(self, "выберете установщик", self.directory_10,
                                                                  "Windows Files (*.exe)")[0]
            print(directory_11)
            self.filename = QFileInfo(str(self.directory_10)).fileName()
            path_exe = str(directory_11[0])
            print(path_exe)
            print(path)
            print(self.filename)
            f_1 = '/home/' + os.getlogin() + '/GamesForLinux/code_files/icon/' + self.selectItem_3 + ' | ' + self.filename
            f_1 = open(f_1, mode="w", encoding="utf_8")
            f_1.write('[Desktop Entry]' + '\n')
            f_1.write('Exec=' + self.str2 + path_exe + '"' + '\n')
            f_1.write('Type=Application' + '\n')
            f_1.write('Path=' + self.directory_10 + '\n')
            f_1.close()
            f_6 = '/home/' + os.getlogin() + '/GamesForLinux/code_files/software_icon_delete/' + self.selectItem_3 + ' | ' + self.filename
            f_6 = open(f_6, mode="w", encoding="utf_8")
            f_6.write('#!/bin/sh' + '\n')
            f_6.write(self.str2 + 'uninstaller' + '"' + '\n')
            f_6.write(
                '/home/' + os.getlogin() + '/GamesForLinux/code_files/icon/' + self.selectItem_3 + ' | ' + self.filename)
            f_6.close()
            chmod = 'chmod +x ' + '/home/' + os.getlogin() + '/GamesForLinux/code_files/software_icon_delete/' + '"' + self.selectItem_3 + ' | ' + self.filename + '"'
            os.system("bash -c '%s'" % chmod)
            chmod_2 = 'chmod +x ' + '/home/' + os.getlogin() + '/GamesForLinux/code_files/icon/' + '"' + self.selectItem_3 + ' | ' + self.filename + '"'
            os.system("bash -c '%s'" % chmod_2)
            self.listWidget_3.clear()
            self.icons_directory = '/home/' + os.getlogin() + '/GamesForLinux/code_files/icon/'
            for self.item_3 in os.listdir(self.icons_directory):  # для каждого файла в директории
                self.listWidget_3.addItem(self.item_3)

        except AttributeError:
            error_1 = 'Выбери пути!'
            QMessageBox.question(self, 'Введено', error_1, QMessageBox.Ok, QMessageBox.Ok)
        except IndexError:
            error_2 = 'Выбери пути!'
            QMessageBox.question(self, 'Введено', error_2, QMessageBox.Ok, QMessageBox.Ok)

    def _click_backspace_button(self):
        self.listWidget_2.clear() 
        self.prefix_locate_directory = '/home/' + os.getlogin() + '/GamesForLinux/code_files/prefix_locate/'
        for self.item_2 in os.listdir(self.prefix_locate_directory):  # для каждого файла в директории
            self.listWidget_2.addItem(self.item_2)   # добавить файл в listWidget 
        
    def _click_search_button(self):
         self.search_string = self.lineEdit_2.text()
         if self.search_string == "":
                self.listWidget_2.clear() 
                self.prefix_locate_directory = '/home/' + os.getlogin() + '/GamesForLinux/code_files/prefix_locate/'
                for self.item_2 in os.listdir(self.prefix_locate_directory):  # для каждого файла в директории
                    self.listWidget_2.addItem(str(self.item_2))   # добавить файл в listWidget
         else:
            match_items = self.listWidget_2.findItems(self.search_string, QtCore.Qt.MatchExactly)
            for i in range(self.listWidget_2.count()):
                it = self.listWidget_2.item(i)
                it.setHidden(it not in match_items)


        



    def _click_install_script_button(self):
        self.selectedLayers=self.comboBox_2.currentText()
        self.text5 = str(self.runner_directory)
        self.selectedLayers=self.comboBox_2.currentText()
        setup = 'python3 ' + self.text5 + self.selectedLayers + ' &'
        os.system("bash -c '%s'" % setup)
        print(setup)
        
    def _click_delete_item_button(self):
        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            # msg.setIconPixmap(pixmap)  # Своя картинка
  
            msg.setWindowTitle("Информация")
            msg.setText("Удалить?")
            msg.setInformativeText("Удалить файл префикса?")
  
            okButton = msg.addButton( '  Да  ', QMessageBox.AcceptRole)
            msg.addButton('Нет', QMessageBox.RejectRole)
            okButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(233, 15, 131, 255), stop:1 rgba(25, 206, 246, 255));")
            msg.setStyleSheet("border-radius:5px;"
"background-color: rgb(48, 48, 48);"
"color: rgb(255, 255, 255);"
"font:11pt;"
"font-weight:900;") 
  
            msg.exec()
            if msg.clickedButton() == okButton:
                self.directory_8 = '/home/'+os.getlogin()+'/GamesForLinux/code_files/prefix_locate_delete/'
                self.selectItem_3 = self.listWidget_2.currentItem().text()
                setups = 'rm ' +'"' + self.prefix_locate_directory + self.selectItem_3 + '"'
                print(setups)
                delete_prefix = 'sh '+ '"'+self.directory_8 + self.selectItem_3+'"'
                print(delete_prefix)
                delete_prefix_sh = 'rm '+ '"'+self.directory_8 + self.selectItem_3+'"'
                os.system("bash -c '%s'" % delete_prefix)
                os.system("bash -c '%s'" % delete_prefix_sh)
                os.system("bash -c '%s'" % setups)
                self.listWidget_2.clear() 
                self.prefix_locate_directory = '/home/' + os.getlogin() + '/GamesForLinux/code_files/prefix_locate/'
                for self.item_2 in os.listdir(self.prefix_locate_directory):  # для каждого файла в директории
                    self.listWidget_2.addItem(str(self.item_2))   # добавить файл в listWidget
        except AttributeError:
            error_1 = 'Выбери пути!'
            
            QMessageBox.question(self, 'Введено', error_1, QMessageBox.Ok, QMessageBox.Ok)

        

    def _click_delete_button(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        # msg.setIconPixmap(pixmap)  # Своя картинка
  
        msg.setWindowTitle("Информация")
        msg.setText("Удалить?")
        msg.setInformativeText("Удалить приложение?")
  
        okButton = msg.addButton( '  Да  ', QMessageBox.AcceptRole)
        msg.addButton('Нет', QMessageBox.RejectRole)
        okButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(233, 15, 131, 255), stop:1 rgba(25, 206, 246, 255));")
        msg.setStyleSheet("border-radius:5px;"
"background-color: rgb(48, 48, 48);"
"color: rgb(255, 255, 255);"
"font:11pt;"
"font-weight:900;") 
  
        msg.exec()
        if msg.clickedButton() == okButton:        
            self.selectItem_4 = self.listWidget_3.currentItem().text()
            self.directory_12 = '/home/'+os.getlogin()+'/GamesForLinux/code_files/software_icon_delete/'
            self.f_8 = self.directory_12 + self.selectItem_4
            self.f_8 = open(self.f_8, mode="r", encoding="utf_8")
            self.str2=str(self.f_8.readlines()[1])
            start_uninstaller = self.str2
            os.system("bash -c '%s'" % start_uninstaller)
            self.f_7 = self.directory_12 + self.selectItem_4
            self.f_7 = open(self.f_7, mode="r", encoding="utf_8")
            self.str3=str(self.f_7.readlines()[2])
            print(self.str3)
            rm_icon = 'rm ' + '"'+self.str3+'"' 
            os.system("bash -c '%s'" % rm_icon)
            rm_software_icon_delete = 'rm ' + '"'+self.directory_12 + self.selectItem_4+'"'
            os.system("bash -c '%s'" % rm_software_icon_delete)
            self.listWidget_3.clear()
            self.icons_directory = '/home/' + os.getlogin() + '/GamesForLinux/code_files/icon/'
            for self.item_3 in os.listdir(self.icons_directory):  # для каждого файла в директории
                self.listWidget_3.addItem(self.item_3)        

    def _click_wine_config(self):
        try:
            self.selectItem_2 = self.listWidget_2.currentItem().text()
            self.f_2 = self.prefix_locate_directory + self.selectItem_2
            self.f_2 = open(self.f_2, mode="r", encoding="utf_8")
            s=str(self.f_2.readlines()[2])
            winecfg =  s 
            os.system("bash -c '%s'" % winecfg)
            print(winecfg)
        except AttributeError:
            error_1 = 'Выбери пути!'
            QMessageBox.question(self, 'Введено', error_1, QMessageBox.Ok, QMessageBox.Ok)
        except IndexError:
            error_2 = 'Выбери пути!'
            QMessageBox.question(self, 'Введено', error_2, QMessageBox.Ok, QMessageBox.Ok)
        
    def _click_winetricks(self):
        try:
            self.selectItem = self.listWidget_2.currentItem().text()
            self.f = self.prefix_locate_directory + self.selectItem
            self.f = open(self.f, mode="r", encoding="utf_8")
            a=str(self.f.readlines()[1])
            run =  a
            os.system("bash -c '%s'" % run)
            print(run)
        except AttributeError:
            error_3 = 'Выбери пути!'
            QMessageBox.question(self, 'Введено', error_3, QMessageBox.Ok, QMessageBox.Ok)
        except IndexError:
            error_4 = 'Выбери пути!'
            QMessageBox.question(self, 'Введено', error_4, QMessageBox.Ok, QMessageBox.Ok)
        update =  '/home/'+os.getlogin()+'/GamesForLinux/code_files/winetricks --self-update'
        os.system("bash -c '%s'" % update)
        
    def _click_select_exe_button(self):
        directory3 = QtWidgets.QFileDialog.getOpenFileName(self,"выберете утсановщик", "","Windows Files (*.exe)")[0]
        print(directory3)
        self.text3 = str(directory3)
        self.label_6.setText(self.text3)
            
            

    def _click_load_prefix_button(self):
        if self.text2 == 'wine':
            if self.text and self.text2:
                self.combo_box=self.comboBox.currentText()
                install = 'WINEARCH=' + self.combo_box + ' WINEPREFIX=' + '"' + self.text + '" ' + self.text2 + ' winecfg &'
                os.system("bash -c '%s'" % install)
                print(install)
                install = 'префикс успешно сконфигурирован'
        if self.text2 != 'wine':
                self.combo_box=self.comboBox.currentText()
                install = 'WINEARCH=' + self.combo_box + ' WINEPREFIX=' + '"' + self.text + '" ' + self.text2 + '/bin/wine' + ' winecfg &'
                os.system("bash -c '%s'" % install)
                print(install)
                install = 'префикс успешно сконфигурирован'
            #msg = QMessageBox()
            #msg.setIcon(QMessageBox.Information)
  
            #msg.setWindowTitle("Информация")
            #msg.setText("\nпрефикс успешно сконфигурирован")
  
            #okButton = msg.addButton('Ок', QMessageBox.AcceptRole)
            #okButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(233, 15, 131, 255), stop:1 rgba(25, 206, 246, 255));")
            #msg.setStyleSheet("border-radius:5px;"
#"background-color: rgb(48, 48, 48);"
#"color: rgb(255, 255, 255);"
#"font:11pt;"
#"font-weight:900;")
            #msg.exec()
        if self.text == '':
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
  
                    msg.setWindowTitle("Информация")
                    msg.setText("Error")
                    msg.setInformativeText("InformativeText")
  
                    okButton = msg.addButton('Окей', QMessageBox.AcceptRole)
                    okButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(233, 15, 131, 255), stop:1 rgba(25, 206, 246, 255));")
                    msg.setStyleSheet("border-radius:5px;"
"background-color: rgb(48, 48, 48);"
"color: rgb(255, 255, 255);")
                    msg.exec()
                    if msg.clickedButton() == okButton:
                        print("Yes")
                    else:
                        print("No")
    def _click_run_button(self):
        self.text4 = self.lineEdit_5.text()
        self.selectItem_6 = self.listWidget_3.currentItem().text()
        xdg2 ='export ' + self.text4 + '&&' + self.icons_directory + '/' + '"' + self.selectItem_6 + '"'
        os.system("bash -c '%s'" % xdg2 + '&')
        print(xdg2)
            
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    GamesForLinux = ExampleApp()  # Создаём объект класса ExampleApp
    GamesForLinux.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
