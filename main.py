from tkinter import *
from tkinter import messagebox, Menu
import tkinter as tk
import requests
from PIL import ImageTk, Image
from io import BytesIO
import urllib.parse



class Request:
    def __init__(self, method, args, preview_link=None):
        self.args = args
        self.method = method
        self.preview_link = preview_link

inc = 0

def fetch_information(title, poster, date, rating, preview_link):
    global inc
    inc += 1

    text[f'a{inc}'].config(text=title)

    if check_var.get():
        text2[f'a{inc}{inc}'].config(text=date)
    else:
        text2[f'a{inc}{inc}'].config(text="")

    if check_var2.get():
        text3[f'a{inc}{inc}{inc}'].config(text=rating)
    else:
        text3[f'a{inc}{inc}{inc}'].config(text="")

    # Verifica se o link da capa é válido
    if poster and poster != 'N/A':
        try:
            response = requests.get(poster)
            if response.status_code == 200:
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                resized_image = img.resize((140, 200))
                photo2 = ImageTk.PhotoImage(resized_image)
                image[f'b{inc}'].config(image=photo2)
                image[f'b{inc}'].image = photo2
            else:
                messagebox.showinfo("Info", f"Failed to fetch image for {title}. Status code: {response.status_code}")
                # Exibe uma imagem de placeholder e uma mensagem de erro
                display_placeholder_image(inc, error=True)
        except Exception as e:
            messagebox.showinfo("Info", f"Error fetching image for {title}: {e}")
            # Exibe uma imagem de placeholder e uma mensagem de erro
            display_placeholder_image(inc, error=True)
    else:
        messagebox.showinfo("Info", f"No valid image URL for {title}")
        # Exibe uma imagem de placeholder e uma mensagem de erro
        display_placeholder_image(inc, error=True)

    # Exibe o link de prévia se disponível
    if preview_link:
        preview_label = Label(image[f'b{inc}'], text="Preview Link", font=("Arial", 10), fg="white",bg= "black", cursor="hand2")
        preview_label.place(relx=0.5, rely=0.9, anchor=CENTER)
        preview_label.bind("<Button-1>", lambda event, link=preview_link: open_preview_link(link))

def open_preview_link(link):
    # Abrir o link de prévia em um navegador padrão
    import webbrowser
    webbrowser.open_new_tab(link)


def display_placeholder_image(inc, error=False):
    # Imagem de placeholder
    placeholder_image = Image.new('RGB', (140, 200), color='gray')  # Criando uma imagem cinza como placeholder
    placeholder_photo = ImageTk.PhotoImage(placeholder_image)

    # Exibe a imagem de placeholder
    image[f'b{inc}'].config(image=placeholder_photo)
    image[f'b{inc}'].image = placeholder_photo

    # Exibe a mensagem de erro na interface gráfica
    if error:
        error_label = Label(image[f'b{inc}'], text="Image not available", font=("Arial", 10), fg="red", bg="gray")
        error_label.place(relx=0.5, rely=0.5, anchor=CENTER)

def search():
    global inc
    inc = 0
    request = Request('GET', {'q': Search.get()})  # Alterado para {'q': Search.get()} conforme a estrutura da URL da API

    if request.method == 'GET':
        search = urllib.parse.quote(request.args.get('q', ''))
        url = f"https://www.googleapis.com/books/v1/volumes?q={search}&maxResults=5"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                title = volume_info.get('title', 'N/A')
                published_date = volume_info.get('publishedDate', 'N/A')
                rating = volume_info.get('averageRating', 'N/A')

                # Handling authors which is a list
                authors = volume_info.get('authors', ['N/A'])
                authors = ', '.join(authors)

                image_links = volume_info.get('imageLinks', {})
                thumbnail = image_links.get('thumbnail') if 'thumbnail' in image_links else 'N/A'

                preview_link = volume_info.get('previewLink', None)  # Captura o link de prévia

                fetch_information(title, thumbnail, published_date, rating, preview_link)

                if check_var.get() or check_var2.get():
                    frame6.place(x=160, y=600)
                    frame7.place(x=360, y=600)
                    frame8.place(x=560, y=600)
                    frame9.place(x=760, y=600)
                    frame10.place(x=960, y=600)
                else:
                    frame6.place_forget()
                    frame7.place_forget()
                    frame8.place_forget()
                    frame9.place_forget()
                    frame10.place_forget()
        else:
            messagebox.showinfo("Info", "Failed to fetch data from Google Books API.")
    else:
        messagebox.showinfo("Info", "Invalid request method.")




def show_menu(event):
    # Display the menu at the mouse position
    menu.post(event.x_root, event.y_root)


root = Tk()
root.title("Book Recommendation System")
root.geometry("1250x700")
root.config(bg="#111119")
root.resizable(False, False)

###########################################################################################

# icon
icon_image = PhotoImage(file="Images/icon.png")

# background image
heading_image = PhotoImage(file="Images/background.png")
Label(root, image=heading_image, bg="#111119").place(x=-2, y=-2)

# logo
logo_image = PhotoImage(file="Images/logo.png")
Label(root, image=logo_image, bg="#0099ff").place(x=300, y=70)

# heading
heading = Label(root, text="Book Recommendation", font=("Lato", 30, "bold"), fg="white", bg="#0099ff")
heading.place(x=410, y=90)

# search Background image
search_box = PhotoImage(file="Images/Rectangle 2.png")
Label(root, image=search_box, bg="#0099ff").place(x=300, y=155)

