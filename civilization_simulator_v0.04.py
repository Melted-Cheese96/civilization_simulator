import tkinter as tk
import os
import sys
from tkinter import messagebox
import threading
from time import sleep
import random


# TODO LIST 9/2/19
# Add the ability to load save games
# Test the housing features in a seperate unit test.
# Add more features.
# Continue working on displays all building related options.
# Continue working on displaying all financial related options.
# Bug test GUI and streamline.
# Work on backend for every feature and test extensively.
# Implement load save function once the base stats are finished
# Edit the save func to accomodate for the new stats that have been added!
# Implement the population incremention func from unit test
# Add the ability to make neighborhood districts to place houses in.


class Game:
    def __init__(self):
        self.check_for_save_folder() # Check if '.saves' is in current directory.
        self.starting_dir = os.getcwd() # Directory which script was started in.
        self.civ_name = ''  # This variable contains the name of the civilization that the player has chosen
        self.civ_species = ''  # Holds the name of species
        self.wood_increment_amt = 10 # How much wood to give the player each time they harvest.
        # house1 = SingleHouse(1)
        self.houses = [] # Keeps track of the created house objects
        self.total_amount_of_buildings = 0  # Counter for the total amount of buildings built in town.
        self.amount_of_houses = 0  # Counter for the number of homes built
        self.amount_of_workplaces = 0  # Counter for the number of workplaces.
        self.occupant_names = []  # Stores the names of occupants that are in the town.
        self.wood_amt = 1500  # Displays amount of wood the player has.
        self.stone_amt = 0  # Displays amount of stone the player has.
        self.current_population = 0  # Displays current population of town.
        self.workplace_stone_amt = 500  # The amount of stone needed to build a workplace.
        self.district_objects = [] # Stores the created district objects
        self.district_wood_cost = 1000
        self.district_cost = 500
        self.district_counter = 0
        self.money_workplace_amt = 1200  # The amount needed to build a workplace.
        self.single_house_amt = 100  # The amount needed to build a small sized house.
        self.single_house_cost = 400
        self.medium_house_amt = 300 # The amount needed to build a medium sized house.
        self.money_amt = 650 # Stores the amount of money the player has in total.
        self.population_increment_level = 0
        self.population_increment_money_price = 600 # Amount needed to upgrade advertising.
        self.neighborhood_count = 0 # Amount of neighborhood districts in the town.
        self.minimum_year = 1432  # self.year cannot be lower than this.
        self.year = 0000  # Variable for what year the player is in.
        self.country = ''  # Country where civilization is based in
        self.starting_window()

    def get_occupant_names(self):
        with open('.names', 'r') as doc:
            content = doc.readlines()
        for name in content:
            self.occupant_names.append(name)

    def save_game_prompt(self):
        # Displays what the user will see when they are wanting to save their game.
        save_prompt_window = tk.Toplevel()
        save_prompt_window.title('Save Game')
        save_prompt_window.resizable(width=False, height=False)
        save_name_entry_label = tk.Label(save_prompt_window, text='Save Name:')
        save_name_entry_label.grid(row=0)
        save_name_entry = tk.Entry(save_prompt_window)
        save_name_entry.grid(row=0, column=1)
        save_game_button = tk.Button(save_prompt_window, text='Save Game',
                                     command=lambda:self.save_game_backend(save_name_entry.get()))
        save_game_button.grid(row=1, column=1)

    def save_game_backend(self, save_name):
        # Saves the player's progress into a file.
        # That file name is called whatever is passed as an argument
        save_name = '.' + save_name
        os.chdir('.saves')
        if save_name in os.listdir():
            overwrite_save_prompt = messagebox.askyesno('Overwrite Save?',
                                                        'A file already exists called {}. Do you want to overwrite {}?'
                                                        .format(save_name, save_name))
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
                doc.write('WOOD_INCREMENT:{} \n'.format(self.wood_increment_amt))
                doc.write('YEAR:{}'.format(self.year))
            messagebox.showinfo('Progress Saved!', 'Your Progress Has Been Saved!')
            os.chdir(self.starting_dir)

    def main_game(self, root_window):
        root_window.withdraw()
        main_window = tk.Toplevel()
        # self.get_occupant_names()
        main_window.title('Civilization Menu')
        main_window.resizable(width=False, height=False)
        main_window.protocol("WM_DELETE_WINDOW", lambda: self.quit(root_window))
        game_options_drop_menu = tk.Menu()
        main_window.configure(menu=game_options_drop_menu)
        options_menu = tk.Menu(game_options_drop_menu)
        game_options_drop_menu.add_cascade(label='Options...', menu=options_menu)
        options_menu.add_command(label='Save...', command=lambda:self.save_game_prompt())
        options_menu.add_command(label='Return To Main Menu...',
                                 command=lambda:self.return_player_to_main_menu(main_window, root_window))
        current_money_amt_display = tk.Label(main_window, text='Money:{}'.format(self.money_amt))
        current_money_amt_display.grid(row=0)
        current_wood_amt_display = tk.Label(main_window, text='Wood:{}'.format(self.wood_amt))
        current_wood_amt_display.grid(row=1)
        current_stone_amt_display = tk.Label(main_window, text='Stone:{}'.format(self.stone_amt))
        current_stone_amt_display.grid(row=2)
        population_label = tk.Label(main_window, text='Population:{}'.format(self.current_population))
        population_label.grid(row=3)
        self.display_buttons(main_window, current_wood_amt_display, current_money_amt_display, root_window,
                             population_label)

    def build_single_home(self, money_label, wood_label):
        if self.wood_amt >= self.single_house_amt and self.money_amt >= self.single_house_cost:
            self.money_amt -= self.single_house_cost
            self.wood_amt -= self.single_house_amt
            money_label.configure(text='Money:{}'.format(self.money_amt))
            wood_label.configure(text='Wood:{}'.format(self.wood_amt))
            single_home_obj = HomeTemplate(1)
            self.houses.append(single_home_obj)
            print(self.houses)
            messagebox.showinfo('Home purchased!', 'A new home has been purchased!')
            # Continue
        else:
            messagebox.showerror('Insufficient Funds/Materials!', 'You have insufficient funds/materials!')

    def display_available_districts(self, window):
        row_count = -1
        for item in self.district_objects:
            row_count += 1
            district_name = item.district_name
            tk.Button(window, text=district_name).grid(row=row_count)
                # print(item.district_name)

    def choose_district_window(self): # This function runs when the player chooses to create a new home.
        districts = self.district_objects
        if len(districts) == 0:
            messagebox.showerror('Create a District!', 'You need to create a district before you can build a home!')
        else:
            show_districts_window = tk.Toplevel()
            show_districts_window.resizable(width=False, height=False)
            show_districts_window.title('Choose District')
            self.display_available_districts(show_districts_window)

    def display_building_options(self, window, money_label, wood_label):
        # This functions displays all the building related options to the user.
        # window.withdraw()
        build_single_house_desc = 'Build a single small home that holds 1 person! Costs {} wood and {} dollars'.format(
            self.single_house_amt, self.single_house_cost)
        build_medium_house_desc = 'Build a medium home that holds up to 4 people! Costs {} wood'.format(
            self.medium_house_amt)
        build_workplace_desc = 'Register new business! - Costs {} dollars and {} stone'.format(
            self.workplace_stone_amt, self.money_workplace_amt)
        # build_district_desc = 'Build a district - Costs {} dollars and {} wood'.format(
          #   self.district_cost, self.district_wood_cost)
        building_options_window = tk.Toplevel()
        building_options_window.title('Building Options')
        building_options_window.resizable(width=False, height=False)
        amount_of_total_buildings_desc = 'Total Buildings Count:{}'.format(self.total_amount_of_buildings)
        amount_of_homes_desc = 'Total Homes Count:{}'.format(self.amount_of_houses)
        amount_of_total_buildings_label = tk.Label(building_options_window, text=amount_of_total_buildings_desc)
        amount_of_total_buildings_label.grid(row=0)
        amount_of_homes_label = tk.Label(building_options_window, text=amount_of_homes_desc)
        amount_of_homes_label.grid(row=1)
        # build_new_district = tk.Button(building_options_window, text=build_district_desc)
        # build_new_district.grid(row=2)
        # build_single_house_button = tk.Button(building_options_window, text=build_single_house_desc,
          #                                     command=lambda:self.build_single_home(money_label, wood_label))
        build_single_house_button = tk.Button(building_options_window, text=build_single_house_desc,
                                              command=self.choose_district_window)
        build_single_house_button.grid(row=2)
        build_single_house_button.grid(row=3)
        build_medium_house_button = tk.Button(building_options_window, text=build_medium_house_desc)
        build_medium_house_button.grid(row=4)
        build_workplace_button = tk.Button(building_options_window, text=build_workplace_desc)
        build_workplace_button.grid(row=5)

    def display_financial_options(self, previous_window, population_label, money_label):
        next_population_increment_level = self.population_increment_level + 1
        financial_options_window = tk.Toplevel()
        financial_options_window.title('Financial Options')
        financial_options_window.resizable(width=False, height=False)
        increment_population_desc = 'Upgrade your population increment to level {} - Costs {} dollars'.\
            format(next_population_increment_level, self.population_increment_money_price)
        if next_population_increment_level > 4:
            pass
        else:
            increment_population_button = tk.Button(financial_options_window, text=increment_population_desc,
                                                   command=lambda:self.start_increment_population_thread(population_label,
                                                                                                         money_label))
            increment_population_button.grid(row=0)

    def display_town_options(self, money_label, wood_label):
        make_new_district_desc = 'Create a new district for houses - Costs {} wood and {} dollars'.format(
            self.district_wood_cost, self.district_cost)
        all_districs_desc = 'Total Districts:{}'.format(self.district_counter)
        town_options_window = tk.Toplevel()
        town_options_window.title('Town Options')
        town_options_window.resizable(width=False, height=False)
        districts_label = tk.Label(town_options_window, text=all_districs_desc)
        districts_label.grid(row=0)
        make_new_district_button = tk.Button(town_options_window, text=make_new_district_desc,
                                             command=lambda:self.create_new_district_window(money_label, wood_label))
        make_new_district_button.grid(row=1)

    def create_new_district_window(self, money_label_var, wood_label_var):
        # Displays the window for creating a new district.
        new_district_window = tk.Toplevel()
        new_district_window.title('Create District')
        new_district_window.resizable(width=False, height=False)
        new_district_entry_label = tk.Label(new_district_window, text='District Name:')
        new_district_entry_label.grid(row=0)
        new_district_entry = tk.Entry(new_district_window)
        new_district_entry.grid(row=0, column=1)
        housing_limit_entry_label = tk.Label(new_district_window, text='Housing Limit:')
        housing_limit_entry_label.grid(row=1)
        housing_limit_entry = tk.Entry(new_district_window)
        housing_limit_entry.grid(row=1, column=1)
        create_district_button = tk.Button(new_district_window, text='Create District',
                                           command=lambda:self.create_district(new_district_entry.get(),
                                                                               housing_limit_entry.get(),
                                                                               new_district_window,
                                                                               money_label_var,
                                                                               wood_label_var))
        create_district_button.grid(row=2, column=1)

    def create_district(self, district_name, district_housing_limit, district_window, money_label, wood_label):
        if district_housing_limit.isalpha():
            messagebox.showerror('Enter a valid number!', 'Please enter a valid number!')
        else:
            housing_limit = int(district_housing_limit)
            if housing_limit > 45:
                messagebox.showerror('Too high!',' Districts can have no higher than 45 houses')
            else:
                if self.money_amt >= self.district_cost and self.wood_amt >= self.district_wood_cost:
                    new_district_obj = District(housing_limit, district_name)
                    self.district_objects.append(new_district_obj)
                    self.money_amt -= self.district_cost
                    self.wood_amt -= self.district_wood_cost
                    money_label.config(text='Money:{}'.format(self.money_amt))
                    wood_label.config(text='Wood:{}'.format(self.wood_amt))

                    messagebox.showinfo('District Created!', 'You have created a new district!')
                    print(self.district_objects)
                    district_window.destroy()
                else:
                    messagebox.showerror('Not enough funds!', 'You do not have enough funds!')
                    district_window.destroy()

    def display_buttons(self, window, wood_label_var, money_label_var, root, population_label):
        # This displays all the buttons to a window that is passed as an argument.
        harvest_wood_desc = 'Harvest Wood - Takes 2 hours - Gives {} wood!'.format(self.wood_increment_amt)
        sell_wood_desc = 'Sell Wood - 2 dollars per wood piece!'
        town_options_desc = 'Town Options'
        building_options_desc = 'Building Options'
        financial_options = 'Financial Related Options'
        harvest_wood_button = tk.Button(window, text=harvest_wood_desc,
                                        command=lambda: self.add_wood(self.wood_increment_amt, wood_label_var))
        harvest_wood_button.grid(row=4)
        sell_wood_button = tk.Button(window, text=sell_wood_desc,
                                     command=lambda: self.sell_wood(wood_label_var,
                                                                    money_label_var))
        sell_wood_button.grid(row=5)
        building_options_button = tk.Button(window, text=building_options_desc,
                                            command=lambda: self.display_building_options(window, money_label_var,
                                                                                          wood_label_var))
        building_options_button.grid(row=6)
        financial_options_button = tk.Button(window, text=financial_options,
                                             command=lambda:self.display_financial_options(window, population_label,
                                                                                           money_label_var))
        financial_options_button.grid(row=7)
        town_options_button = tk.Button(window, text=town_options_desc,
                                        command=lambda:self.display_town_options(money_label_var, wood_label_var))
        town_options_button.grid(row=8)

    def start_increment_population_thread(self, population_label, money_label):
        if self.money_amt >= self.population_increment_money_price:
            print('Upgrade purchased!')
            self.money_amt -= self.population_increment_money_price
            money_label.config(text='Money:{}'.format(self.money_amt))
            self.population_increment_level += 1
            increment_population_thread = threading.Thread(target=self.increment_population_amount,
                                                           args=(population_label,))
            increment_population_thread.start()
        else:
            print('You do not have suffiient funds!')

    def increment_population_amount(self, label_to_update):
        # Label to update refers to the population label.
        running = False
        increment_options = [1, 3, 6]
        while True:
            if running is True:
                to_increment_population_by = random.choice(increment_options)
                print(to_increment_population_by)
                if len(self.houses) == 0:
                    print('self.houses is empty!')
                    running = False
                else:
                    for item in self.houses:
                        print('House Limit: {}'.format(item.inhabitant_amount))
                        print('House Occupants: {}'.format(item.occupants))
                        print('Value: {}'.format(to_increment_population_by))
                        if item.full_house is False:
                            all_occupants = item.occupants
                            if len(all_occupants) == item.inhabitant_amount:
                                running = False
                            else:
                                if len(all_occupants) + to_increment_population_by == item.inhabitant_amount or len(all_occupants) + to_increment_population_by < item.inhabitant_amount:
                                    print('Valid!')
                                    for x in range(0, to_increment_population_by):
                                        item.add_occupant(random.choice(self.occupant_names))
                                    print(item.occupants)
                                    self.population += to_increment_population_by
                                    label_to_update.configure(text='Population: {}'.format(self.population))
                                    running = False
                                elif len(all_occupants) + to_increment_population_by > item.inhabitant_amount:
                                    print('Not allowed!')
                                    running = False
                        else:
                            running = False
            else:
                if self.population_increment_level == 1:
                    print('Before sleep statement')
                    sleep(20)
                    running = True
                elif self.population_increment_level == 2:
                    sleep(15)
                    running = True
                elif self.population_increment_level == 3:
                    sleep(10)
                    running = True
                elif self.population_increment_level == 4:
                    sleep(5)
                    running = True


    def return_player_to_main_menu(self, window_to_close, root_window):
        # Returns player to title screen
        save_prompt = messagebox.askyesno('Save?', 'Do you want to save your current progress?')
        if save_prompt is True:
            self.save_game_prompt()
        else:
            window_to_close.destroy()
            root_window.deiconify()
            # self.starting_window()

    def register_new_business_window(self, previous_window):
        previous_window.withdraw()
        make_new_business_window = tk.Toplevel()
        make_new_business_window.title('New Business')
        make_new_business_window.resizable(width=False, height=False)
        company_name_entry_label = tk.Label(make_new_business_window, text='Business Name:')
        company_name_entry_label.grid(row=0)
        company_name_entry = tk.Entry()
        company_name_entry.grid(row=0, column=1)
        employee_limit_entry_label = tk.Labe(make_new_business_window, text='Employee Limit:')
        employee_limit_entry_label.grid(row=1)
        employee_limit_entry = tk.Entry(make_new_business_window)
        employee_limit_entry.grid(row=1, column=1)

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

    def create_civilization(self, civ_name, civ_species_name, starting_year, root_window,
                            previous_win):  # Creates civilization
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

    def load_game_window(self,parent_window):
        # Reads from a file called ".playernamexample> in .saves and loads the player's progress.
        parent_window.withdraw()
        load_game_prompt = tk.Toplevel()
        load_game_prompt.resizable(width=False, height=False)
        load_game_prompt.protocol('WM_DELETE_WINDOW', lambda: self.back(load_game_prompt, parent_window))
        self.display_available_saves(load_game_prompt, parent_window)

    def display_available_saves(self, window_to_display_to, parent_window):
        # parent_window in this case would be the window from the starting_win function
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
                tk.Button(window_to_display_to, text=save_file_name,
                          command=lambda save_name=save_file_name: print(save_name)).grid(row=row_count)

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


class District: # Class for making a new district.
    def __init__(self, housing_limit, district_name):
        self.district_name = district_name
        self.housing_limit = housing_limit
        self.houses_in_district = []

    def add_home_to_district(self, house_obj):
        self.houses_in_districty.append(house_obj)

    def remove_home_from_district(self, house_obj):
        self.houses_in_district.remove(house_obj)

class HomeTemplate:
    def __init__(self, resident_limit):
        self.resident_limit = resident_limit
        self.occupants = []
        self.house_full = False

    def add_occupant(self, occupant_name):
        self.occupants.append(occupant_name)

    def remove_occupant(self, occupant_name):
        self.occupants.remove(occupant_name)


game_instance = Game()
