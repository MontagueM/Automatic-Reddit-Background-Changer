import requests
from PIL import Image
from io import BytesIO
import ctypes
import os

"""
New design:
- new backgrounds can be automatically loaded in with a specified time
- can press enter to grab a new image immediately
- can press F to favourite the image and save a copy, adding to a hash map or something
- does not crash with vpn or internet loss
- deals better with weird image sizes and ratios
- GUI???
- class for background
- artstation???
"""


class Background:
    def __init__(self, site_url, subreddit_origin):
        """
        :param site_url: the url of the background online
        :param subreddit_origin: the subreddit the image came from
        """
        self.site_url = site_url
        self.dimensions = []
        self.subreddit_origin = subreddit_origin
        self.image_content = None
        self.image_file_path = ""

    def pull_image_from_url(self):
        """
        :return: the image content of the background
        """
        response = requests.get(self.site_url)
        if response.status_code != 200:
            return False

        try:
            self.image_content = Image.open(BytesIO(response.content))
        except IOError:
            return False
        return True

    def save_image_to_file(self):
        """
        Once we know we have the right image to set to the background we can save it to change bg.
        :return: the OS file path of the image
        """
        # We can't set this url to be constant as favourite images do not use this url
        self.image_file_path = os.getcwd() + "/background.png"
        self.image_content.save(self.image_file_path)
        #return self.image_file_path

    def set_dimensions(self):
        self.dimensions = self.image_content.size

    def is_ratio_valid(self):
        width, height = self.dimensions
        # Some arbritrary aspect ratio requirement that is < 16/9
        if width / height > 10/7:
            return True
        return False

    def add_favourite(self):
        pass

    def is_image_duped(self):
        # we dont want to show duped images
        pass

    def change_background(self):
        """
        Uses in-built OS commands to change the background. Only works for Windows as of now.
        """
        ctypes.windll.user32.SystemParametersInfoW(20, 0, self.image_file_path,
                                                   3)  # Setting background for all four monitors
        print("Changed background.\n")
