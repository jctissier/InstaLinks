import warnings
import webbrowser

import requests
from bs4 import BeautifulSoup
from termcolor import cprint, colored
from lxml import html

# Get rid of warning message
warnings.filterwarnings("ignore", category=DeprecationWarning)


#Main Menu simulation
class mainMenu():
    def __init__(self):
        self.runMenu()

    def runMenu(self):
        cprint("\n                TV SHOW                               MOVIE                "
               " ", 'red', attrs=['underline'])
        menu_options = colored("[1]Episode Links  [2]List of Episodes | "
                               "[3]Movie Links  [4]Movie Suggestions\n", 'red', attrs=['bold'])
        options = input(menu_options)
        menu_guard = ['1', '2', '3', '4']
        while options not in menu_guard:
            options = input(menu_options)
        if options == "1":
            tvLinks()
        elif options == "2":
            tvEpisodes()
        elif options == "3":
            movieLinks()
        elif options == "4":
            movieSuggestion()


# Displays lists of episodes for a tv show
class tvEpisodes():
    epguides = "http://epguides.com/"

    def __init__(self):
        self.findEpisodes()

    def listMenu(self):
        new_list = input(colored("[1]Episode Links  [2]List of Episodes  [3]Main Menu\n", 'red', attrs=['bold']))
        list_guard = ['1','2','3']
        while new_list not in list_guard:
            new_list = input(new_list)
        if new_list == "1":
            tvLinks()
        elif new_list == "2":
            tvEpisodes()
        elif new_list == "3":
            mainMenu()

    # method called when user enter a show name, displays all the aired episodes
    def episodeList(self, show):
        trimming = show.replace(":", "").replace(" ", "").replace("(","").replace(")","").replace("_","")[7:] + "/"
        full_link = tvEpisodes.epguides + trimming
        r = requests.get(full_link)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("div", {"id": "eplist"})
        if len(g_data) == 0:
            cprint("Couldn't retrieve episodes for this show...",'yellow',attrs=['bold'])
        for link in g_data:
            if len(link.text) > 0:
                print(link.text[:-5])

    # Find list of episodes for a TV Show
    def findEpisodes(self):
        show = input(colored("Name of the show?\n",'red',attrs=['bold']))
        show = "tvguard" + show
        tvEpisodes.episodeList(self, show)
        tvEpisodes.listMenu(self)


#Searches for the name of a tv show
class tvSearch():
    pre_search = 'http://watchtvlinks.sx/TVshows/'

    def __init__(self):
        self.nameSearch2()

    def nameSearch(self,show):
        full_link = tvSearch.pre_search + show.replace(" ", "%20") + "-page-1"
        r = requests.get(full_link)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("div", {"class": "results-heading"})
        #Relaunch search if TV Show is not found
        if len(g_data) < 1:
            cprint("'" + show + "' was not found, please enter the name of a TV Show", 'yellow')
            tvSearch.nameSearch2(self)
        page = requests.get(full_link)
        tree = html.fromstring(page.content)
        #Prints RELEASED YEAR for each TV Show that the search returns
        try:
            for x in range(20):
                for name in g_data[x]:
                    cprint(("[" + str(x + 1) + "] ") + name.text, 'red', attrs=['bold'])
                    if x == 0:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[6]/div[4]/span[2]//text()')))
                    elif x == 1:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[8]/div[4]/span[2]//text()')))
                    elif x == 2:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[10]/div[4]/span[2]//text()')))
                    elif x == 3:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[12]/div[4]/span[2]//text()')))
                    elif x == 4:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[14]/div[4]/span[2]//text()')))
                    elif x == 5:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[16]/div[4]/span[2]//text()')))
                    elif x == 6:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[18]/div[4]/span[2]//text()')))
                    elif x == 7:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[20]/div[4]/span[2]//text()')))
                    elif x == 8:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[22]/div[4]/span[2]//text()')))
                    elif x == 9:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[24]/div[4]/span[2]//text()')))
                    elif x == 10:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[26]/div[4]/span[2]//text()')))
                    elif x == 11:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[28]/div[4]/span[2]//text()')))
                    elif x == 12:
                        print("RELEASED: " + "".join(tree.xpath('//*[@id="section"]/div[30]/div[4]/span[2]//text()')))
        except IndexError:
            number = input(colored("\nEnter your TV Show's number, [N]New Search:\n", 'red', attrs=['bold']))
            while not(number.isdigit()) or (int(number) > 12) or (int(number) == 0) or (int(number) > len(g_data)):
                if number.lower() == "n":
                    tvSearch.nameSearch2(self)
                    break
                number = input(colored("\nEnter your TV Show's number, [N]New Search:\n",'red', attrs=['bold']))
        try:
            for name in g_data[int(number) - 1]:
                show_link = name.get('href')
                tvEpisodes.episodeList(self, show_link)
                tvLinks.pickEpisode(self, show_link, show)
        except IndexError:
            pass

    def nameSearch2(self):
        # Pick Show Name
        show_input = colored(
            "\nWhat TV Show would you like to watch?\n", 'red', attrs=['bold'])
        show = input(show_input)
        tvSearch.nameSearch(self, show)


