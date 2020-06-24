import requests
from bs4 import BeautifulSoup
import background
import random
from threading import Timer

past_urls = []
image_extensions = ['jpg', 'jpeg', 'png', 'bmp']


def load_settings():
    """
    Loads the settings from file to be parsed by the program.
    Settings in form of [time_sleep, stop_default_message, subreddits, sorting_of_subreddits]
    :return: array of these settings
    """
    settings = {}
    with open('settings.ini', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if '//' not in line and line != '\n':  # ignoring comments and blank lines
                setting = line.split("=")
                settings[setting[0]] = setting[1].replace("\n", "")  # getting the actual data we need
        settings["SUBREDDITS"] = settings["SUBREDDITS"].split(',')  # splitting up the subreddits into a list instead of string
        try:
            settings["TIME_SLEEP"] = float(settings["TIME_SLEEP"]) * 60
        except ValueError:
            print(f'{settings["TIME_SLEEP"]} is not a valid float.')
            return
    return settings


def try_ask_settings_msg(settings):
    if settings["SHOW_SETTINGS_MESSAGE"] == "TRUE":  # If defaults message is set to TRUE (by default), show the message
        input("Reminder to change settings.ini to desired settings. Change SHOW_SETTINGS_MESSAGE to disable this in the future (Enter to continue) ")


def get_redd_imgs(settings):
    sub = settings["SUBREDDITS"][random.randint(0, len(settings["SUBREDDITS"]) - 1)]
    url = 'https://old.reddit.com/r/' + sub.replace(' ', '') + "/"
    print("Grabbing from", sub)
    sorting = settings["SORTING"]
    if sorting == "TOP":
        url += 'top/'
    # url += '?limit=100'
    print(url)

    response = requests.get(url,
                            headers={'User-agent': 'ImaginaryEscapism'})  # Required to be allowed to get reddit data
    html_soup = BeautifulSoup(response.text, 'lxml')
    containers = html_soup.find_all('div', class_="expando expando-uninitialized")

    bgs = []

    for k in containers:  # Actually getting the url out of the container selected
        k = str(k).split(" ")
        for a in k:
            if 'href' in a:
                a = a[6:-1]
                if a.split('.')[-1] in image_extensions:
                    bg = background.Background(a, sub)
                    bgs.append(bg)
    return bgs


def find_background(bgs):
    if len(bgs) <= 0:
        print("Could not find a background.")
        return False
    choice = bgs[random.randint(0, len(bgs) - 1)]
    choice.get_image_from_url()
    if choice.is_image_duped(past_urls) or choice.is_ratio_invalid():
        find_background(bgs)
    choice.save_image_to_file()
    past_urls.append(choice.site_url)
    return choice


def loop(loop_time_s):
    print('\nLooping\n')
    backgrounds = get_redd_imgs(settings)
    chosen_bg = find_background(backgrounds)
    b_changed = chosen_bg.change_background()
    if not b_changed:
        print("Could not change background. Trying again.")
        loop(loop_time_s)
    # We want to be able to cancel this loop at any time from here by pressing enter (skip) or F (favourite)
    t = Timer(loop_time_s, loop, [loop_time_s])
    t.start()
    prompt = "You have %d seconds to input an option (anything for skip, 'f' for favourite)...\n" % loop_time_s
    answer = input(prompt)
    t.cancel()
    if answer.lower() == 's':
        print('Skipping\n')
        loop(loop_time_s)
    elif answer.lower() == 'f':
        print('Favouriting')
        chosen_bg.add_favourite()
    print('Looping again\n')
    loop(loop_time_s)


if __name__ == '__main__':
    settings = load_settings()
    try_ask_settings_msg(settings)
    loop(settings["TIME_SLEEP"])


# figure out why its being slow/freezing here and there