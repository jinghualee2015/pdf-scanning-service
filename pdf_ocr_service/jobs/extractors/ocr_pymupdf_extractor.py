import os

from pdf_ocr_service.jobs.extractors import PyMupdfExtractor


class OcrPyMupdfExtractor(PyMupdfExtractor):
    def __init__(self):
        super().__init__()
        self._side_car_path = None

    def init_side_car_path(self, side_car_path: str = ''):
        self._side_car_path = side_car_path

    def extract_page(self) -> dict:
        result = {}
        content = ''
        pages = []
        files = os.listdir(self._side_car_path)
        if len(files) <= 0:
            result['content'] = content
            result['pages'] = pages
            return result
        sorted_files = sorted(files, key=lambda name: int(name.split(".")[0]))

        for page_number, file in enumerate(sorted_files):
            text_path = f"{self._side_car_path}/{file}"
            with open(text_path, 'r') as page_file:
                page_content = page_file.read()
            page_content = page_content if page_content is not None else ''
            content = content + page_content
            page_info = {
                "content": page_content,
                "page": page_number
            }
            pages.append(page_info)
        result['content'] = content
        result['pages'] = pages
        return result