#Opens 2 links in browser and prints other links
class tvLinks():
    #Constant links
    pre_link = 'http://watchtvlinks.sx/episode'

    def __init__(self):
        self.episodeLink()

    def episodeLink(self):
        tvSearch.nameSearch2(self)

    def pickEpisode(self, show_link, show):
        # Pick season number
        season = input(colored("What season?\n", 'red', attrs=['bold']))
        while not (season.isdigit()) or (int(season) > 50):
            season = input(colored("What season? Please enter a number:\n", 'red', attrs=['bold']))
        # Pick episode number
        episode = input(colored("what episode?\n", 'red', attrs=['bold']))
        while not (episode.isdigit()) or (int(episode) > 50):
            episode = input(colored("what episode? Please enter a number:\n", 'red', attrs=['bold']))
        tvLinks.fullLink(self, season, episode, show_link, show)

    def fullLink(self, season, episode, show_link, show):
        full_link = tvLinks.pre_link + show_link[6:] + "_s" + season + "_e" + episode
        r = requests.get(full_link)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("td", {"class": "video-title"})
        tvLinks.openLinks(self, g_data)
        tvLinks.printLinks1(self, show, full_link)
        tvLinks.printLinks2(self, show, season, episode)

    def openLinks(self, g_data):
        # Opens show link for vidzi.tv
        for item in g_data:
            if "vidzi.tv" in item.find_all("a", {"class": "hostLink p2"})[0].text:
                link = ("".join(map(str, item.find_all())))[29:43]
                r = requests.get("http://watchtvlinks.sx" + link)
                soup2 = BeautifulSoup(r.content, "lxml")
                for link in soup2.find_all("a"):
                    if "vidzi" in link.get("href"):
                        vidzi = ("%s" % (link.get("href")))
                        webbrowser.open_new(vidzi)
                        print(vidzi)
                        break
                break
        # Opens show link for watchvideo.us
        for item in g_data:
            if "watchvideo.us" in item.find_all("a", {"class": "hostLink p2"})[0].text:
                link = ("".join(map(str, item.find_all())))[29:43]
                r = requests.get("http://watchtvlinks.sx" + link)
                soup2 = BeautifulSoup(r.content, "lxml")
                for link in soup2.find_all("a"):
                    if "watchvideo" in link.get("href"):
                        watchvideo = ("%s" % (link.get("href")))
                        webbrowser.open_new(watchvideo)
                        print(watchvideo)
                        break
                break

    # prints extra links from watchtvlinks.sx
    def printLinks1(self, show, full_link):
        r = requests.get(full_link)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("td", {"class": "video-title"})

        # Prints extra link for vodlocker.com
        for item in g_data:
            if "vodlocker.com" in item.find_all("a", {"class": "hostLink p2"})[0].text:
                link = ("".join(map(str, item.find_all())))[29:43]
                r = requests.get("http://watchtvlinks.sx" + link)
                soup2 = BeautifulSoup(r.content, "lxml")
                for link in soup2.find_all("a"):
                    if "vodlocker" in link.get("href"):
                        vodlocker = ("%s" % (link.get("href")))
                        print(vodlocker)
                        break
                break
        # Prints extra link for vidbull.com
        for item in g_data:
            if "vidbull.com" in item.find_all("a", {"class": "hostLink p2"})[0].text:
                link = ("".join(map(str, item.find_all())))[29:43]
                r = requests.get("http://watchtvlinks.sx" + link)
                soup2 = BeautifulSoup(r.content, "lxml")
                for link in soup2.find_all("a"):
                    if "vidbull" in link.get("href"):
                        vidbull = ("%s" % (link.get("href")))
                        print(vidbull)
                        break
                break
        # Prints extra link for openload.io
        for item in g_data:
            if "openload.io" in item.find_all("a", {"class": "hostLink p2"})[0].text:
                link = ("".join(map(str, item.find_all())))[29:43]
                r = requests.get("http://watchtvlinks.sx" + link)
                soup2 = BeautifulSoup(r.content, "lxml")
                for link in soup2.find_all("a"):
                    if "openload" in link.get("href"):
                        openload = ("%s" % (link.get("href")))
                        print(openload)
                        break
                break
        # Prints extra links for streamin.to
        for item in g_data:
            if "streamin.to" in item.find_all("a", {"class": "hostLink p2"})[0].text:
                link = ("".join(map(str, item.find_all())))[29:43]
                r = requests.get("http://watchtvlinks.sx" + link)
                soup2 = BeautifulSoup(r.content, "lxml")
                for link in soup2.find_all("a"):
                    if "streamin" in link.get("href"):
                        streamin = ("%s" % (link.get("href")))
                        print(streamin)
                        break
                break
        # Prints extra links for vidto.me
        for item in g_data:
            if "vidto.me" in item.find_all("a", {"class": "hostLink p2"})[0].text:
                link = ("".join(map(str, item.find_all())))[29:43]
                r = requests.get("http://watchtvlinks.sx" + link)
                soup2 = BeautifulSoup(r.content, "lxml")
                for link in soup2.find_all("a"):
                    if "vidto" in link.get("href"):
                        vidto = ("%s" % (link.get("href")))
                        print(vidto)
                        break
                break

    # Prints a second list of links scraped from watchseries.ac
    def printLinks2(self, show, season, episode):
        # Building customized link
        print_link = "http://www.watchseries.ac"
        pre_link = 'http://www.watchseries.ac/episode/'
        full_link = pre_link + show.replace(" ", "_") + "_s" + season + "_e" + episode + ".html"
        r = requests.get(full_link)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("a")
        # vidbull.com - close one add and click play
        for link in g_data:
            if "link/vidzi.tv" in link.get("href"):
                print(print_link + "".join(map(str, ("%s%s" % (link.get("href"), link.text[:-21])))))
                break
        # vidbull.com - close one add and click play
        for link in g_data:
            if "link/filehoot.com" in link.get("href"):
                print(print_link + "".join(map(str, ("%s%s" % (link.get("href"), link.text[:-21])))))
                break
        # vidbull.com - close one add and click play
        for link in g_data:
            if "link/vidto.me" in link.get("href"):
                print(print_link + "".join(map(str, ("%s%s" % (link.get("href"), link.text[:-21])))))
                break
        # idowatch.net - close one add and click play
        for link in g_data:
            if "link/idowatch.net" in link.get("href"):
                print(print_link + "".join(map(str, ("%s%s" % (link.get("href"), link.text[:-21])))))
                break
        # allvid.ch if available
        for link in g_data:
            if "link/allvid.ch" in link.get("href"):
                new_link = print_link+"".join(map(str, ("%s%s" % (link.get("href"), link.text[:-21]))))
                r = requests.get(new_link)
                soup = BeautifulSoup(r.content, "lxml")
                g_data2 = soup.find_all("a")
                for link in g_data2:
                    if "http://allvid" in link.get("href"):
                        print(("%s" % (link.get("href"))))
                        break
                break
        # vidbull.com
        for link in g_data:
            if "link/vidbull.com" in link.get("href"):
                print("http://www.watchseries.ac" + "".join(map(str, ("%s%s" % (link.get("href"), link.text[:-21])))))
                break
        # vodlocker.com
        for link in g_data:
            if "link/vodlocker.com" in link.get("href"):
                print(print_link + "".join(map(str, ("%s%s" % (link.get("href"), link.text[:-21])))))
                break
        # allmyvideos.net
        for link in g_data:
            if "link/allmyvideos.net" in link.get("href"):
                print(print_link + "".join(map(str, ("%s%s" % (link.get("href"), link.text[:-21])))))
                break
        # vidspot.net
        for link in g_data:
            if "link/vidspot.net" in link.get("href"):
                print(print_link + "".join(map(str, ("%s%s" % (link.get("href"), link.text[:-21])))))
                break
        # novamov.com
        for link in g_data:
            if "link/novamov.com" in link.get("href"):
                print(print_link + "".join(map(str, ("%s%s" % (link.get("href"), link.text[:-21])))))
                break
        # Restart program
        mainMenu()


