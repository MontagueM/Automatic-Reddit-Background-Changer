import time
import image_fetcher
import bg_changer

past_images = []


def load_defaults():
    """
    Loads the defaults from file to be parsed by the program.
    Defaults in form of [time_sleep, stop_default_message, subreddits, sorting_of_subreddits]
    Returns the default settings in an array
    """
    defaults_ret = []
    with open('defaults.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if '//' not in line and line != '\n':  # ignoring comments and blank lines
                defaults_ret.append(line.split("=")[1].replace("\n", ""))  # getting the actual data we need
        defaults_ret[2] = defaults_ret[2].split(',')  # splitting up the subreddits into a list instead of string
    return defaults_ret


def cycle(sleep_time_str):
    """
    This function is the main script that is iterated upon forever until the program is closed.
    """
    past_image = image_fetcher.fetch_image(defaults[2], defaults[3], past_images)  # Gets image from reddit
    past_images.append(past_image)  # Ensuring that we don't get duplicate images
    bg_changer.change_bg()  # Changes background
    sleep_time = int(sleep_time_str)*60  # Delay turned from mins to seconds

    time.sleep(sleep_time)  # Sleeping for sleep_time seconds


defaults = load_defaults()

if defaults[1] == "TRUE":  # If defaults message is set to TRUE (by default), show the message
    use_def = input("Change the settings in default.txt. To not see this message again press y, otherwise press enter: ").lower()
    if use_def == 'y':
        with open('defaults.txt', 'rw') as f:
            lines = f.readlines()
            lines = lines[3].replace('STOP_DEFAULTS_MESSAGE=FALSE', 'STOP_DEFAULTS_MESSAGE=TRUE')
            f.write(lines)

while True:
    cycle(defaults[0])
