import os
import json
from Tkinter import Tk, Button, Text, Label, END
from tkFileDialog import askopenfilename


class GenerateREADME():
    def __init__(self, master):
        self.master = master
        master.title("README.md Generator")

        self.h1 = Label(
                master,
                text=('This script will create a README.md file by\n' +
                      'extracting any markdown content from an .ipynb.'),
                font=('Helvetica', 12))
        self.h1.pack()

        self.dir_button = Button(master, text='Generate README.md',
                                 command=self.WriteREADME)
        self.dir_button.pack()

        self.text = Text(master, width=40, height=1)
        self.text.pack()

    def WriteREADME(self):
        path = askopenfilename()
        dirpath = os.path.dirname(path)
        readme = dirpath + '/README.md'

        if not path.endswith('.ipynb'):
            self.text.delete('1.0', END)
            self.text.insert('1.0', 'Selected file is not .ipynb')
            return

        if os.path.exists(readme):
            self.text.delete('1.0', END)
            self.text.insert('1.0', 'A README.md file already exists.')
            return

        with open(path) as myfile:
            data = myfile.read().replace('\n', '')
        jdata = json.loads(data)
        content = []

        for i in range(len(jdata['cells'])):
            if jdata['cells'][i]['cell_type'] == 'markdown':
                content.append(jdata['cells'][i]['source'])

        if not content:
            self.text.delete('1.0', END)
            self.text.insert('1.0', 'There is no markdown content in .ipynb')
            return

        with open(readme, 'w') as outfile:
            [[outfile.write(str(item)) for item in row] for row in content]

        if os.path.exists(readme):
            self.text.delete('1.0', END)
            self.text.insert('1.0', 'README.md successfully created.')
            return


def main():
    root = Tk()
    GenerateREADME(root)
    root.mainloop()

if __name__ == '__main__':
    main()
