import os
import sys
import shutil
import PySimpleGUI as sg


class Tree:
    def __init__(self, parent, file):
        self.file = file
        self.children = []
        self.parent = parent
        self.is_selected = False

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


start = "test"
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
sg.theme('DarkAmber')


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


start = "test"
tree = Tree(None, start)
add_dir(tree, start)
tree.print_tree()


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
        os.chdir(path)
        os.rmdir(name)
        os.chdir(dir_path)
    except FileNotFoundError as e:
        print(e, sys.stderr)


def delete_full_folder(path, name):
    try:
        os.chdir(path)
        shutil.rmtree(name)
        os.chdir(dir_path)
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
        os.chdir(path)
        shutil.copy2(name, new_path)
        os.chdir(dir_path)
    except (FileNotFoundError, IOError) as e:
        print(e, sys.stderr)


def copy_folder(path, name, new_path):
    try:
        os.chdir(path)
        shutil.copytree(name, os.path.join(new_path + "\\" + name))
        os.chdir(dir_path)
    except (FileNotFoundError, IOError) as e:
        print(e, sys.stderr)


def get_input():
    layout_input = [[sg.InputText(key="-INPUT-")], [sg.Button('Ok')]]
    window1 = sg.Window('Input Box', layout_input, resizable=True, finalize=True)
    window1.close_destroys_window = True
    while True:
        event1, values1 = window1.read()
        if event1 in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event1 == 'Ok':
            ret = values1["-INPUT-"]
            break
    window1.close()
    return ret


names = tree.get_children()

file_list_column = [
    [sg.Listbox(values=names, enable_events=True, size=(80, 40), key="-FILE LIST-",
                right_click_menu=['Unused', ['New Folder', 'New File', 'Cut', 'Copy', 'Delete', 'Rename', 'Paste']])],
]

button_column = [[sg.Button("UP", key="-UP-")], ]

layout = [[sg.Text(text=".", key="-PATH-", ), ],
          [sg.Column(file_list_column),
           sg.VSeperator(), sg.Column(button_column, vertical_alignment='top'), ]
          ]

window = sg.Window('File Manager', layout, resizable=True, finalize=True)

obj = tree
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event == "-FILE LIST-":
        obj = values["-FILE LIST-"][0]
        if obj.is_selected:
            if len(obj.children) != 0:
                values = obj.get_children()
                window["-FILE LIST-"].update(values)
                text = obj.file
                window["-PATH-"].update(text)
            obj.is_selected = False
        else:
            obj.parent.deselect_children()
            obj.is_selected = True
    if event == "-UP-":
        if obj.parent is not None:
            obj = obj.parent
            values = obj.get_children()
            window["-FILE LIST-"].update(values)
            text = obj.file
            window["-PATH-"].update(text)
    if event == 'Rename':
        path = obj.parent.file
        item = os.path.join(obj.parent.file, obj.parent.get_selected().__str__())
        if os.path.isdir(item):
            rename_folder(path, os.path.basename(item), get_input())
        else:
            rename_file(path, os.path.basename(item), get_input())
        list_directories(start, 0)
        tree1 = Tree(None, start)
        add_dir(tree1, start)
        tree = tree1
        tree.print_tree()
        # values = obj.parent.get_children()
        # window["-FILE LIST-"].update(values)
        # text = obj.file
        # window["-PATH-"].update(text)
        #tbd

window.close()
