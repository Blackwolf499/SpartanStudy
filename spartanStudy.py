import time
import datetime

# ASCII based GUI related imports
import curses
from curses import wrapper

# Selenium related imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options





###################################################
#####   Web Scraping Component of the Program #####
###################################################

#def web_scrape():
options = Options()
options.headless = True
url = "https://tryhackme.com/p/Blackwolf"
service = Service("/home/blackwolf/scripts/python/webdrivers/geckodriver/geckodriver")
browser = webdriver.Firefox(options=options, service=service)
browser.get(url)
#    return browser

# Fetching appropriate data for logging
def rank_fetch():
    return browser.find_element(By.ID, "user-rank").text
    
def user_stats():
    #browser.refresh()
    user_stats = {
        "username": browser.find_element(By.CLASS_NAME, "level").text,
        "level": browser.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div[3]/div[1]").text,
        "rooms": browser.find_element(By.ID, "rooms-completed").text,
        "badges": browser.find_element(By.ID, "badge-count").text,
    } 
    return user_stats 


###################################
#####   Logic for the program #####
###################################


# Reading score before writing (to prevent duplicates)
def last_score_stored():
    with open("/home/blackwolf/scripts/github/StatTracker/pandas_data.csv", "r") as file:
        lines = file.read().splitlines()
        rank_saved = int(list(lines[-1].split(" "))[0])
    return int(rank_saved) 

# daily score increase tracker
def daily_ladder():
    daily_increase = 0
    todays_score = 0
    
    # Reading log file
    with open("/home/blackwolf/scripts/github/StatTracker/pandas_data.csv", "r") as file:
        lines = file.read().splitlines()
        
        # Looping over every line in log file
        for line in lines:

            # Updating date and score value every new line
            dateVal = line.split(" ")[1]
            scoreVal = line.split(" ")[0]
            
            # Checking for first appearance of current date, sets starting score val 
            if dateVal == str(datetime.date.today()) and todays_score == 0:
                todays_score = int(scoreVal)
            
            # Records difference in rank for todays date occurences
            elif dateVal == str(datetime.date.today()):
                daily_increase = todays_score - int(scoreVal)

   # Returning difference in score from first val of todays work
    if(daily_increase > 0):
        return "+" + str(daily_increase)
    else:
        return daily_increase

################################################################################
####    This section is for the ASCII based GUI component of the program    ####
################################################################################

def draw_frame(win):
    win.clear()
    for x in range(60):
        win.addstr(0, x, "=")
        win.addstr(2, x, "=")
        win.addstr(13, x, "=")
        win.addstr(15, x, "=")
    
    for y in range(15):
        win.addstr(y, 0, "|")
        win.addstr(y, 60, "|")
    win.refresh()

def top_text(top_win):
    top_win.clear()
    top_win.addstr(0, 1, f"Date: {datetime.date.today()}")
    top_win.addstr(0, 30, f"User: xxxx")
    top_win.refresh()

def profile(profile_win):
    profile_win.clear()
    profile_win.addstr(f"User: {user_stats().get('username')},  Lvl {user_stats().get('level')}")
    profile_win.addstr(1, 0, f"Rooms Completed: {user_stats().get('rooms')}")
    profile_win.addstr(2, 0, f"Badges: {user_stats().get('badges')}")
    profile_win.refresh()


def updating(win):
    x = 120
    while(x >= 0):
        win.clear()
        win.addstr(f"Updating In: {x}")
        win.refresh()
        x -= 1
        time.sleep(1)


def ladder(win):
    win.clear()
    win.addstr(f"Daily Ladder: {daily_ladder()}")
    win.refresh()

def main(screen):
    # Initialising windows
    ladder_win = curses.newwin(1, 21, 14, 39)
    profile_win = curses.newwin(5, 30, 3, 2)
    skeleton_frame = curses.newwin(16, 70, 0, 0)
    top_win = curses.newwin(1, 58, 1, 1)
    updating_win = curses.newwin(1, 17, 14, 2)

    # Calling Functions to draw frame and text, has to be top to bottom
    draw_frame(skeleton_frame)
    top_text(top_win)
    profile(profile_win)
    ladder(ladder_win)
    updating(updating_win)

    # Need this so program doesn't end abruptly
    top_win.getch()
    profile_win.getch()
    screen.getch()
    updating.getch()

wrapper(main)