# Movie Suggestions
class movieSuggestion():
    year = "https://www.rottentomatoes.com/top/bestofrt/?year="
    genre = "https://www.rottentomatoes.com/top/bestofrt/top_100_"

    def __init__(self):
        self.pickSuggestion()

    def pickSuggestion(self):
        pick = input(colored("Best movies by: [1]Year  [2]Genre\n",'red',attrs=['bold']))
        pick_guard = ['1','2']
        while pick not in pick_guard:
            movieSuggestion.pickSuggestion(self)
        if pick == "1":
            movieSuggestion.movieListbyYear(self)
        elif pick =="2":
            movieSuggestion.movieListbyGenre(self)

    # best movies by year
    def movieListbyYear(self):
        show = input("What year?\n")
        while ((not show.isdigit()) or (int(show) < 1980) or (int(show) > 2020)):
            show = input("Pick a year, ex: '2016','2006'\n")
        full_link = movieSuggestion.year + show
        r = requests.get(full_link)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("tr", {"itemprop": "itemListElement"})
        for link in g_data:
            print(link.text[0:-4])
        mainMenu()

    # best movies by genre
    def movieListbyGenre(self):
        pre_link2 = "_movies/"
        genre = input(colored("What genre?\n"
                              "[1]Action & Adventure  [2]Animation  "
                              "[3]Comedy  [4]Horror\n",'red',attrs=['bold']))
        genres = ["1", "2", "3", "4"]
        while genre not in genres:
            genre = input(colored("What genre?\n[1]Action & Adventure  "
                                  "[2]Animation  [3]Comedy  [4]Horror\n",
                                  'red',attrs=['bold']))
        if genre == "1":
            genre = "action__adventure"
        elif genre == "2":
            genre = "animation"
        elif genre == "3":
            genre = "comedy"
        elif genre == "4":
            genre = "horror"
        full_link = movieSuggestion.genre + genre + pre_link2
        r = requests.get(full_link)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("tr", {"itemprop": "itemListElement"})
        for link in g_data:
            print(link.text[0:-4])
        mainMenu()


