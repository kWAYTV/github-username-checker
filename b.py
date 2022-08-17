import requests, os, threading, random, time, sys
from colorama import Fore, Back, Style
from pystyle import Colors, Colorate, Center

clear = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear") # Don't touch this
# create check.txt if it doesn't exist, if it does, read and split lines into users list
if not os.path.exists("check.txt"):
    with open("check.txt", "w") as f:
        f.write("")
else:
    with open("check.txt", "r") as f:
        users = f.read().splitlines()

count = 0
free = 0
taken = 0
ratelimited = 0
error = 0
proxyDebug = False
os.system(f"title GithubUsername Checker - Starting...")
clear()


# Vanity Generator Logo
logo = """
░██████╗░██╗████████╗██╗░░██╗██╗░░░██╗██████╗░  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗██████╗░
██╔════╝░██║╚══██╔══╝██║░░██║██║░░░██║██╔══██╗  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔══██╗
██║░░██╗░██║░░░██║░░░███████║██║░░░██║██████╦╝  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░██████╔╝
██║░░╚██╗██║░░░██║░░░██╔══██║██║░░░██║██╔══██╗  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══██╗
╚██████╔╝██║░░░██║░░░██║░░██║╚██████╔╝██████╦╝  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗██║░░██║
░╚═════╝░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░╚═════╝░╚═════╝░  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝"""

def printLogo():
        print(Center.XCenter(Colorate.Horizontal(Colors.white_to_green, logo, 1)))

def check():
    global count, free, taken, ratelimited, error
    session = requests.Session()
    while True:
        for line in users: 
            if len(line) < 3:
                print(f"{Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}] {Fore.RED}{line}{Fore.RESET} is too short! Skipping...")
                continue
            proxy = random.choice(open("proxies.txt","r").read().splitlines()); proxyDict = {"http": f"http://{proxy}"}
            if proxyDebug == True:
                print(f"{Fore.MAGENTA}[{Fore.RESET}!{Fore.MAGENTA}] {Fore.RESET}Using proxy: {Fore.MAGENTA}{proxyDict}{Fore.RESET}")
            else:
                pass
            r = session.get(f'https://www.github.com/{line}')
            count += 1
            if r.status_code == 200:
                print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}] {Fore.RESET}Taken: {Fore.RED}" + line + f"{Fore.RESET}")
                with open ("taken.txt", "a") as f:
                    f.write(line + "\n")
                    taken += 1
            elif r.status_code == 404:
                print(f"{Fore.GREEN}[{Fore.RESET}-{Fore.GREEN}] {Fore.RESET}Free: {Fore.GREEN}"+ line + f"{Fore.RESET}")
                with open ("free.txt", "a") as f:
                    f.write(line + "\n")
                    free += 1
            elif r.status_code == 429:
                print(f"{Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}] {Fore.RESET}Ratelimited: {Fore.YELLOW}" + line + f"{Fore.RESET}. Sleeping for {Fore.RED}30{Fore.RESET} seconds...")
                with open ("ratelimited.txt", "a") as f:
                    f.write(line + "\n")
                    ratelimited += 1
                for i in range(30,0,-1):
                    sys.stdout.write(str(i)+' ')
                    sys.stdout.flush()
                    time.sleep(1)
                print(f"\n{Fore.GREEN}[{Fore.RESET}!{Fore.GREEN}] {Fore.RESET}Continuing{Fore.GREEN}!{Fore.RESET}")
                continue
            else:
                print(f"{Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}] {Fore.RESET}Error: {Fore.RED}" + line + f"{Fore.RESET}")
                with open ("error.txt", "a") as f:
                    f.write(line + "\n")
                    error += 1
            os.system(f"title Github Username Checker - Status: {count}/{len(users)} - Free: {free} - Taken: {taken} - Ratelimited: {ratelimited} - Error: {error}")


clear()
printLogo()
if os.stat("check.txt").st_size == 0:
    clear()
    print(f"{Fore.YELLOW}[{Fore.RESET}!{Fore.YELLOW}] {Fore.RESET}No usernames in check.txt! Exiting...")
    os.system(f"title Github Username Checker - check.txt is empty! Exiting...")
    time.sleep(1)
    sys.exit()
print(f"{Fore.MAGENTA}[{Fore.RESET}!{Fore.MAGENTA}] {Fore.RESET}Found {Fore.YELLOW}{len(users)}{Fore.RESET} accounts to check.")
try:
    while True:
        check()
except KeyboardInterrupt:
    clear()
    print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}] {Fore.RESET}Exiting. If it keeps, just close the program.")
    os.system(f"title GithubUsername Checker - Exiting. If it keeps, just close the program.")
    time.sleep(1)
    exit()