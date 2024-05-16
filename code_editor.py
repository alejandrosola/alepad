from tkinter import Tk, Text, END
from helpers import increase_fontsize, decrease_fontsize, restore_fontsize, do_backspace, open_code_file, save_to_code_file, close_char, do_tab, consult_gemini

class CodeEditor:


    def __init__(self, w, h, font="Calibri", fontsize=18, background="#24273a", foreground="#FFFFFF"):

        self.root = Tk()
        self.data_to_save = []
        self.currentfile = None
        self.font = font
        self.fontsize = fontsize
        self.default_fontsize = fontsize

        self.font_params = {
            "font": self.font,
            "fontsize": self.fontsize
        }

        self.root.config(highlightbackground=background)
        self.text = Text(self.root, font=tuple(self.font_params.values()), width=w, height=h, background=background, 
                         foreground=foreground, highlightbackground=background, insertbackground=foreground,
                         borderwidth=0, padx=10, pady=10)
        self.text.pack(expand=True)
        
        self.root.bind("<Control-o>", lambda event, text_editor=self: open_code_file(event, text_editor))
        self.root.bind("<Control-plus>", lambda event, text_editor=self: increase_fontsize(event, text_editor))
        self.root.bind("<Control-minus>", lambda event, text_editor=self: decrease_fontsize(event, text_editor))
        self.root.bind("<Control-0>", lambda event, text_editor=self: restore_fontsize(event, text_editor))
        self.root.bind("<Control-s>", lambda event, text_editor=self: save_to_code_file(event, text_editor))
        self.root.bind("<Control-BackSpace>", lambda event, text_editor=self: do_backspace(event, text_editor))
        self.text.bind("(", lambda event, text_editor=self, chars="()": close_char(event, text_editor, chars))
        self.text.bind("{", lambda event, text_editor=self, chars="{}": close_char(event, text_editor, chars))
        self.text.bind("[", lambda event, text_editor=self, chars="[]": close_char(event, text_editor, chars))
        self.text.bind("\"", lambda event, text_editor=self, chars="\"\"": close_char(event, text_editor, chars))
        self.text.bind("'", lambda event, text_editor=self, chars="''": close_char(event, text_editor, chars))
        self.text.bind("<Tab>", lambda event, text_editor=self, tab=True: do_tab(event, text_editor, tab))
        self.text.bind("<Shift-ISO_Left_Tab>", lambda event, text_editor=self, tab=False: do_tab(event, text_editor, tab))
        
        self.root.mainloop()
    
    def clear(self):
        self.text.delete('1.0', END)

def space():
    print("space was pressed")
    return 'break'