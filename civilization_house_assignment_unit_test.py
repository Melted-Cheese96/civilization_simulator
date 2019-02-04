import tkinter as tk
import os
import sys
from tkinter import messagebox
import threading
from time import sleep
import random 

# This is a "unit test" type thing that tests out the logic for assigning houses to newcomers 


class CivilizationTest:
    def __init__(self):
        self.current_population = 0
        self.small_houses = []
        self.medium_houses = []
        self.large_houses = []
        self.total_money_amt = 1000
        self.wood_amt = 1000
        self.stone_amt = 1000
        self.main_game_window()

    def main_game_window(self):
        window = tk.Tk()
        window.resizable(height=False, width=False)
        money_txt = 'Money:{}'.format(self.total_money_amt)
        wood_amt_txt = 'Wood:{}'.format(self.wood_amt)
        stone_amt_txt = 'Stone:{}'.format(self.stone_amt)
        money_label = tk.Label(text=money_txt)
        money_label.grid(row=0)
        stone_label = tk.Label(text=stone_amt_txt)
        stone_label.grid(row=1)
        wood_label = tk.Label(text=wood_amt_txt)
        wood_label.grid(row=2)
        population_increment = tk.Button(text='Population increment')
        # population_increment.grid(row=0)



game = CivilizationTest()