# entry box / Search section
Search = StringVar()
search_entry = Entry(root, textvariable=Search, width=24, font=("Lato", 25), bg="white", fg="black", bd=0,
                     highlightthickness=0)
search_entry.place(x=402, y=175)

# Search Button
recommand_button_image = PhotoImage(file="Images/Search.png")
recommand_button = Button(root, image=recommand_button_image, bg="#0099ff", bd=0, highlightthickness=0,
                          activebackground="#0099ff", cursor="hand2", command=search)
recommand_button.place(x=860, y=168)

# setting button
Setting_image = PhotoImage(file="Images/setting.png")
setting = Button(root, image=Setting_image, bd=0, highlightthickness=0, cursor="hand2", activebackground="#0099ff",
                 bg="#0099ff")
setting.place(x=1050, y=173)
setting.bind('<Button-1>', show_menu)

menu = Menu(root, tearoff=0)  # Menu for search button

check_var = BooleanVar()
menu.add_checkbutton(label="Publish Date", variable=check_var,
                     command=lambda: messagebox.showinfo("Publish Date Check", 
                                                          f"Publish Date check Option is {'checked' if check_var.get() else 'unchecked'}"))

check_var2 = BooleanVar()
menu.add_checkbutton(label="Rating", variable=check_var2,
                     command=lambda: messagebox.showinfo("Rating Check", 
                                                          f"Rating check Option is {'checked' if check_var2.get() else 'unchecked'}"))

# logout button
Logout_image = PhotoImage(file="Images/logout.png")
Button(root, image=Logout_image, bg="#0099ff", cursor="hand1", bd=0, highlightthickness=0,
       activebackground="#0099ff", command=lambda: root.destroy()).place(x=1150, y=20)

###########################################################################################

###################first frame#######################

frame1 = Frame(root, width=150, height=240, bg="white")
frame2 = Frame(root, width=150, height=240, bg="white")
frame3 = Frame(root, width=150, height=240, bg="white")
frame4 = Frame(root, width=150, height=240, bg="white")
frame5 = Frame(root, width=150, height=240, bg="white")
frame1.place(x=160, y=350)
frame2.place(x=360, y=350)
frame3.place(x=560, y=350)
frame4.place(x=760, y=350)
frame5.place(x=960, y=350)

########################################################

####################Book Title######################
text = {"a1": Label(frame1, text="", font=("arial", 10), fg="green", bg="white"),
        "a2": Label(frame2, text="", font=("arial", 10), fg="green", bg="white"),
        "a3": Label(frame3, text="", font=("arial", 10), fg="green", bg="white"),
        "a4": Label(frame4, text="", font=("arial", 10), fg="green", bg="white"),
        "a5": Label(frame5, text="", font=("arial", 10), fg="green", bg="white")}
text["a1"].place(x=10, y=4)
text["a2"].place(x=10, y=4)
text["a3"].place(x=10, y=4)
text["a4"].place(x=10, y=4)
text["a5"].place(x=10, y=4)
####################################################

################Poster/ Image of book###############
image = {
    'b1': Label(frame1, bg='white'),
    'b2': Label(frame2, bg='white'),
    'b3': Label(frame3, bg='white'),
    'b4': Label(frame4, bg='white'),
    'b5': Label(frame5, bg='white')
}
for key in image:
    image[key].place(x=5, y=30)

####################################################

###########################################################################################

################second frame########################

frame6 = Frame(root, width=150, height=50, bg="#e6e6e6")
frame7 = Frame(root, width=150, height=50, bg="#e6e6e6")
frame8 = Frame(root, width=150, height=50, bg="#e6e6e6")
frame9 = Frame(root, width=150, height=50, bg="#e6e6e6")
frame10 = Frame(root, width=150, height=50, bg="#e6e6e6")

##########################################################

##############published date##################
text2 = {'a11': Label(frame6, text="date", font=("arial", 10), fg="red", bg="#e6e6e6"),
         'a22': Label(frame7, text="date", font=("arial", 10), fg="red", bg="#e6e6e6"),
         'a33': Label(frame8, text="date", font=("arial", 10), fg="red", bg="#e6e6e6"),
         'a44': Label(frame9, text="date", font=("arial", 10), fg="red", bg="#e6e6e6"),
         'a55': Label(frame10, text="date", font=("arial", 10), fg="red", bg="#e6e6e6")}
text2['a11'].place(x=10, y=4)
text2['a22'].place(x=10, y=4)
text2['a33'].place(x=10, y=4)
text2['a44'].place(x=10, y=4)
text2['a55'].place(x=10, y=4)
###############################################

####################Rating#####################
text3 = {'a111': Label(frame6, text="rating", font=("arial", 10), fg="black", bg="#e6e6e6"),
         'a222': Label(frame7, text="rating", font=("arial", 10), fg="black", bg="#e6e6e6"),
         'a333': Label(frame8, text="rating", font=("arial", 10), fg="black", bg="#e6e6e6"),
         'a444': Label(frame9, text="rating", font=("arial", 10), fg="black", bg="#e6e6e6"),
         'a555': Label(frame10, text="rating", font=("arial", 10), fg="black", bg="#e6e6e6")}
text3['a111'].place(x=20, y=30)
text3['a222'].place(x=20, y=30)
text3['a333'].place(x=20, y=30)
text3['a444'].place(x=20, y=30)
text3['a555'].place(x=20, y=30)
###############################################



###########################################################################################

root.mainloop()
