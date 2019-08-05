import time
import image_fetcher
import bg_changer
from selenium import webdriver

past_images = []


def load_defaults():
    defaults_ret = []
    with open('defaults.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if '//' not in line and line != '\n':
                defaults_ret.append(line.split("=")[1].replace("\n", ""))
        defaults_ret[2] = defaults_ret[2].split(',')
    return defaults_ret


def cycle(sleep_time_str):
    past_image = image_fetcher.fetch_image(defaults[2], defaults[3], past_images)
    past_images.append(past_image)
    bg_changer.change_bg()
    sleep_time = int(sleep_time_str)*60
    time.sleep(sleep_time)  # Sleeping for sleep_time seconds


defaults = load_defaults()
# print(defaults)
if defaults[1] == "TRUE":
    use_def = input("Change the settings in default.txt. To not see this message again press y, otherwise press enter: ").lower()
    if use_def == 'y':
        with open('defaults.txt', 'rw') as f:
            lines = f.readlines()
            lines = lines[3].replace('STOP_DEFAULTS_MESSAGE=FALSE', 'STOP_DEFAULTS_MESSAGE=TRUE')
            f.write(lines)

while True:
    cycle(defaults[0])
