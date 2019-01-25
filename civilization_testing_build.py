import tkinter as tk
import os
import sys
from tkinter import messagebox

# To Do List 25/1/19

class Game:
    def __init__(self):
        self.civ_name = ''
        self.civ_species = ''
        self.year = 0000
        self.country = ''
        self.main_window = tk.Tk()
        self.main_window.title('Game Options')
        self.main_window.resizable(width=False, height=False)
        self.start_new_game = tk.Button(text='New Game', command=self.new_game_window)
        self.start_new_game.grid(row=0)
        self.load_game = tk.Button(text='Load Game')
        self.load_game.grid(row=1)
        self.quit_game = tk.Button(text='Quit')
        self.quit_game.grid(row=2)

    def new_game_window(self):
        self.main_window.withdraw()
        new_game_window = tk.Toplevel()
        new_game_window.resizable(width=False, height=False)
        new_game_window.title('New Game')
        new_game_window.protocol("WM_DELETE_WINDOW", lambda: self.back(new_game_window, self.main_window))
        civ_name_label = tk.Label(new_game_window, text='Civ Name')
        civ_name_label.grid(row=0)
        civ_name_entry = tk.Entry(new_game_window)
        civ_name_entry.grid(row=0, column=1)
        species_name_label = tk.Label(new_game_window, text='Species Name:')
        species_name_label.grid(row=1)
        species_name_entry = tk.Entry(new_game_window)
        species_name_entry.grid(row=1, column=1)
        starting_year_label = tk.Label(new_game_window, text='Starting Year:')
        starting_year_label.grid(row=2)
        starting_year_entry = tk.Entry(new_game_window)
        starting_year_entry.grid(row=2, column=1)
        choose_country = tk.Button(new_game_window, text='Choose Country',
                                   command=lambda: self.choose_country(new_game_window))
        choose_country.grid(row=3, column=1)
        create_civilization_button = tk.Button(new_game_window, text='Create',
                                               command = lambda: self.create_civilization(civ_name_entry.get(),
                                                                                          species_name_entry.get(),
                                                                                          starting_year_entry.get()))
        create_civilization_button.grid(row=4, column=1)

    def choose_country(self, parent_window):
        parent_window.withdraw()
        country_window = tk.Toplevel()
        country_window.title('Choose Country')
        country_window.resizable(width=False, height=False)
        country_window.protocol("WM_DELETE_WINDOW", lambda: self.back(country_window, parent_window))
        instructions_label = tk.Label(country_window, text='Choose your country!')
        instructions_label.grid(row=0)
        america_country_choice = tk.Button(country_window, text='America',
                                           command=lambda: self.assign_country('America', parent_window,
                                                                               country_window))
        america_country_choice.grid(row=1)
        australia_country_choice = tk.Button(country_window, text='Australia',
                                             command=lambda: self.assign_country('Australia', parent_window,
                                                                                 country_window))
        australia_country_choice.grid(row=2)
        europe_country_choice = tk.Button(country_window, text='Europe',
                                          command=lambda: self.assign_country('Europe', parent_window,
                                                                              country_window))
        europe_country_choice.grid(row=3)

    def assign_country(self, country, parent_window, child_window):
        self.country = country
        messagebox.showinfo('Country chosen!', 'Your civilization will be living in {}!'.format(country))
        self.back(child_window, parent_window)

    def create_civilization(self, civ_name, civ_species_name, starting_year):
        if civ_name == '' or civ_species_name == '' or starting_year == '' or self.country == '':
            messagebox.showerror('Fill out all fields!', 'Please fill out all fields!')
        else:
            self.civ_name = civ_name
            self.civ_species = civ_species_name
            if starting_year.isnumeric():
                self.year = starting_year
                print(self.civ_name)
                print(self.civ_species)
                print(self.year)
                print(self.country)
            else:
                messagebox.showerror('Invalid format!', 'Please choose a valid year!')


    def back(self, window_to_close, window_to_open):
        window_to_close.destroy()
        window_to_open.deiconify()

    def load_game(self):
        pass

    def quit(self):
        self.main_window.destroy()
        sys.exit()

    @staticmethod
    def check_for_save_folder(self):
        if '.saves' in os.listdir():
            pass
        else:
            os.mkdir('.saves')

game_instance = Game()