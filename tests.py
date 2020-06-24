import unittest
import background
import os.path


class MyTestCase(unittest.TestCase):
    past_url_testing = ["https://i.redd.it/eqhlkjhh1p151.jpg"]
    bg_valid_ratio_hires = background.Background("https://i.redd.it/eqhlkjhh1p151.jpg", 'wallpaper')
    bg_invalid_url = background.Background("https://i.redd.it/eqhlkjhh1p151.test", "test")
    bg_invalid_ratio = background.Background("https://cdnb.artstation.com/p/assets/images/images/026/905/135/large/kotakan-kinokonoyamanoshiro20200520-1000.jpg?1590054349",
                                             "ImaginaryCastles")
    bg_clipped_ratio = background.Background("https://cdna.artstation.com/p/assets/images/images/026/798/234/large/z-4-zero-.jpg",
                                             'ImaginaryCastles')

    def test_0_pull_image_from_reddit(self):
        self.assertEqual(True, self.bg_valid_ratio_hires.get_image_from_url())
        self.assertEqual(False, self.bg_invalid_url.get_image_from_url())
        self.assertEqual(True, self.bg_invalid_ratio.get_image_from_url())
        self.assertEqual(True, self.bg_clipped_ratio.get_image_from_url())

    def test_1_is_aspect_ratio_valid(self):
        self.bg_valid_ratio_hires.get_dimensions()
        self.bg_invalid_ratio.get_dimensions()
        self.bg_clipped_ratio.get_dimensions()
        self.assertEqual(False, self.bg_valid_ratio_hires.is_ratio_invalid())
        self.assertEqual(True, self.bg_invalid_ratio.is_ratio_invalid())
        self.assertEqual(False, self.bg_clipped_ratio.is_ratio_invalid())

    def test_2_is_image_duplicated(self):
        self.assertEqual(True, self.bg_valid_ratio_hires.is_image_duped(self.past_url_testing))
        self.assertEqual(False, self.bg_clipped_ratio.is_image_duped(self.past_url_testing))

    def test_3_saving_image_to_file(self):
        self.bg_valid_ratio_hires.save_image_to_file()
        self.assertEqual(True, os.path.isfile(self.bg_valid_ratio_hires.image_file_path))

    def test_4_set_image_background(self):
        # Should only fail for non-Windows OS but cannot unit test this
        self.assertEqual(True, self.bg_valid_ratio_hires.change_background())

    def test_x_add_favourite(self):
        pass

    def test_x_skip_current_image(self):
        pass


if __name__ == '__main__':
    unittest.main()
