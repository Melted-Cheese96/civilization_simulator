import tkinter as tk
import os
import sys
from tkinter import messagebox
import threading
from time import sleep
import random


#TODO LIST 7/2/19
# Add the ability to load save games
# Test the housing features in a seperate unit test.
# Add more features.
# Continue working on displays all building related options.
# Continue working on displaying all financial related options.
# Bug test GUI and streamline.
# Work on backend for every feature and test extensively.

class Game:
    def __init__(self):
        self.check_for_save_folder()
        self.starting_dir = os.getcwd() 
        self.civ_name = ''  # This variable contains the name of the civilization that the player has chosen
        self.civ_species = ''  # Holds the name of species
        self.wood_increment_amt = 10
        # house1 = SingleHouse(1)
        self.houses = []
        self.total_amount_of_buildings = 0
        self.amount_of_houses = 0
        self.amount_of_workplaces = 0 
        self.occupant_names = [] 
        self.wood_amt = 0
        self.stone_amt = 0
        self.current_population = 0
        self.workplace_stone_amt = 500
        self.money_workplace_amt = 1200
        self.single_house_amt = 100
        self.medium_house_amt = 300
        self.money_amt = 0
        self.advertising_level = 0
        self.neighborhood_count = 0
        self.minimum_year = 1432  # self.year cannot be lower than this
        self.year = 0000  # Variable for what year the player is in.
        self.country = ''  # Country where civilization is based in
        self.starting_window()

    def get_occupant_names(self):
        with open('.names', 'r') as doc:
            content = doc.readlines()
        for name in content:
            self.occupant_names.append(name)

    def save_game_prompt(self, parent_window):
        # Displays what the user will see when they are wanting to save their game.
        parent_window.withdraw()
        save_prompt_window = tk.Toplevel()
        save_prompt_window.title('Save Game')
        save_prompt_window.resizable(width=False, height=False)
        save_prompt_window.protocol('WM_DELETE_WINDOW', lambda: self.back(save_prompt_window, parent_window))
        save_name_entry_label = tk.Label(save_prompt_window, text='Save Name:')
        save_name_entry_label.grid(row=0)
        save_name_entry = tk.Entry(save_prompt_window)
        save_name_entry.grid(row=0, column=1)
        save_game_button = tk.Button(save_prompt_window, text='Save Game')
        save_game_button.grid(row=1, column=1)
        back_button = tk.Button(save_prompt_window, text='Back', command=lambda:self.back(save_prompt_window, parent_window))
        back_button.grid(row=2, column=1)

    def save_game_backend(self, save_name):
        # Saves the player's progress into a file.
        # That file name is called whatever is passed as an argument
        save_name = '.' + save_name 
        os.chdir('.saves')
        if save_name in os.listdir():
            overwrite_save_prompt = messagebox.askyesno('Overwrite Save?', 'A file already exists called {}'.format(save_name))
            if overwrite_save_prompt is True:
                with open(save_name, 'w') as doc:
                    doc.write('MONEY:{} \n'.format(self.money_amt))
                    doc.write('WOOD:{} \n'.format(self.wood_amt))
                    doc.write('STONE:{} \n'.format(self.stone_amt))
                    doc.write('ADVERTISING:{} \n'.format(self.advertising_level))
                    doc.write('WOOD_INCREMENT:{} \n'.format(self.wood_increment_amt))
                    doc.write('YEAR:{}'.format(self.year))
                messagebox.showinfo('Progress Saved!', 'Your progress has been saved!')
                os.chdir(self.starting_dir)

            else:
                messagebox.showinfo('Save Canceled', 'You chose not to overwrite your save!')
                os.chdir(self.starting_dir)
        else:
            with open(save_name, 'w') as doc:
                doc.write('MONEY:{} \n'.format(self.money_amt))
                doc.write('WOOD:{} \n'.format(self.wood_amt))
                doc.write('STONE:{} \n'.format(self.stone_amt))
                doc.write('ADVERTISING:{} \n'.format(self.advertising_level))
                doc.writE('WOOD_INCREMENT:{} \n'.format(self.wood_increment_amt))
                doc.write('YEAR:{}'.format(self.year))
            messagebox.showinfo('Progress Saved!', 'Your Progress Has Been Saved!')
            os.chdir(self.starting_dir)

    def main_game(self, root_window):
        root_window.withdraw()
        main_window = tk.Toplevel()
        self.get_occupant_names()
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

    def display_building_options(self, window):
        # This functions displays all the building related options to the user.
        window.withdraw()
        build_single_house_desc = 'Build a single small home that holds 1 person! Costs {} wood'.format(
            self.single_house_amt)
        build_medium_house_desc = 'Build a medium home that holds up to 4 people! Costs {} wood'.format(
            self.medium_house_amt)
        build_workplace_desc = 'Register new business! - Costs {} dollars and {} stone'.format(
            self.workplace_stone_amt, self.money_workplace_amt)
        building_options_window = tk.Toplevel()
        building_options_window.title('Building Options')
        building_options_window.resizable(width=False, height=False)
        amount_of_total_buildings_desc = 'Total Buildings Count:{}'.format(self.total_amount_of_buildings)
        amount_of_homes_desc = 'Total Homes Count:{}'.format(self.amount_of_houses)
        amount_of_total_buildings_label = tk.Label(building_options_window, text=amount_of_total_buildings_desc)
        amount_of_total_buildings_label.grid(row=0)
        amount_of_homes_label = tk.Label(building_options_window, text=amount_of_homes_desc)
        amount_of_homes_label.grid(row=1)
        build_single_house_button = tk.Button(building_options_window, text=build_single_house_desc)
        build_single_house_button.grid(row=3)
        build_medium_house_button = tk.Button(building_options_window, text=build_medium_house_desc)
        build_medium_house_button.grid(row=4)
        build_workplace_button = tk.Button(building_options_window, text=build_workplace_desc)
        build_workplace_button.grid(row=5)

    def display_buttons(self, window, wood_label_var, money_label_var):
        # This displays all the buttons to a window that is passed as an argument.
        harvest_wood_desc = 'Harvest Wood - Takes 2 hours - Gives {} wood!'.format(self.wood_increment_amt)
        sell_wood_desc = 'Sell Wood - 2 dollars per wood piece!'
        building_options_desc = 'Building Options'
        financial_options = 'Financial Related Options'
        harvest_wood_button = tk.Button(window, text=harvest_wood_desc,
                                        command=lambda:self.add_wood(self.wood_increment_amt, wood_label_var))
        harvest_wood_button.grid(row=3)
        sell_wood_button = tk.Button(window, text=sell_wood_desc,
                                    command=lambda: self.sell_wood(wood_label_var,
                                                                    money_label_var))
        sell_wood_button.grid(row=4)
        building_options_button = tk.Button(window, text=building_options_desc,
                                            command=lambda: self.display_building_options(window))
        building_options_button.grid(row=5)
        financial_options_button = tk.Button(window, text=financial_options)
        financial_options_button.grid(row=6)
        '''
        start_advertising_desc = 'Start Advertising - Attracts more people to your town! - Costs 600 dollars!'
        build_single_house_desc = 'Build a single small home that holds 1 person! Costs {} wood'.format(
            self.single_house_amt)
        build_medium_house_desc = 'Build a medium home that holds up to 4 people! Costs {} wood'.format(
            self.medium_house_amt)
        build_workplace_desc = 'Register new business! - Costs {} dollars and {} stone'.format(
            self.workplace_stone_amt, self.money_workplace_amt)
        save_game_button = tk.Button(window, text='Save Progress', command=lambda:self.save_game_prompt(window))
        save_game_button.grid(row=3)
        harvest_wood_button = tk.Button(window, text=harvest_wood_desc,
                                        command=lambda: self.add_wood(self.wood_increment_amt,  wood_label_var))
        harvest_wood_button.grid(row=4)
        sell_wood_button = tk.Button(window, text=sell_wood_desc, command=lambda: self.sell_wood(wood_label_var,
                                                                                                 money_label_var))
        sell_wood_button.grid(row=5)
        build_single_house_desc = tk.Button(window, text=build_single_house_desc)
        build_single_house_desc.grid(row=6)
        build_medium_house_desc = tk.Button(window, text=build_medium_house_desc)
        build_medium_house_desc.grid(row=7)
        upgrade_advertising_button = tk.Button(window, text=start_advertising_desc,
                                               command=lambda: self.advertising_start(600))
        upgrade_advertising_button.grid(row=8)
        make_new_business_button = tk.Button(window, text=build_workplace_desc, command=lambda:self.register_new_business_window(window))
        make_new_business_button.grid(row=9)
        '''    

    def register_new_business_window(self, previous_window):
        previous_window.withdraw()
        make_new_business_window = tk.Toplevel()
        make_new_business_window.title('New Business')
        make_new_business.resizable(width=False, height=False)
        company_name_entry_label = tk.Label(make_new_business_window, text='Business Name:')
        company_name_entry_label.grid(row=0)
        company_name_entry = tk.Entry()
        company_name_entry.grid(row=0, column=1)
        employee_limit_entry_label = tk.Labe(make_new_business_window, text='Employee Limit:')
        employee_limit_entry_label.grid(row=1)
        employee_limit_entry = tk.Entry(make_new_business_window)
        employee_limit_entry.grid(row=1, column=1)

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
                for item in self.houses:
                    occupant_names = item.return_occupant_names()
                    print(occupant_names)
                    occupant_amount = item.inhabitant_amount
                    number_of_new_people -= occupant_amount
                    house_value = item.check_if_residence_is_full()
                    if house_value is True:
                        item.add_occupant(random.choice(self.occupant_names))
                    else:
                        print('House full!')
                    

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
        load_game = tk.Button(text='Load Game', command=lambda: self.load_game_window(starting_window))
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

    def load_game_window(self, parent_window):  # Reads from a file called ".playernamexample> in .saves and loads the player's progress.
        parent_window.withdraw()
        load_game_prompt = tk.Toplevel()
        load_game_prompt.resizable(width=False, height=False)
        load_game_prompt.protocol('WM_DELETE_WINDOW', lambda: self.back(load_game_prompt, parent_window))
        self.display_available_saves(load_game_prompt, parent_window)

    def display_available_saves(self, window_to_display_to, parent_window):
        #parent_window in this case would be the window from the starting_win function
        os.chdir('.saves')
        items = os.listdir()
        row_count = -1 
        if len(items) == 0:
            messagebox.showinfo('No Saves!', 'You have no savegames!')
            os.chdir(self.starting_dir)
            self.back(window_to_display_to, parent_window)       
        else:
            for save_file_name in os.listdir():
                row_count += 1 
                tk.Button(window_to_display_to, text=save_file_name, command=lambda save_name=save_file_name:print(save_name)).grid(row=row_count)
                

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


