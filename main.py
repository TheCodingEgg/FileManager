import os
import sys
import shutil
import PySimpleGUI as sg
import subprocess
from datetime import datetime

class Tree:
    def __init__(self, parent, file):
        self.file = file
        self.children = []
        self.parent = parent
        self.is_selected = False
        self.was_cut = False

    def __str__(self):
        return os.path.basename(self.file)

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self):
        if len(self.children) == 0:
            print(self.file)
        for c in self.children:
            if os.path.isdir(c.file):
                print(self.file)
            c.print_tree()

    def get_children(self):
        ch = []
        for c in self.children:
            ch.append(c)
        return ch

    def deselect_children(self):
        for c in self.children:
            c.is_selected = False

    def get_selected(self):
        for c in self.children:
            if c.is_selected:
                return c

    def get_file(self):
        return self.file

    def find_file(self, file):
        if self.file == file:
            return self
        else:
            if len(self.children) != 0:
                for c in self.children:
                    res = c.find_file(file)
                    if res is not None:
                        return res

def file_exists(directory: Tree, name: str):
    for child in directory.get_children():
        if os.path.basename(child.file) == name:
            return True
    return False

def list_directories(path, tab_count):
    if not os.path.isdir(path):
        print("\t" * (tab_count - 1) + os.path.basename(path))
    else:
        for p in os.listdir(path):
            new_path = os.path.join(path, p)
            if os.path.isdir(new_path):
                print("\t" * tab_count + p)
            try:
                list_directories(new_path, tab_count + 1)
            except PermissionError as e:
                print(e, sys.stderr)

def add_dir(parent, path):
    if not os.path.isdir(path):
        node = Tree(parent, path)
        parent.add_child(node)
    else:
        try:
            dirs = os.listdir(path)
            for f in dirs:
                name = os.path.join(path, f)
                node = Tree(parent, name)
                if os.path.isdir(name):
                    parent.add_child(node)
                    add_dir(node, name)
                else:
                    add_dir(parent, name)
        except PermissionError as e:
            print(e, sys.stderr)

def create_file(path, name):
    try:
        os.chdir(path)
        open(name, "x")
        os.chdir(dir_path)
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)

def create_folder(path, name):
    try:
        os.chdir(path)
        os.makedirs(name)
        os.chdir(dir_path)
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)

def delete_file(path, name):
    try:
        os.chdir(path)
        os.remove(name)
        os.chdir(dir_path)
    except FileNotFoundError as e:
        print(e, sys.stderr)

def delete_empty_folder(path, name):
    try:
        os.rmdir(name)
    except FileNotFoundError as e:
        print(e, sys.stderr)

def delete_full_folder(path, name):
    try:
        shutil.rmtree(name)
    except FileNotFoundError as e:
        print(e, sys.stderr)

def delete_folder(path, name):
    try:
        os.chdir(path)
        if len(os.listdir(name)) == 0:
            delete_empty_folder(path, name)
        else:
            delete_full_folder(path, name)
        os.chdir(dir_path)
    except FileNotFoundError as e:
        print(e, sys.stderr)

def rename_file(path, old_name, new_name):
    try:
        os.chdir(path)
        os.rename(old_name, new_name)
        os.chdir(dir_path)
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)

def rename_folder(path, old_name, new_name):
    try:
        os.chdir(path)
        os.rename(old_name, new_name)
        os.chdir(dir_path)
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)

def move_file(path, name, new_path):
    try:
        os.chdir(path)
        shutil.move(name, os.path.join(new_path, name))
        os.chdir(dir_path)
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)

def move_folder(path, name, new_path):
    try:
        os.chdir(path)
        shutil.move(name, os.path.join(new_path, name))
        os.chdir(dir_path)
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)

def copy_file(path, name, new_path):
    try:
        os.chdir(dir_path)
        shutil.copy2(os.path.join(path),
                     os.path.join(new_path, name))
        os.chdir(dir_path)
    except (FileNotFoundError, IOError) as e:
        print(e, sys.stderr)

