from requests import get
from bs4 import BeautifulSoup
import random
import os
from PIL import Image
import requests
from io import BytesIO


def fetch_image(subreddits, sorting, past_images):
    used = True
    # print(sorting)
    sub = subreddits[random.randint(0, len(subreddits) - 1)].lower()
    url = 'https://old.reddit.com/r/' + sub + "/"
    print("Grabbing from", sub)
    if sorting == "TOP":
        url += 'top/?t=all/'
    url += '?limit=100'
    # print(url)
    response = get(url, headers={'User-agent': 'ImaginaryEscapism'})
    html_soup = BeautifulSoup(response.text, 'lxml')

    split = str(html_soup).split(',')
    containers = html_soup.find_all('a', class_='thumbnail invisible-when-pinned may-blank outbound')
    urls = []

    for k in containers:
        k = str(k).split(" ")
        for a in range(0, len(k), 2):
            a = k[a]
            if 'href' in a:
                # print(a[15:-1])
                urls.append(a[15:-1])

    for i in split:
        if '"content":"' in i and 'preview':
            if 'jpg' in i or 'png' in i or 'bmp' in i:
                i = i.split('"')
                urls.append(i[3])
    # print(urls)
    print(len(urls), "urls found")
    if len(urls) > 5:
        while used is True:
            try:
                ranin = random.randint(0, len(urls)-1)
                # print(ranin)
                image_url = urls[ranin]
            except ValueError:
                try:
                    image_url = urls[0]
                except IndexError:
                    image_url = past_images[random.randint(0, len(past_images)-1)]
            if image_url not in past_images:
                used = False
                print("Image not repeated.")
            else:
                print("Image repeated.")
        print("Image url:", image_url)
        response_img = requests.get(image_url)
        try:
            img = Image.open(BytesIO(response_img.content))
            img.save(os.getcwd() + "/background.png")
        except OSError:
            print("Error in parsing image. Likely image is corrupt. Skipping.")
            fetch_image(subreddits, sorting, past_images)
        print("Saved new image")
        return image_url
    else:
        return ""