class WorkPlace:
    def __init__(self, workplace_type):
        self.workplace_employee_limit = 15
        self.full = False 
        self.workplace_type = workplace_type
        self.number_of_workers = 0
        self.list_of_workers_names = []

    def add_new_worker(self, worker_name):
        if self.number_of_workers < self.workplace_employee_limit:
            self.list_of_workers_names.append(worker_name)
            self.number_of_workers += 1
        else:
            print('Workplace full!')
            self.full = True 

    def remove_worker(self, worker_name):
        self.list_of_workers_names.remove(worker_name)
        self.number_of_workers -= 1 

    def get_workers(self):
        return self.list_of_workers_names

class SingleHouse:
    def __init__(self, inhabitant_amount): # Inhabitant amount should return a
        self.inhabitant_amount = inhabitant_amount
        self.full_house = False 
        self.occupants = []

    def check_if_residence_is_full(self):
        if len(self.occupants) == self.inhabitant_amount:
            self.full_house = True
            return False 
        else:
            self.full_house = False
            return True 
    
    def return_occupant_names(self):
        return self.occupants

    def get_inhabitant_amount(self):
        return self.inhabitant_amount

    def add_occupant(self, occupant_name):
        self.occupants.append(occupant_name)
        return self.occupants


game_instance = Game()
