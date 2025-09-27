from random import shuffle
import json
from random import randint
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QRadioButton, QGroupBox, QButtonGroup, QTextEdit, QListWidget, QVBoxLayout, QLineEdit, QInputDialog

#notes = {"Добро пожаловать": 
#{"текст": " В этом приложении можно создавать заметки с тегами...", 
#"теги": ["черновик", "мысли"]}}

#with open ("notes_data.json", "w") as file:
   #json.dump(notes, file)


app = QApplication([])

main_win = QWidget()
main_win.setWindowTitle('умные заметки')
main_win.resize(1000,700)

text_i = QTextEdit()
tegs_id = QLineEdit()
tegs_id.setPlaceholderText('Введите тег...')
notes_title = QLabel('Список заметок')
tegs_title = QLabel('Список тегов')
list_notes = QListWidget()
list_tegs = QListWidget()

btn_add_note = QPushButton('Создать заметку')
btn_delete_note = QPushButton('Удалить заметку')
btn_save_note = QPushButton('Сохранить заметку')

btn_add_teg = QPushButton('Добавить к заметке')
btn_undo_teg = QPushButton('Открепить от заметки')
btn_found_teg = QPushButton('Искать заметки по тегу')



main_line = QHBoxLayout()
Rrr_line = QVBoxLayout()
line_btn_notes = QHBoxLayout()
line_btn_tegs = QHBoxLayout()

main_line.addWidget(text_i)
Rrr_line.addWidget(notes_title)
Rrr_line.addWidget(list_notes)

line_btn_notes.addWidget(btn_add_note)
line_btn_notes.addWidget(btn_delete_note)
Rrr_line.addLayout(line_btn_notes)
Rrr_line.addWidget(btn_save_note)

Rrr_line.addWidget(tegs_title)
Rrr_line.addWidget(list_tegs)
Rrr_line.addWidget(tegs_id)

line_btn_tegs.addWidget(btn_add_teg)
line_btn_tegs.addWidget(btn_undo_teg)
Rrr_line.addLayout(line_btn_tegs)
Rrr_line.addWidget(btn_found_teg)

main_line.addLayout(Rrr_line)

main_win.setLayout(main_line)

with open ("notes_data.json", "r") as file:
   notes = json.load(file)
list_notes.addItems(notes)

def show_note():#показывает заметки
    name = list_notes.selectedItems()[0].text()
    if name in notes:
        text_i.setText(notes[name]["текст"])
        list_tegs.clear()
        list_tegs.addItems(notes[name]["теги"])
list_notes.itemClicked.connect(show_note)

def add_note():#добавляет заметку
    note_name, result = QInputDialog.getText(main_win, 'Добавить заметку', 'Название заметки:')
    print(note_name)
    if result:
        notes[note_name] = {"текст": '',
        "теги": []}
        list_notes.addItem(note_name)
btn_add_note.clicked.connect(add_note)

def del_note():#удаляет выбранную заметку
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        del notes[name]
        with open ("notes_data.json", "w") as file:
            json.dump(notes, file)
        list_notes.clear()
        text_i.clear()
        list_tegs.clear()
        list_notes.addItems(notes)
btn_delete_note.clicked.connect(del_note)

def save_note():#сохраняет созданную заметку
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        text = text_i.toPlainText()
        notes[name]['текст'] = text
        with open ("notes_data.json", "w") as file:
            json.dump(notes, file)
btn_save_note.clicked.connect(save_note)

def add_teg():#добавляет тег и прикрепляет тег к выбранной заметке
    if list_notes.selectedItems():
        note = list_notes.selectedItems()[0].text()
        teg = tegs_id.text()
        if teg != '' and teg not in notes[note]['теги']:
            notes[note]['теги'].append(teg)
            list_tegs.addItem(teg)
            tegs_id.clear()
            with open ("notes_data.json", "w") as file:
                json.dump(notes, file)
btn_add_teg.clicked.connect(add_teg)

def del_teg():#удаляет тег
    if list_notes.selectedItems():
        name_note = list_notes.selectedItems()[0].text()
        name_teg = list_tegs.selectedItems()[0].text()
        notes[name_note]['теги'].remove(name_teg)
        with open ("notes_data.json", "w") as file:
            json.dump(notes, file)
        list_tegs.clear()
        tegs_id.clear()
        list_tegs.clear()
        list_tegs.addItems(notes[name_note]['теги'])
btn_undo_teg.clicked.connect(del_teg)

def search_teg():#ищет по тегу
    if btn_found_teg.text() == 'Искать заметки по тегу':
        tag = tegs_id.text()
        notes_filtered = []
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered.append(note)
        list_notes.clear()
        list_notes.addItems(notes_filtered)
        btn_found_teg.setText('Сбросить поиск')
    else:
        list_notes.clear()
        list_notes.addItems(notes)
        btn_found_teg.setText('Искать заметки по тегу')
btn_found_teg.clicked.connect(search_teg)

main_win.show()
app.exec_()

