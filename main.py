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


start = "test"
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
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)


def create_folder(path, name):
    try:
        os.chdir(path)
        os.makedirs(name)
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)


def delete_file(path, name):
    try:
        os.chdir(path)
        os.remove(name)
    except FileNotFoundError as e:
        print(e, sys.stderr)


def delete_empty_folder(path, name):
    try:
        os.chdir(path)
        os.rmdir(name)
    except FileNotFoundError as e:
        print(e, sys.stderr)


def delete_full_folder(path, name):
    try:
        os.chdir(path)
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
    except FileNotFoundError as e:
        print(e, sys.stderr)


def rename_file(path, old_name, new_name):
    try:
        os.chdir(path)
        os.rename(old_name, new_name)
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)


def rename_folder(path, old_name, new_name):
    try:
        os.chdir(path)
        os.rename(old_name, new_name)
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)


def move_file(path, name, new_path):
    try:
        os.chdir(path)
        shutil.move(name, os.path.join(new_path, name))
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)


def move_folder(path, name, new_path):
    try:
        os.chdir(path)
        shutil.move(name, os.path.join(new_path, name))
    except (FileNotFoundError, FileExistsError) as e:
        print(e, sys.stderr)


def copy_file(path, name, new_path):
    try:
        os.chdir(path)
        shutil.copy2(name, new_path)
    except (FileNotFoundError, IOError) as e:
        print(e, sys.stderr)


def copy_folder(path, name, new_path):
    try:
        os.chdir(path)
        shutil.copytree(name, os.path.join(new_path + "\\" + name))
    except (FileNotFoundError, IOError) as e:
        print(e, sys.stderr)


names = tree.get_children()

file_list_column = [
    [sg.Listbox(values=names, enable_events=True, size=(80, 40), key="-FILE LIST-",
                right_click_menu=['Unused', ['New Folder', 'New File', 'Cut', 'Copy', 'Delete', 'Rename', 'Paste', 'Properties']])],
]

button_column = [[sg.Button("UP", key="-UP-")],]

layout = [[sg.Text(text=".", key="-PATH-", ), ],
          [sg.Column(file_list_column),
           sg.VSeperator(), sg.Column(button_column, vertical_alignment='top'), ]
          ]

window = sg.Window('Tree Element Test', layout, resizable=True, finalize=True)

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

window.close()
