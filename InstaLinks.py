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