def copy_folder(path, name, new_path):
    try:
        os.chdir(dir_path)
        shutil.copytree(os.path.join(path),
                        os.path.join(new_path, name))
        os.chdir(dir_path)
    except (FileNotFoundError, IOError) as e:
        print(e, sys.stderr)

def get_input():
    layout_input = [[sg.InputText(key="-INPUT-")], [sg.Button('Ok')]]
    window1 = sg.Window('Input Box', layout_input,
                        resizable=True, finalize=True)
    window1.close_destroys_window = True
    ret = None
    while True:
        event1, values1 = window1.read()
        if event1 in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event1 == 'Ok':
            ret = values1["-INPUT-"]
            break
    window1.close()
    return ret

def message_box(message: str, window_title: str):
    layout_message = [[sg.Text(message)], [sg.Button('Ok')]]
    window2 = sg.Window(window_title, layout_message,
                        resizable=True, finalize=True, size=(300, 80))
    window2.close_destroys_window = True
    while True:
        event2, values2 = window2.read()
        if event2 in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event2 == 'Ok':
            break
    window2.close()

def rebuild():
    tree1 = Tree(None, start)
    add_dir(tree1, start)
    return tree1

def refresh(selected_temp):
    values_temp = selected_temp.get_children()
    window["-FILE LIST-"].update(values_temp)
    text_temp = selected_temp.file
    window["-PATH-"].update(text_temp)

def search_files(directory: Tree, query: str):
    results = []
    if query.lower() in os.path.basename(directory.file).lower():
        results.append(directory)
    for child in directory.children:
        results.extend(search_files(child, query))
    return results

def display_properties(path):
    try:
        stats = os.stat(path)
        file_size = stats.st_size
        creation_time = datetime.fromtimestamp(stats.st_ctime)
        modification_time = datetime.fromtimestamp(stats.st_mtime)
        message = (f"File: {os.path.basename(path)}\n"
                   f"Size: {file_size} bytes\n"
                   f"Created: {creation_time}\n"
                   f"Modified: {modification_time}")
        message_box(message, "File Properties")
    except FileNotFoundError as e:
        print(e, sys.stderr)

