
from PIL import ImageGrab
import PIL
from datetime import datetime
import os.path
from tkinter import END, PhotoImage, filedialog, INSERT, SEL_LAST, SEL_FIRST, SEL
import pickle
import threading
import tkinter as tk
from tkinter import messagebox

def paste_image(event=None, text_editor=None):
    if not text_editor:
        print("Error, no hay un editor de texto asignado.")
        return
    
    try:
        img = run_with_timeout(get_clipboard_img, timeout=0.1)
    except Exception as _:
        return
    if not img:
        return
    
    img_name = get_unique_name("image")
    img_filename = f'{img_name}.png'
    img_directory = 'saved_images'

    img_path = save_img(img_directory, img_filename, img)

    if not img_path:
        return
    text_editor.images_paths.append(img_path)

    img_file = open_img(img_path)

    image_data = img_file.read()
    image_reference = PhotoImage(data=image_data)

    #text_editor.append_image(image_reference)
    text_editor.create_image(image_reference, img_name)
    


def get_unique_name(name: str):
    """
    Get unique name based on the actual date
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{name}_{timestamp}.png"

def increase_fontsize(event=None, text_editor=None, amount=4):
    if not text_editor:
        return
    text_editor.update_font_size(amount)

def decrease_fontsize(event=None, text_editor=None, amount=-4):
    if not text_editor:
        return
    text_editor.update_font_size(amount)

def restore_fontsize(event=None, text_editor=None):
    if not text_editor:
        return
    text_editor.restore_fontsize()

def toggle_bold(event=None, text_editor=None):
    """ global bold
    global text
    bold = not bold
    if bold:
        text.insert(END, 'a', 'bold')
    else:
        text.insert(END, 'a', '') """
    if not text_editor:
        return

def save_to_file(event=None, text_editor=None):

    if not text_editor:
        return
    
    filepath = get_save_filepath(text_editor, "Pickle files", '*.pkl')
    data_to_save = get_data_to_save(text_editor)

    with open(filepath, 'wb') as f:
        pickle.dump(data_to_save, f)

def open_file(event=None, text_editor=None):
    if not text_editor:
        return
    filename = filedialog.askopenfilename(initialdir="../../Uni/Cuarto", filetypes=[('Pickle files', '*.pkl')])

    if not filename:
        return
    
    text_editor.currentfile = filename

    text_editor.images = []

    img_names = text_editor.text.image_names()
    for name in img_names:
        index = text_editor.text.index(name)
        text_editor.text.delete(index, index)
    
            
    with open(filename, 'rb') as f:
        loaded_data = pickle.load(f)

    # Restaurar el contenido del texto y las imágenes
    text_editor.text.delete('1.0', END)
    for item in loaded_data:
        if item[0] is None:
            text_content = item[1]
            text_editor.text.insert(END, f"{text_content}\n")
        if item[0] is not None:
            #if item[0] == "tag":
            #    print(item)
            #else:
            index, image_path = item
            image = PhotoImage(file=f"saved_images/{image_path}.png")
            text_editor.images.append(image)
            text_editor.text.image_create(index, image=image, name=image_path)
    text_editor.root.update_idletasks()


def do_backspace(event=None, text_editor=None):
    if not text_editor:
        return
    previous = text_editor.text.get("insert -1 chars", "insert")
    
    special_chars = " [](){}\"'"

    i = 1
    while previous not in special_chars and previous != "\n" and i < 100:
        i += 1
        previous = text_editor.text.get(f"insert -{i} chars", f"insert -{i - 1} chars")
    text_editor.text.delete(f"insert -{i - 1} chars", "insert")

    return "break"


def get_save_filepath(text_editor, filetype, extension):
    if not text_editor.currentfile:
        filepath = filedialog.asksaveasfilename(initialdir="../../Uni/Cuarto", filetypes=[(filetype, extension), ("All files", "*.*")])

        if not filepath:
            return text_editor.currentfile

        text_editor.currentfile = filepath
        return filepath
    return text_editor.currentfile

def get_data_to_save(text_editor):
    data_to_save = []

    text_content = text_editor.text.get('1.0', END)

    data_to_save.append((None, text_content))

    #data_to_save.append(("tag", etiquetas_con_rangos))

    all_images = text_editor.text.image_names()
    for image in all_images:
        index = text_editor.text.index(image)
        data_to_save.append((index, f"{image}"))
    return data_to_save

def save_img(img_directory, img_filename, img):
    img_path = os.path.join(img_directory, img_filename)

    img.save(img_path, 'PNG')

    if not os.path.exists(img_path):
        return None
    
    return img_path

def open_img(img_path):
    return open(img_path, 'rb')

def is_letter(character):
    character.isalpha()

def is_special_char(char):
    """ Implementar función para borrar con ctrl + backspace hasta que se encuentre un char especial """
    pass



def get_clipboard_img():
    try:
        image = ImageGrab.grabclipboard()
        if isinstance(image, PIL.Image.Image):
            return image
        return None
    except Exception as _:
        return None

def run_with_timeout(func, args=(), kwargs={}, timeout=5):
    result = [None]
    exception = [None]

    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        thread._stop()
        raise TimeoutError("La función ha excedido el tiempo máximo de espera")
    if exception[0] is not None:
        raise exception[0]
    
    return result[0]


def open_code_file(event=None, text_editor=None):
    if not text_editor:
        return

    filepath = filedialog.askopenfilename(initialdir=".", filetypes=[('All files', '*')])

    if not filepath:
        return
    
    text_editor.currentfile = filepath

    file = open(filepath)

    text_editor.clear()

    text_editor.text.insert(1.0, file.read())


def save_to_code_file(event=None, text_editor=None):
    if not text_editor:
        return
    
    filepath = get_save_filepath(text_editor, "All files", '')

    if filepath:
        try:
            with open(filepath, 'w') as file:
                text_content = text_editor.text.get("1.0", "end-1c")
                file.write(text_content)
        except Exception as _:
            return

def close_char(event=None, text_editor=None, chars=None):
    if not text_editor:
        return
    if not chars:
        return        
    if text_editor.text.tag_ranges(SEL):
        text_editor.text.insert(SEL_FIRST, chars[0])
        text_editor.text.insert(SEL_LAST, chars[1])
        return 'break'
    text_editor.text.insert(INSERT, chars[0])

    text_editor.text.insert(INSERT, chars[1])
    current_position = text_editor.text.index(INSERT)
    
    if current_position != "1.0":
        text_editor.text.mark_set("insert", "insert-1c")
    return 'break'


def do_tab(event=None, text_editor=None, tab=True):
    if not text_editor:
        return
    if text_editor.text.tag_ranges(SEL):
        sel_first = text_editor.text.index("sel.first")
        sel_first = sel_first.split(".")
        sel_last = text_editor.text.index("sel.last")
        sel_last = sel_last.split(".")
        line_start = text_editor.text.index(f"{sel_first[0]}.0")


        sel_first_parts = int(sel_first[0])
        sel_last_parts = int(sel_last[0])

        for line_num in range(sel_first_parts, sel_last_parts + 1):
            line_start = f"{line_num}.0"
            if (tab):
                text_editor.text.insert(line_start, "\t")
            else:
                line_start = f"{line_num}.0"
                line_end = f"{line_num}.end"
                line_text = text_editor.text.get(line_start, line_end)
                if line_text.startswith("\t"):
                    # Eliminar la tabulación al principio de la línea
                    updated_line = line_text[1:]
                    # Actualizar el texto de la línea en el widget de texto
                    text_editor.text.replace(line_start, line_end, updated_line)

        return 'break'

    
def consult_gemini(event=None, text_editor=None):
    if not text_editor:
        return

    query = text_editor.text.selection_get()

    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    #root.mainloop()
    
    response = text_editor.ai_model.generate_content(f"{query} Explicame detalladamente")
    
    
    
    # Muestra la respuesta en una ventana emergente
    custom_box = tk.Toplevel()
    custom_box.title("Respuesta de Gemini")

    # Etiqueta para mostrar el mensaje
    label = tk.Label(custom_box, text=response.text)
    label.pack(padx=20, pady=10)

    # Botón para cerrar el cuadro de diálogo
    close_button = tk.Button(custom_box, text="Cerrar", command=custom_box.destroy)
    # Botón para copiar la respuesta de gemini
    copy_button = tk.Button(custom_box, text="Copiar respuesta", command=custom_box.destroy)
    copy_button.pack(pady=10)
    close_button.pack(pady=10)

    # Establecer el tamaño mínimo de la ventana
    custom_box.minsize(width=200, height=100)

    return "break"

def insert_text(event=None, text_editor=None, text=""):
    if not text_editor:
        return
    if not text:
        return
    if text_editor.text.tag_ranges(SEL):
        text_editor.text.insert(SEL_FIRST, text[0:len(text)//2])
        text_editor.text.insert(SEL_LAST, text[len(text)//2:])
        return 'break'
    text_editor.text.insert(INSERT, text)
    return 'break'