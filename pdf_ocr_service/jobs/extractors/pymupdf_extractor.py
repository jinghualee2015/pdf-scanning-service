from pdf_ocr_service.jobs.domains import TokenPosition, DocumentProcessResult
from pdf_ocr_service.jobs.extractors import BasePdfExtractor
import fitz
from lxml import etree
from pdf_ocr_service.celery import task_logger

logger = task_logger


class PyMupdfExtractor(BasePdfExtractor):
    creator_meta_data_key = 'creator'
    creator_key_value = "Tesseract OCR-PDF"

    def init_pdf(self, pdf_file: str = None):
        self.pdf_file = pdf_file
        try:
            self.pdf_obj = fitz.open(self.pdf_file, filetype="pdf")
        except Exception as ex:
            raise ex

    def extract_page(self) -> dict:
        result = {}
        content = ''
        pages = []
        content_method = self._get_extract_method()
        for page in self.pdf_obj:
            page_content = content_method(page=page)  # page.get_text()
            content = content + page_content
            page_info = {
                "content": page_content,
                "page": page.number
            }
            pages.append(page_info)
        result['content'] = content
        result['pages'] = pages
        return result

    def _get_extract_method(self):
        pdf_meta_data = self.pdf_obj.metadata
        if pdf_meta_data is not None:
            creator = pdf_meta_data.get(PyMupdfExtractor.creator_meta_data_key)
            if (creator is not None and
                    PyMupdfExtractor.creator_key_value in creator):
                return PyMupdfExtractor.get_xhtml_content

        return PyMupdfExtractor.get_text_content

    @classmethod
    def get_text_content(cls, page):
        page_content = page.get_text('text', flags=fitz.TEXTFLAGS_TEXT)
        return page_content

    @classmethod
    def get_xhtml_content(cls, page):
        text = page.get_text("xhtml", flags=fitz.TEXTFLAGS_XHTML)
        html_content = etree.HTML(text)
        contents = html_content.xpath("//tt/text()")
        page_content = ''
        if len(contents) <= 0:
            return page_content
        for content in contents:
            page_content += content
        return page_content + '\n'

    def extract_position(self,
                         page_number: int = None,
                         block_number: int = None,
                         token: str = None, **kwargs) -> list[TokenPosition]:
        result: list[TokenPosition] = []
        token_lines = token.split("\n")
        page = self.pdf_obj.load_page(page_number)
        block_number = kwargs.get('block_numer')
        process_result: DocumentProcessResult = kwargs.get('process_result')
        for line in token_lines:
            line = line.strip()
            if line == '':
                continue
            positions = page.search_for(line, flags=fitz.TEXTFLAGS_TEXT)
            if positions is None or len(positions) <= 0:
                continue
            positions = sorted(positions, key=lambda rect: (rect.y0, rect.x0, rect.x1, rect.y1))
            PyMupdfExtractor.process_normal(line=line,
                                            page_number=page_number,
                                            block_number=block_number,
                                            result=result,
                                            positions=positions)

        process_result.add_page_positions(page_number=page_number,
                                          block_number=block_number,
                                          positions=result)

        return result

    @classmethod
    def process_normal(cls, line: str = '',
                       page_number: int = -1,
                       block_number: int = -1,
                       result: list = [],
                       positions: list = [], ):
        for p in positions:
            tp = PyMupdfExtractor.rect_to_position(rect=p)
            logger.debug(
                f"[extract_position] page={page_number} block_number={block_number} line={line} position={tp}")
            if PyMupdfExtractor.valid_token_position(position=tp,
                                                     result_set=result):
                result.append(tp)

    @classmethod
    def process_specially(cls,
                          line: str = '',
                          page_number: int = -1,
                          block_number: int = -1,
                          result: list = [],
                          positions: list = [],
                          process_result: list[DocumentProcessResult] = [],
                          ):
        if len(line) <= 1:
            # process word or single character
            nearest_position = PyMupdfExtractor.get_previous_position(current_page_positions=result,
                                                                      page_number=page_number,
                                                                      block_number=block_number,
                                                                      process_result=process_result)
            token_position = PyMupdfExtractor.get_nearest_position(find_positions=positions,
                                                                   nearest_position=nearest_position)
            token_position_info = token_position if token_position else 'token_position is none'
            logger.info(
                f"[extract_position] page={page_number} block_number={block_number} line={line} position={token_position_info}")
            if PyMupdfExtractor.valid_token_position(position=token_position,
                                                     result_set=result):
                result.append(token_position)
        else:
            # process normal statement
            for p in positions:
                tp = PyMupdfExtractor.rect_to_position(rect=p)
                logger.info(
                    f"[extract_position] page={page_number} block_number={block_number} line={line} position={tp}")
                if PyMupdfExtractor.valid_token_position(position=tp,
                                                         result_set=result):
                    result.append(tp)

    @classmethod
    def get_previous_position(cls,
                              current_page_positions: list[TokenPosition],
                              page_number: int,
                              block_number: int,
                              process_result: DocumentProcessResult,
                              ):
        if current_page_positions is not None \
                and len(current_page_positions) > 0:
            return current_page_positions[len(current_page_positions) - 1]
        pre_block = block_number - 1
        while pre_block >= 0:
            page_positions: list[TokenPosition] = process_result.get_page_positions_key(page_number=page_number,
                                                                                        block_number=pre_block)
            if page_positions is not None \
                    and len(page_positions) > 0:
                return page_positions[len(page_positions) - 1]

            pre_block = pre_block - 1
        return None

    @classmethod
    def valid_token_position(cls, position: TokenPosition,
                             result_set: list[TokenPosition] = []) -> bool:
        if position is not None \
                and position.is_valid() \
                and position not in result_set:
            return True
        return False

    @classmethod
    def get_nearest_position(cls,
                             find_positions: list = [],
                             nearest_position: TokenPosition = None) -> TokenPosition:
        if find_positions is None \
                or len(find_positions) <= 0:
            return None
        if nearest_position is None:
            # the first statement just return the first
            return PyMupdfExtractor.rect_to_position(rect=find_positions[0])
        for rect in find_positions:
            p = PyMupdfExtractor.rect_to_position(rect=rect)
            if p is not None \
                    and p > nearest_position:
                return p
        return None

    @classmethod
    def rect_to_position(cls, rect=None) -> TokenPosition:
        if rect is None:
            return None
        tp = TokenPosition(left=rect.x0,
                           right=rect.x1,
                           top=rect.y0,
                           bottom=rect.y1)
        return tp

    def _positions_to_tp(self, positions: list = None) -> TokenPosition:
        length = len(positions)
        if length <= 0:
            return None
        if length == 1:
            p = positions[0]
            tp = TokenPosition(left=p.x0,
                               right=p.x1,
                               top=p.y0,
                               bottom=p.y1)
            return tp
        else:
            final_top = final_left = 20000
            final_bottom = final_right = -1
            for p in positions:
                if p.x0 < final_left:
                    final_left = p.x0
                if p.x1 > final_right:
                    final_right = p.x1
                if p.y0 < final_top:
                    final_top = p.y0
                if p.y1 > final_bottom:
                    final_bottom = p.y1
            tp = TokenPosition(left=final_left,
                               right=final_right,
                               top=final_top,
                               bottom=final_bottom)
            return tp

    def __del__(self):
        self.pdf_file = None
        if self.pdf_obj is not None:
            self.pdf_obj.close()
