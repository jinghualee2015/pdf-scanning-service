import os
from PIL import Image
import unittest

class ImageTest(unittest.TestCase):
    def get_image_dpi(self,path):
        try:
            with Image.open(path) as img:
                dpi = img.info.get('dpi')
                return dpi
        except Exception as e:
            print(f"Error occured:{e}")
            return None
    
    def test_get_dpi(self):
        image_path = os.path.join(os.path.dirname(__file__), "../examples", "img.png")
        dpi = self.get_image_dpi(path= image_path)
        print(f"dpi={dpi}")
    