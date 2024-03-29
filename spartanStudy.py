import time
import json 
import datetime
import requests
import threading
import concurrent.futures

# ASCII based GUI related imports
import curses
import pyfiglet
from curses import wrapper
from pyfiglet import figlet_format

""" 
Project SpartanStudy

Started: [10/2/2022]
This project was developed by BlackWolf

For additonal details read the README.md



To Do:
    - Threading
        * API calls will benefit from the use of hyper-threading
        * Need to use threading for update timer and pomo clock to run 
          concurrently, won't work without hyper-threading.

    - Need to create and implement the pomodoro study technique timer
    - Figure out how to fetch user-streak, no API for that.

    - Replace selenium webscrape using TryHackMe's APIs instead [DONE]
        * This did result in some loss in functionality
            * No API for userLevel, User-Streak
            * API for badges is weird, will need to work on it
        * user stats data can be fetched through THM's API
        * Will make time taken for script to start much shorter (Hopefully)
            * Cut down start-up time from 5s to <1s
            * Only issue is that only the skeleton and top windows display 
              immediately, the user-stats window loads after 3s

"""



####################################################
######## Change this to your own username!! ########
####################################################

# This is case sensitive
Username = "Blackwolf"
# tHiS iS cAsE sEnSiTiVe

#####################################################
#####   Data fetching component of the program  #####
#####################################################

# To do: Implement hyper-threading on the fetching of data
def rank_fetch():
    return json.loads(requests.get("https://tryhackme.com/api/user/rank/" + Username).text).get("userRank") 
def totalUsers():
    return json.loads(requests.get("https://tryhackme.com/api/site-stats").text).get("totalUsers")

def user_stats():
    user_stats = {
        "username": Username,
        "rooms":  json.loads(requests.get("https://tryhackme.com/api/no-completed-rooms-public/" + Username).text),
        "badges": json.loads(requests.get("https://tryhackme.com/api/badges/get/" + Username).text),
    }
    return user_stats

###################################
#####   Logic for the program #####
###################################
        
def rank_percentile():
    return rank_fetch() / totalUsers() * 100

# Reading score before writing (to prevent duplicates)
def last_score_stored():
    with open("score_log.csv", "r") as file:
        lines = file.read().splitlines()
        return int(list(lines[-1].split(" "))[0])

def daily_percentile():
    with open("score_log.csv", "r") as file:
        lines = file.read().splitlines()
    
        for line in lines:
            dateVal = line.split(" ")[1]
            scoreVal = line.split(" ")[0]

            if dateVal == str(datetime.date.today()):
                return int(scoreVal) / totalUsers() * 100 - rank_percentile()

def update():
    if(last_score_stored() != rank_fetch()):
        with open("score_log.csv", "a") as file:
            position_difference = last_score_stored() - rank_fetch()
            file.write(str(rank_fetch()) + " " + str(datetime.date.today()))
            file.write("\n")

# daily score increase tracker
def daily_ladder():
    daily_increase = 0
    todays_score = 0
    
    # Reading log file
    with open("score_log.csv", "r") as file:
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
                daily_increase = int(todays_score) - int(scoreVal)

   # Returning difference in score from first val of todays work
    if(daily_increase > 0):
        return "+" + str(daily_increase)
    else:
        return daily_increase

################################################################################
####    This section is for the ASCII based GUI component of the program    ####
################################################################################

##### This is the logic for the clock
def timer(clock_win):
    count = 1500
    while True:
        mins, secs = divmod(count, 60)
        clock_win.clear()
        clock_win.addstr(0, 0, pyfiglet.figlet_format(f"{mins} : {secs}", font = "small"))
        clock_win.refresh()
        count -= 1
        time.sleep(1)

def draw_frame(win):
    win.clear()
    for x in range(63):
        win.addstr(0, x, "=")
        win.addstr(2, x, "=")
        win.addstr(13, x, "=")
        win.addstr(15, x, "=")
    
    for y in range(15):
        win.addstr(y, 0, "|")
        win.addstr(y, 63, "|")
    win.refresh()

def top_text(top_win):
    top_win.clear()
    top_win.addstr(0, 1, "SpartanStudy v1.18")
    top_win.addstr(0, 40, f"Date: {datetime.date.today()}")
    top_win.refresh()

