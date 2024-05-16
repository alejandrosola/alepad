from tkinter import Tk, Text, SEL_FIRST, SEL_LAST, INSERT
from helpers import paste_image, open_file, increase_fontsize, decrease_fontsize, restore_fontsize, save_to_file, do_backspace, consult_gemini, insert_text
from IPython.display import Markdown
import google.generativeai as genai

class TextEditor:
    def __init__(self, w, h, font="Calibri", fontsize=18, background="#1f1c1c", foreground="#FFFFFF"):
        gemini_api_key = "AIzaSyAMIR8lUYTaVbQFkpz8y6HlQwKfgJQMTKU"
        genai.configure(api_key = gemini_api_key)

        self.ai_model = genai.GenerativeModel('gemini-pro')
        self.root = Tk()
        self.images = []
        self.images_paths = [] 
        self.data_to_save = []
        self.bold = False
        self.currentfile = None
        self.font = font
        self.fontsize = fontsize
        self.default_fontsize = fontsize
        self.has_clipboard = False

        self.font_params = {
            "font": self.font,
            "fontsize": self.fontsize
        }

        self.root.config(highlightbackground=background)
        self.text = Text(self.root, font=tuple(self.font_params.values()), width=w, height=h, background=background, 
                         foreground=foreground, highlightbackground=background, insertbackground=foreground,
                         borderwidth=0, padx=10, pady=10, undo=True)
        self.text.pack(expand=True)

        self.root.bind("<Control-v>", lambda event, text_editor=self: paste_image(event, text_editor))
        self.root.bind("<Control-o>", lambda event, text_editor=self: open_file(event, text_editor))
        self.root.bind("<Control-plus>", lambda event, text_editor=self: increase_fontsize(event, text_editor))
        self.root.bind("<Control-minus>", lambda event, text_editor=self: decrease_fontsize(event, text_editor))
        self.root.bind("<Control-0>", lambda event, text_editor=self: restore_fontsize(event, text_editor))
        self.root.bind("<Control-s>", lambda event, text_editor=self: save_to_file(event, text_editor))
        self.root.bind("<Control-BackSpace>", lambda event, text_editor=self: do_backspace(event, text_editor))
        self.text.bind("<Control-g>", lambda event, text_editor=self, tab=False: consult_gemini(event, text_editor))
        self.text.bind("<Control-equal>", lambda event, text_editor=self, tab=False: insert_text(event, text_editor, "============================================================"))
        self.text.bind("<Control-underscore>", lambda event, text_editor=self, tab=False: insert_text(event, text_editor, " -> "))
        self.root.mainloop()
    

    def update_font_size(self, amount: int):
        self.fontsize += amount
        self.font_params["fontsize"] = self.fontsize
        self.text.config(font=tuple(self.font_params.values()))
    
    def restore_fontsize(self):
        self.fontsize = self.default_fontsize
        self.font_params["fontsize"] = self.fontsize
        self.text.config(font=tuple(self.font_params.values()))
    
    def append_image(self, image):
        self.images.append(image)

    def get_last_image(self):
        return self.images[len(self.images) - 1]
    
    def create_image(self, image_data, image_name):
        # Mantener una referencia global a la imagen

        self.append_image(image_data)
        image = self.get_last_image()
        # Asignar la imagen al atributo de la etiqueta de texto
        self.text.image = image
        self.text.image_create(INSERT, image=image, name=image_name)
        self.text.insert(INSERT, "\n")
        self.root.update_idletasks()
    
    def get_selection(self):
        return self.text.get(SEL_FIRST, SEL_LAST)
    