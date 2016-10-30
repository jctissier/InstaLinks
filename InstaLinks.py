import warnings
import webbrowser
import shelve
import requests
from bs4 import BeautifulSoup
from termcolor import cprint, colored
from lxml import html
import sys

#Get rid of warning message
warnings.filterwarnings("ignore", category=DeprecationWarning)

# This helps you remember what was the last show you were watching
def login_reminder():
    shelf_file = shelve.open('mydata')
    print(shelf_file['data'])
    last_watched['data'] = data
    last_watched.close()

#Main Menu simulation
class mainMenu():
    def __init__(self):
        self.runMenu()
        
    def runMenu(self):
        cprint("\n                TV SHOW                               MOVIE                         "
               " ",'red', attrs=['underline'])
        menu_options = colored("[1]Episode Links  [2]List of Episodes | "
                               "[3]Movie Links  [4]Movie Suggestions  [5]Exit\n",'red', attrs=['bold'])
        options = input(menu_options)
        menu_guard = ['1','2','3','4','5','6']
        while options not in menu_guard:
            options = input(menu_options)
        if options =="1":
            tvLinks()
        elif options =="2":
            tvEpisodes()
        elif options =="3":
            movieLinks()
            