if __name__ == '__main__':
    start = "test"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sg.theme('DarkAmber')
    tree = Tree(None, start)
    add_dir(tree, start)
    names = tree.get_children()
    file_list_column = [
        [sg.Listbox(values=names, enable_events=True, size=(80, 40), key="-FILE LIST-",
                    select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
                    right_click_menu=['Unused', ['Open', 'New Folder', 'New File', 'Cut', 'Copy', 'Delete', 'Rename', 'Paste', 'Properties']])],
    ]

    button_column = [[sg.Button("UP", key="-UP-")],
                     [sg.HSeparator()], [sg.Button("GAME", key="-GAME-")],
                     [sg.Input(key='-SEARCH-'), sg.Button('Search', key='-SEARCH_BTN-')]]

    layout = [[sg.Text(text=".", key="-PATH-", ), ],
              [sg.Column(file_list_column),
               sg.VSeperator(), sg.Column(button_column, vertical_alignment='top'), ]
              ]

    window = sg.Window('File Manager', layout, resizable=True, finalize=True)

    selected = None
    current_directory = tree
    copy = None

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

        if event == "-FILE LIST-":
            if len(values["-FILE LIST-"]) == 0:
                continue
            selected = values["-FILE LIST-"]
            if len(selected) == 1:
                selected = selected[0]
                if selected.is_selected:
                    if os.path.isdir(selected.file):
                        current_directory = selected
                        refresh(selected)
                        selected.is_selected = False
                        selected = None
                else:
                    current_directory.deselect_children()
                    selected.is_selected = True

        if event == "-UP-":
            if current_directory.parent is not None:
                current_directory.deselect_children()
                current_directory = current_directory.parent
                refresh(current_directory)

        if event == 'Rename':
            if selected is None:
                continue
            for item in selected:
                if not item.is_selected:
                    continue
                path = current_directory.file
                item_path = os.path.join(path, item.__str__())
                name = get_input()
                if name is None or name == "":
                    message_box("You must input a name!", "Warning")
                    continue
                if os.path.isdir(item_path):
                    rename_folder(path, os.path.basename(item_path), name)
                else:
                    rename_file(path, os.path.basename(item_path), name)
            tree = rebuild()
            current_directory = tree.find_file(current_directory.file)
            selected = None
            refresh(current_directory)

        if event == 'Delete':
            if selected is None:
                continue
            for item in selected:
                if not item.is_selected:
                    continue
                path = current_directory.file
                item_path = os.path.join(current_directory.file, item.__str__())
                if os.path.isdir(item_path):
                    delete_folder(path, os.path.basename(item_path))
                else:
                    delete_file(path, os.path.basename(item_path))
            tree = rebuild()
            current_directory = tree.find_file(current_directory.file)
            selected = None
            refresh(current_directory)

        if event == 'New File':
            path = current_directory.file
            name = get_input()
            if name is None or name == "":
                message_box("You must input a name!", "Warning")
                continue

            filename, extension = os.path.splitext(name)
            i = 1
            while file_exists(current_directory, filename + extension):
                filename = os.path.splitext(name)[0] + " (" + str(i) + ")"
                i += 1

            create_file(path, filename + extension)
            tree = rebuild()
            current_directory = tree.find_file(current_directory.file)
            selected = None
            refresh(current_directory)

        if event == 'New Folder':
            path = current_directory.file
            name = get_input()
            if name is None or name == "":
                message_box("You must input a name!", "Warning")
                continue

            filename = name
            i = 1
            while file_exists(current_directory, filename):
                filename = name + " (" + str(i) + ")"
                i += 1

            create_folder(path, filename)
            tree = rebuild()
            current_directory = tree.find_file(current_directory.file)
            selected = None
            refresh(current_directory)

        if event == 'Copy':
            if selected is None:
                continue
            copy = selected

        if event == 'Cut':
            if selected is None:
                continue
            copy = selected
            for item in copy:
                item.was_cut = True

        if event == 'Paste':
            if copy is None:
                continue

            if copy[0].parent is None:
                print("You can't copy the starting folder.")
                continue

            for item in copy:
                filename, extension = os.path.splitext(os.path.basename(item.file))
                i = 1
                while file_exists(current_directory, filename + extension):
                    filename = os.path.splitext(os.path.basename(item.file))[0] + " (" + str(i) + ")"
                    i += 1
                if os.path.isdir(item.file):
                    copy_folder(item.file, filename + extension, current_directory.file)
                else:
                    copy_file(item.file, filename + extension, current_directory.file)

                if item.was_cut is False:
                    tree = rebuild()
                    current_directory = tree.find_file(current_directory.file)
                    selected = None
                    refresh(current_directory)
                else:
                    path = item.parent.file
                    item_path = os.path.join(path, item.__str__())
                    if os.path.isdir(item_path):
                        delete_folder(path, os.path.basename(item_path))
                    else:
                        delete_file(path, os.path.basename(item_path))
                    tree = rebuild()
                    current_directory = tree.find_file(current_directory.file)
                    selected = None
                    refresh(current_directory)
                    copy = None

        if event == 'Open':
            if selected is None:
                continue
            if len(selected) == 1:
                selected_item = selected[0]
                if not os.path.isdir(selected_item.file):
                    if os.name == 'nt':
                        subprocess.Popen([selected_item.file], shell=True)
                    else:
                        os.system('xdg-open "%s"' % selected_item.file)
                else:
                    message_box("Can't open a directory", "Warning")

        if event == 'Properties':
            if selected is None:
                continue
            for item in selected:
                display_properties(item.file)

        if event == 'Search':
            query = values['-SEARCH-']
            if query:
                search_results = search_files(tree, query)
                window['-FILE LIST-'].update(search_results)

        if event == "-GAME-":
            subprocess.Popen([sys.executable, "game.py"])

    window.close()
