import tkinter as tk
import os
import sys
from tkinter import messagebox

# To Do List 26/1/19
# Write comments


class Game:
    def __init__(self):
        self.civ_name = ''  # This variable contains the name of the civilization that the player has chosen
        self.civ_species = ''  # Holds the name of species
        self.minimum_year = 1432  # self.year cannot be lower than this
        self.year = 0000  # Variable for what year the player is in.
        self.country = ''  # Country where civilization is based in
        self.main_window = tk.Tk()
        self.main_window.title('Game Options')
        self.main_window.resizable(width=False, height=False)
        self.start_new_game = tk.Button(text='New Game', command=self.new_game_window)
        self.start_new_game.grid(row=0)
        self.load_game = tk.Button(text='Load Game')
        self.load_game.grid(row=1)
        self.quit_game = tk.Button(text='Quit')
        self.quit_game.grid(row=2)

    def new_game_window(self):  # Displays the window for creating a new game
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

    def choose_country(self, parent_window):  # Makes a new window and displays countries to choose from.
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

    def assign_country(self, country, parent_window, child_window):  # Changes self.country to player's choice.
        self.country = country
        messagebox.showinfo('Country chosen!', 'Your civilization will be living in {}!'.format(country))
        self.back(child_window, parent_window)

    def create_civilization(self, civ_name, civ_species_name, starting_year):  # Creates civilization
        if civ_name == '' or civ_species_name == '' or starting_year == '' or self.country == '':
            # Checks if the user has filled out all the requirements.
            messagebox.showerror('Fill out all fields!', 'Please fill out all fields!')
        else:
            self.civ_name = civ_name
            self.civ_species = civ_species_name
            if starting_year.isnumeric():  # Checks if the year that the user has entered is a numeric value
                if starting_year < self.minimum_year:
                    messagebox.showerror('Too low!', 'The year you entered is too low!')
                else:
                    self.year = starting_year
                    print(self.civ_name)
                    print(self.civ_species)
                    print(self.year)
                    print(self.country)
                    messagebox.showinfo('Civilization made!', 'Your civilization has been made!')
            else:
                messagebox.showerror('Invalid format!', 'Please choose a valid year!')

    def back(self, window_to_close, window_to_open):  # Returns the player to the previous window.
        window_to_close.destroy()
        window_to_open.deiconify()

    def load_game(self):  # Reads from a file called ".playernamexample> in .saves and loads the player's progress.
        pass

    def quit(self):  # Destroys the main root window and closes the program.
        self.main_window.destroy()
        sys.exit()

    @staticmethod
    def check_for_save_folder():  # Checks if '.saves' is in the current directory.
        # '.saves' is the directory where the player's progress is stored!
        if '.saves' in os.listdir():
            pass
        else:
            os.mkdir('.saves')


game_instance = Game()
