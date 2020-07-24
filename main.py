import background
import random
from threading import Timer
import praw
import prawcore.exceptions

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
    print("Grabbing from", sub)

    bgs = []
    reddit = praw.Reddit(client_id="R1QneAltTJA0aw",
                         client_secret="qn4uzfRkFkTgRB0SOk7oMYQRS9E",
                         user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")
    try:
        for submission in reddit.subreddit(sub).top(time_filter='all'):
            if submission:
                bg = background.Background(submission.url, sub)
                bgs.append(bg)
    except prawcore.exceptions.ResponseException:
        print("401 HTTP Timeout. Trying again.")
        get_redd_imgs(settings)
    return bgs


def find_background(bgs):
    if len(bgs) <= 0:
        print("Could not find a background.")
        return None
    choice = bgs[random.randint(0, len(bgs) - 1)]
    b_grabbed_image = choice.get_image_from_url()
    recursive_count = 0
    if choice.is_image_duped(past_urls) or choice.is_ratio_invalid() or not b_grabbed_image:
        if recursive_count > 5:
            return None
        recursive_count += 1
        find_background(bgs)
    choice.save_image_to_file()
    past_urls.append(choice.site_url)
    return choice


def loop(loop_time_s):
    print('\nLooping\n')
    backgrounds = get_redd_imgs(settings)
    chosen_bg = find_background(backgrounds)
    if not chosen_bg:
        print('Could not find background. Trying again.')
        loop(loop_time_s)
    b_changed = chosen_bg.change_background()
    if not b_changed:
        print("Could not change background. Trying again.")
        loop(loop_time_s)
    # We want to be able to cancel this loop at any time from here by pressing enter (skip) or F (favourite)
    t = Timer(loop_time_s, loop, [loop_time_s])
    t.start()
    prompt = "You have %d minute(s) to input an option (anything for skip, 'f' for favourite)...\n" % int(loop_time_s / 60)
    answer = input(prompt)
    t.cancel()
    if answer.lower() == 's':
        print('Skipping\n')
        loop(loop_time_s)
    elif answer.lower() == 'f':
        print('Favouriting')
        chosen_bg.add_favourite()
    loop(loop_time_s)


if __name__ == '__main__':
    settings = load_settings()
    try_ask_settings_msg(settings)
    loop(settings["TIME_SLEEP"])


# figure out why its being slow/freezing here and there