# Movie Suggestions
class movieLinks():
    # Constant Links
    movies_search = "http://123movies.to/movie/search/"
    movies_search2 = "watching.html"
    putlocker1 = "https://putlocker.is/search/advanced_search.php?section=1&q="
    putlocker2 = "&director=&actor=&year_from=Year&year_to=Year&genre%5B%5D=All"
    movienight = 'http://movienight.ws/?s='
    movietube = 'http://movietube.ms/?s='

    def __init__(self):
        self.runStreams()

    def runStreams(self):
        self.bestStreams()
        mainMenu()

    def bestStreams(self):
        movie = input(colored("What movie do you want to watch?\n",'red',attrs=['bold']))
        while (len(movie) < 3) or (len(movie) > 50) is True:
            movie = input("Please be more specific, write a word in the title:\n")
        # Building customized link
        cprint("Searching for links...\n",'yellow')
        full_link = movieLinks.movies_search + movie.replace(" ", "+")
        r = requests.get(full_link)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("a")
        # Stream movie from 123movies.to
        for link in g_data:
            movie_link = ("%s" % (link.get("href"))) + movieLinks.movies_search2
            movie_title = ("%s" % (link.text))
            if "film" in movie_link:
                trimmed = movie_title.strip().replace("\n", " ").split(" ", 1)
                if "-season-" not in movie_link:
                    print(colored(trimmed[1][1:],'red') + "\nQuality: " + trimmed[0])
                    cprint("Link: " + movie_link, 'blue')
        # Gets the links from the other websites
        movieLinks.streamPutlocker(self, movie)
        movieLinks.streamMovienight(self, movie)
        movieLinks.streamMovietube(self, movie)

    # Putlocker Search
    def streamPutlocker(self, movie):
        full_link = movieLinks.putlocker1 + movie.replace(" ", "+") + movieLinks.putlocker2
        r = requests.get(full_link)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("img")
        movie = movie.replace(" ", "-")
        for link in g_data:
            movie_link = ("%s" % (link.get("src")))
            movie_title = ("%s" % (link.get("alt")))
            if movie in movie_link:
                first = 'http://putlocker.is/watch-'
                mid = movie_link[42:-26]
                ending = '-online-free-putlocker.html'
                full_link = first + mid + ending
                r = requests.get(full_link)
                soup = BeautifulSoup(r.content, "lxml")
                g_data = soup.find_all("td", {"style": "padding-left:5px;"})
                for link in g_data[0:1]:
                    cprint(movie_title,'red')
                    print("Quality: HD   IMDB:", link.text[13:19])
                    cprint(("Link: " + full_link), 'blue')

    # Link search for movienight.ws
    def streamMovienight(self, movie):
        full_link = movieLinks.movienight + movie.replace("-", "+")
        r = requests.get(full_link)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("a")
        movie = movie.replace(" ", "-")
        for link in g_data:
            movie_link = ("%s" % (link.get("href")))
            if movie in movie_link:
                cprint(movie_link[21:-1].replace("-", " ").title(),'red')
                print("Quality: HD")
                cprint("Link: " + movie_link,'blue')

    # Link search for movietube.ms
    def streamMovietube(self, movie):
        full_link2 = movieLinks.movietube + movie.replace("-", "+")
        r = requests.get(full_link2)
        soup = BeautifulSoup(r.content, "lxml")
        g_data = soup.find_all("a")
        movie = movie.replace(" ", "-")
        for link in g_data:
            movie_link = ("%s" % (link.get("href")))
            if movie in movie_link:
                cprint(movie_link[20:-15].replace("-", " ").title(),'red')
                print("Quality: HD")
                cprint("Link: " + movie_link, 'blue')


# Run these methods
if __name__ == "__main__":
    run = mainMenu()

