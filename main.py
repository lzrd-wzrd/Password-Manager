from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import pandas
import os

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Delete previously generated password
    password_entry.delete(0, END)

    password_list = []

    password_list += [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = ''.join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- UPDATE PASSWORD ----------------------------- #

# def update_password():
#     with open(file='password_data.txt') as data_file:
#         data_list = data_file.readlines()
#         print(data_list)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(message=f"These are the details entered: \nWebsite: {website} \nEmail: "
                                               f"{email} \nPassword: "
                                               f"{password} \nIs it okay to save?")
        # if user clicks ok
        if is_ok:
            if os.path.isfile('passwords.csv'):
                # Update existing dataframe and csv file
                data = pandas.read_csv('passwords.csv', index_col=[0])

                # if site already in dataframe, replace password with new password
                if data['Website'].str.contains(website).any():
                    data.loc[data['Website'] == website, 'Password'] = password
                else:
                    # add new row with new password info
                    data.loc[len(data.index)] = [website, email, password]

                data.to_csv('passwords.csv')
                print(data)

            else:
                # Create new dataframe and csv file
                password_dict = {
                    'Website': [website],
                    'Email': [email],
                    'Password': [password]
                }
                password_df = pandas.DataFrame(password_dict)
                print(password_df)
                password_df.to_csv('passwords.csv')

            # Delete previous entries to enhance user experience
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            email_username_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.minsize(width=220, height=220)
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries

website_entry = Entry(width=36)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2)

email_username_entry = Entry(width=36)
email_username_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Buttons

generate_password_button = Button(text='Generate Password', width=11, command=password_generator)
generate_password_button.grid(column=2, row=3)

add_button = Button(text='Add', width=34, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
