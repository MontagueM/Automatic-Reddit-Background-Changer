from requests import get
from bs4 import BeautifulSoup
import random
import os
from PIL import Image
import requests
from io import BytesIO


def fetch_image(subreddits, sorting, past_images):
    """
    This module essentially uses beautiful soup and requests to get the HTML data from reddit and finds the image
    link directly. There is a lot of data management and reconstruction which is most of the work.
    Returns the image url as string literal.
    """

    # Choosing the subreddit and loading the page
    sub = subreddits[random.randint(0, len(subreddits) - 1)].lower()  # randomly selecting a subreddit
    url = 'https://old.reddit.com/r/' + sub + "/"
    print("Grabbing from", sub)
    if sorting == "TOP":
        url += 'top/?t=all/'
    url += '?limit=100'

    response = get(url, headers={'User-agent': 'ImaginaryEscapism'})  # Required to be allowed to get reddit data
    html_soup = BeautifulSoup(response.text, 'lxml')

    # Getting all the URLs on the page
    split = str(html_soup).split(',')
    containers = html_soup.find_all('a', class_='thumbnail invisible-when-pinned may-blank outbound')
    urls = []

    for k in containers:  # Actually getting the url out of the container selected
        k = str(k).split(" ")
        for a in range(0, len(k), 2):
            a = k[a]
            if 'href' in a:
                # print(a[15:-1])
                urls.append(a[15:-1])

    for i in split:  # Making sure the selected url is an image
        if '"content":"' in i and 'preview':
            if 'jpg' in i or 'png' in i or 'bmp' in i:
                i = i.split('"')
                urls.append(i[3])

    print(len(urls), "urls found")
    trigger_load = True  # This variable ensures that we don't load multiple images over each other
    if len(urls) > 5:  # If it's less than 5 a loading issue probably occurred so will wait to try again
        while trigger_load is True:
            try:
                ranin = random.randint(0, len(urls)-1)
                # print(ranin)
                image_url = urls[ranin]  # Selecting the image
            except ValueError:
                try:
                    image_url = urls[0]
                except IndexError:
                    image_url = past_images[random.randint(0, len(past_images)-1)]
            if image_url not in past_images:  # If we've selected a new image, continue with loading
                trigger_load = False
                print("Image not repeated.")
            else:
                print("Image repeated.")
        print("Image url:", image_url)
        response_img = requests.get(image_url)  # Getting image
        try:
            '''
            This code block checks to see if the image is longer width than height as we want desktop landscape
            backgrounds instead of phone vertical ones. This mostly removes the issue with strange aspect ratios
            but I don't mind them personally (and most aren't 16:9 anyway)
            '''
            img = Image.open(BytesIO(response_img.content))
            img.save(os.getcwd() + "/background.png")
            width, height = img.size
            # if width != "1280" and width != "1920" and width != "2560" and width != "3840":
            #     print("Image not within aspect ratio of 16:9. Skipping.")
            if height > width:
                print("Aspect ratio wrong way round. Skipping.")
                fetch_image(subreddits, sorting, past_images)  # Trying again
        except OSError:
            print("Error in parsing image. Likely image is corrupt. Skipping.")
            fetch_image(subreddits, sorting, past_images)  # Unsure why this occurs, possibly bad url or old image.
        print("Saved new image")
        return image_url
    else:
        return ""
