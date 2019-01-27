import tkinter as tk
import os
import sys
from tkinter import messagebox
import threading
from time import sleep
import random


# To Do List 26/1/19


class Game:
    def __init__(self):
        self.civ_name = ''  # This variable contains the name of the civilization that the player has chosen
        self.civ_species = ''  # Holds the name of species
        self.wood_increment_amt = 100
        self.houses = []
        self.wood_amt = 0
        self.stone_amt = 0
        self.current_population = 0
        self.single_house_amt = 100
        self.medium_house_amt = 300
        self.money_amt = 0
        self.advertising_level = 0
        self.neighborhood_count = 0
        self.minimum_year = 1432  # self.year cannot be lower than this
        self.year = 0000  # Variable for what year the player is in.
        self.country = ''  # Country where civilization is based in
        self.starting_window()

    def main_game(self, root_window):
        root_window.withdraw()
        main_window = tk.Toplevel()
        main_window.title('Civilization Menu')
        main_window.resizable(width=False, height=False)
        main_window.protocol("WM_DELETE_WINDOW", lambda: self.quit(root_window))
        current_money_amt_display = tk.Label(main_window, text='Money:{}'.format(self.money_amt))
        current_money_amt_display.grid(row=0)
        current_wood_amt_display = tk.Label(main_window, text='Wood:{}'.format(self.wood_amt))
        current_wood_amt_display.grid(row=1)
        current_stone_amt_display = tk.Label(main_window, text='Stone:{}'.format(self.stone_amt))
        current_stone_amt_display.grid(row=2)
        self.display_buttons(main_window, current_wood_amt_display, current_money_amt_display)

    def display_buttons(self, window, wood_label_var, money_label_var):
        # upgrade_advertising_desc = 'Upgrade advertising level to {}! This attracts more people!'.format(
            # self.advertising_level+1)
        harvest_wood_desc = 'Harvest Wood - Takes 2 hours - Gives 100 wood!'
        sell_wood_desc = 'Sell Wood - 2 dollars per wood piece!'
        start_advertising_desc = 'Start Advertising - Attracts more people to your town! - Costs 600 dollars!'
        build_single_house_desc = 'Build a single small home that holds 1 person! Costs {} wood'.format(
            self.single_house_amt)
        build_medium_house_desc = 'Build a medium home that holds up to 4 people! Costs {} wood'.format(
            self.medium_house_amt)
        harvest_wood_button = tk.Button(window, text=harvest_wood_desc,
                                        command=lambda: self.add_wood(self.wood_increment_amt,  wood_label_var))
        harvest_wood_button.grid(row=3)
        sell_wood_button = tk.Button(window, text=sell_wood_desc, command=lambda: self.sell_wood(wood_label_var,
                                                                                                 money_label_var))
        sell_wood_button.grid(row=4)
        build_single_house_desc = tk.Button(window, text=build_single_house_desc)
        build_single_house_desc.grid(row=5)
        build_medium_house_desc = tk.Button(window, text=build_medium_house_desc)
        build_medium_house_desc.grid(row=6)
        upgrade_advertising_button = tk.Button(window, text=start_advertising_desc,
                                               command=lambda: self.advertising_start(600))
        upgrade_advertising_button.grid(row=7)

    def advertising_start(self, amount_needed_to_upgrade):  # Creates a new thread and runs it.
        if self.money_amt >= amount_needed_to_upgrade:
            self.money_amt -= amount_needed_to_upgrade
            self.advertising_level += 1
            start_advertising_thread = threading.Thread(target=self.population_increment)
            start_advertising_thread.start()
        else:
            messagebox.showerror('Not enough money!', 'You do not have enough money! '
                                                      'You need {} dollars'.format(amount_needed_to_upgrade))

    def population_increment(self):
        '''
        This is the "advertising" upgrade. All this does it increment self.population by a random amount every few
        seconds. Then another function is going to check if all those new people can get homes, if so. It adds
        +1 to the self.population variable.
        '''

        while True:
            if self.advertising_level == 1:
                number_of_new_people = random.randint(1, 20)
                print(number_of_new_people)

    def sell_wood(self, wood_amt_display, money_amt_display):
        # This functions sells all the wood the player has in their inventory
        total_money_gained = 0
        for x in range(0, self.wood_amt):
            total_money_gained += 2
            self.money_amt += 2
        self.wood_amt = 0
        wood_amt_display.config(text='Wood:{}'.format(self.wood_amt))
        money_amt_display.config(text='Money:{}'.format(self.money_amt))
        messagebox.showinfo('Wood has been sold!', 'You sold all your wood for a sum of {} dollars'.format(
            total_money_gained))

    def add_wood(self, wood_amt, wood_label_var):
        # This function adds a specified wood amount to the player's total wood.
        messagebox.showinfo('Working...', 'You go out and harvest wood.')
        sleep(2)
        self.wood_amt += wood_amt
        print(self.wood_amt)
        wood_label_var.config(text='Wood:{}'.format(self.wood_amt))

    def starting_window(self):
        starting_window = tk.Tk()
        starting_window.title('Game Options')
        starting_window.resizable(width=False, height=False)
        start_new_game = tk.Button(text='New Game', command=lambda: self.new_game_window(starting_window))
        start_new_game.grid(row=0)
        load_game = tk.Button(text='Load Game')
        load_game.grid(row=1)
        quit_button = tk.Button(text='Quit', command=lambda: self.quit(starting_window))
        quit_button.grid(row=2)

    def new_game_window(self, parent_window):  # Displays the window for creating a new game
        parent_window.withdraw()
        new_game_window = tk.Toplevel()
        new_game_window.resizable(width=False, height=False)
        new_game_window.title('New Game')
        new_game_window.protocol("WM_DELETE_WINDOW", lambda: self.back(new_game_window, parent_window))
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
                                               command=lambda: self.create_civilization(civ_name_entry.get(),
                                                                                        species_name_entry.get(),
                                                                                        starting_year_entry.get(),
                                                                                        parent_window,
                                                                                        new_game_window))
        create_civilization_button.grid(row=4, column=1)
        cancel_button = tk.Button(new_game_window, text='Cancel', command=lambda: self.back(new_game_window,
                                                                                            parent_window))
        cancel_button.grid(row=3)

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

    def create_civilization(self, civ_name, civ_species_name, starting_year, root_window, previous_win):  # Creates civilization
        if civ_name == '' or civ_species_name == '' or starting_year == '' or self.country == '':
            # Checks if the user has filled out all the requirements.
            messagebox.showerror('Fill out all fields!', 'Please fill out all fields!')
        else:
            self.civ_name = civ_name
            self.civ_species = civ_species_name
            if starting_year.isnumeric():  # Checks if the year that the user has entered is a numeric value
                if int(starting_year) < self.minimum_year:
                    messagebox.showerror('Too low!', 'The year you entered is too low!')
                else:
                    confirmation_message = 'Are you sure you want to create {}?'.format(civ_name)
                    confirmation = messagebox.askyesno('Confirm?', '{}'.format(confirmation_message))
                    if confirmation is True:
                        self.year = int(starting_year)
                        print(self.civ_name)
                        print(self.civ_species)
                        print(self.year)
                        print(self.country)
                        messagebox.showinfo('Civilization made!', 'Your civilization has been made!')
                        previous_win.withdraw()
                        self.main_game(root_window)
                    else:
                        messagebox.showinfo('Civilization not made!', 'You did not make your civilization!')
                        self.civ_name = ''
                        self.civ_species = ''
            else:
                messagebox.showerror('Invalid format!', 'Please choose a valid year!')

    @staticmethod
    def back(window_to_close, window_to_open):  # Returns the player to the previous window.
        window_to_close.destroy()
        window_to_open.deiconify()

    def load_game(self):  # Reads from a file called ".playernamexample> in .saves and loads the player's progress.
        pass

    def quit(self, window):  # Destroys the main root window and closes the program.
        window.destroy()
        sys.exit()

    @staticmethod
    def check_for_save_folder():  # Checks if '.saves' is in the current directory.
        # '.saves' is the directory where the player's progress is stored!
        if '.saves' in os.listdir():
            pass
        else:
            os.mkdir('.saves')


class SingleHouse:
    def __init__(self, inhabitant_amount): # Inhabitant amount should return a
        self.inhabitant_amount = inhabitant_amount
        self.occupants = []

    def get_inhabitant_amount(self):
        return self.inhabitant_amount

    def add_occupant(self, occupant_name):
        self.occupants.append(occupant_name)
        return self.occupants


game_instance = Game()