def profile(profile_win):
    profile_win.clear()
    profile_win.addstr(f"User: {user_stats().get('username')}")
    profile_win.addstr(1, 0, "-----------------------")
    profile_win.addstr(2, 0, f"Global Rank: {rank_fetch()}")
    profile_win.addstr(3, 0, f"Placed in Top {round(rank_percentile(), 2)}%")
    profile_win.addstr(4, 0, f"Rooms Completed: {user_stats().get('rooms')}")
    #profile_win.addstr(5, 0, f"Increased by {daily_percentile()}")

    for y in range(5):
        profile_win.addstr(y, 22, "|")
    profile_win.refresh()
    
def updater(win, ladder_win, profile_win):
    while True:
        x = 60
        while(x >= 0):
            win.clear()
            win.addstr(0, 0, f"Updating In: {x}")
            win.refresh()
            x -= 1
            time.sleep(1)
        update()
        ladder(ladder_win)
        profile(profile_win)
        
        win.clear()
        win.addstr(f"Updated!")
        win.refresh()
        time.sleep(4)

def ladder(win):
    win.clear()
    win.addstr(0, 0, f"Daily Ladder: {daily_ladder()}")
    win.addstr(1, 0, f"Percentile change {round(daily_percentile(), 4)}%")
    win.refresh()

def clock_options_draw(clock_menu, current_row_idx):
    clock_menu.clear()
    h, w = clock_menu.getmaxyx()
    
    options_length = 0
    for option in menu:
        options_length += len(option) +5
    
    counter = 1
    x = 7
    for idx, row in enumerate(menu):  
        clock_menu.addstr(0, 62, "|")   
        y = h//2

        if idx == current_row_idx:
            clock_menu.attron(curses.color_pair(1))
            clock_menu.addstr(0, x, f"[ {row} ]")
            clock_menu.attroff(curses.color_pair(1))
        
        else:
            clock_menu.addstr(0, x, f"[{row}]")
        counter += 1
        x += 20
        options_length -= len(row) +5

    clock_menu.refresh()


def clock_menu_keys(clock_menu, current_row_idx):
    clock_options_draw(clock_menu, current_row_idx)

    while True:
        key = clock_menu.getch()
        clock_menu.clear()

        if key == curses.KEY_RIGHT and current_row_idx < len(menu)-1:
            current_row_idx += 1

        elif key == curses.KEY_LEFT and current_row_idx > 0:
            current_row_idx -= 1

        elif key == curses.KEY_ENTER or key in [10, 13]:
            clock_menu.addstr(0, 0, f"You pressed {menu[current_row_idx]}") 
            clock_menu.refresh()
            clock_menu.getch()

        clock_options_draw(clock_menu, current_row_idx)
        clock_menu.refresh()



menu = ["Start", "Pause", "Restart"]
def main(screen):
    # Disables cursor
    curses.curs_set(0)

    # Colours
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

   # Clock Menu options
   #menu = ["Start", "Pause", "Restart"]
    current_row_idx = 0

    # Initialising windows
    ladder_win = curses.newwin(2, 30, 11, 2)
    profile_win = curses.newwin(6, 58, 3, 2)
    skeleton_frame = curses.newwin(16, 70, 0, 0)
    top_win = curses.newwin(1, 58, 1, 1)
    updating_win = curses.newwin(1, 17, 10, 2)
    pomodoro_clock = curses.newwin(6, 30, 3, 30)

    clock_menu = curses.newwin(1, 67, 14, 1)
    clock_menu.keypad(1) 
    
    draw_frame(skeleton_frame)
    top_text(top_win)

    # Hyper threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(profile, profile_win)
        executor.submit(ladder, ladder_win)
        executor.submit(timer, pomodoro_clock)
        executor.submit(updater, updating_win, ladder_win, profile_win)
        executor.submit(clock_menu_keys, clock_menu, current_row_idx)
    clock_menu_keys(clock_menu, current_row_idx)
    # Need this so program doesn't end abruptly
    #top_win.getch()
    #profile_win.getch()
    #screen.getch()
    #updating.getch()
    #clock_menu.getch()
wrapper(main)



