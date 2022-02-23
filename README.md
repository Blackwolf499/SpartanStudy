# SpartanStudy
SpartanStudy, is a small tool designed to monitor, track, and log your progress on TryHackMe.com
Typically it should be run as you're working on TryHackMe so you're able to study accordingly and
can see how you progress in real-time. 

![image](https://user-images.githubusercontent.com/33044535/155277641-5ed12ecd-6260-408b-aaa7-ccf8f8a6366b.png)

Current Functionality:
- Global Rank
- Top Percentile
- Rooms Completed
- Daily Ladder
- Percentile Change. 

- Count Down clock [25 minutes]
- Menu Items to Start, Pause, Restart.

SpartanStudy, a text-based application is displayed exclusively using Curses. 
Curses was a library developed for BSD UNIX. I wanted to create a tool that felt like
and resembled an "old-school" application, in which it was entirely text-based. 

It updates and logs your global positional ranking every 60 seconds by accessing an API that
TryHackMe hadn't secured properly (many of their APIs have access control enabled). 
It monitors daily increase of rank, as-well as displaying your change in global rank expressed as a percentage,
so you can see how many people you've surpassed in a days work. 

SpartanStudy was created with the idea that it should be a study-tool for TryHackMe, 
by monitoring your global rank you can see your rank improve as you're studying, 
which for competitive individuals is always a great motivator. Additionally it implements 
the Pomodoro study technique, a neuroscientifically proven method to efficently study.
This method is intended to improve memory retention as memory recall dimnishes after 20 minutes.
Your work should be broken down into 20 minute segments, followed by a 3-5 minute break.

