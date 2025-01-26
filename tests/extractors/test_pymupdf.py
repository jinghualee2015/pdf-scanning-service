import json
import os
import unittest

import fitz

from pdf_ocr_service.jobs.domains import TokenPosition
from pdf_ocr_service.jobs.extractors import BasePdfExtractor, PyMupdfExtractor


class PyMuPdfExtractorTest(unittest.TestCase):
    def setUp(self):
        self.extractor: BasePdfExtractor = PyMupdfExtractor()

    def _get_text(self, blocks: dict) -> str:

        page_text = ''
        for block in blocks:
            if len(block) >= 5:
                str_content = block[4]
                page_text += str_content
        return page_text

    def test_multi_columns_pdf_ocr(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "71089-ocr.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        page = pdf[5]
        text = page.get_text("text")
        print(text)

    def test_multi_columns_pdf_7107(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "71017.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        # print(pdf.metadata)
        creator = pdf.metadata.get('creator')
        # print(creator)
        if creator is not None:
            print(creator)
            if "Tesseract OCR-PDF" in creator:
                print("ocr parsed document")
        page = pdf[5]
        text = page.get_text("blocks")
        print(text)

    def test_extract_dict(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "71017.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        page = pdf[5]

        dict_param = {
            "blocks": [
                {
                    "type": 0,
                    "bbox": (79.34321594238281, 58.1813850402832, 541.1229248046875, 105.17866516113281),
                }
            ]
        }
        text = page.get_text("dict", sort=True)
        print(text)

        # 79.34321594238281, 58.1813850402832, 541.1229248046875, 105.17866516113281

    def test_multi_columns_pdf_2291_1(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "2291_1.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        page = pdf[0]
        text = page.get_text("text", flags=fitz.TEXTFLAGS_TEXT)
        # print(text)
        positions = page.search_for("1", flags=fitz.TEXTFLAGS_TEXT)

        token_positions: list[TokenPosition] = []
        sort_rects = sorted(positions, key=lambda rect: (rect.x0, rect.y0, rect.x1, rect.y1))
        for p in sort_rects:
            token_positions.append(
                TokenPosition(
                    left=p.x0,
                    right=p.x1,
                    top=p.y0,
                    bottom=p.y1
                )
            )
        pre_position = token_positions[10]
        position = PyMupdfExtractor.get_nearest_position(find_positions=sort_rects, nearest_position=pre_position)
        print(position.__dict__)

    def test_multi_columns_pdf(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "71017.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        print(pdf.metadata)
        page = pdf[5]
        print(page.get_text('text', flags=fitz.TEXTFLAGS_TEXT))
        tokon_str = 'FDA, while recognizing the differences between the manufacture of';

        ps = page.search_for(tokon_str, flags=fitz.TEXTFLAGS_TEXT)

        for inst in ps:
            higghlight = page.add_highlight_annot(inst)
        pdf.save(os.path.join(os.path.dirname(__file__), "../examples", "71017-ocr-positions.pdf"), garbage=4,
                 deflate=True,
                 clean=True)

    def test_multi_columns_pdf2(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "pdf-3.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        print(pdf.metadata)
        for page in pdf:
            print(page.number)

    def test_ocred_pdf(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "K940242_ocr.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        for page in pdf:
            print(page.number)

    def test_large_pdf(self):
        pdf = fitz.open("/Users/jinghuali/Desktop/PDF/语言/Programming Rust 2nd Edition.pdf", filetype="pdf")
        for page in pdf:
            print(page.number)

    def test_extract(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "71017.pdf")
        self.extractor.init_pdf(pdf_file=pdf_path)
        result: dict = self.extractor.extract_page()
        print(result.get('content'))
        for token in result.get('pages'):
            print(token)

        tokens = 'Guideline maintained by: Food and Drug Administration Center for Drug Evaluation amd Research Office of'
        positions = self.extractor.extract_position(page_number=2, token=tokens)
        for p in positions:
            print(json.dumps(p.__dict__))

    def test_extract_original(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "pdf-3.pdf")
        self.extractor.init_pdf(pdf_file=pdf_path)
        result: dict = self.extractor.extract_page()
        print(result.get('content'))
        for token in result.get('pages'):
            print(token)

        tokens = 'inson, San Jose, CA, USA). A rabbit isotype antibody was used as a negative'
        positions = self.extractor.extract_position(page_number=1, token=tokens)
        for p in positions:
            print(json.dumps(p.__dict__))

    def test_extract_generate_break_line(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "pdf-3.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        page = pdf[1]
        page_text = page.get_text("blocks")  # "text", flags=fitz.TEXTFLAGS_TEXT
        print(page_text)
        token = 'FDA recognizes that the experimental nature of the drug substance, formulation, and dosage form at an early stage of development will have an impact on establishing specifications. At early stages, the acceptance/rejection criteria may not be as specific; however, it is vital that such criteria be scientifically sound and based upon available scientific data. Specifications used as the basis for approval or rejection of components, containers, and closures will be more specific and uniform as additional data become available. It is vital that, at all stages, specifications used are fully documented.'
        positions = page.search_for(token)
        print(positions)

    def test_highlight(self):
        tokens = """Guidance 
FDA recognizes 
that the experimental nature 
of 
the drug 
substance, 
formulation, 
and dosage 
form 
at 
an early 
stage 
of 
development will have 
an impact 
on establishing specifications. 
At early stages, 
the acceptance/rejection criteria may not 
be 
as 
specific; 
however, 
it 
is vital that such criteria 
be 
scientifically sound and based upon available scientific data. 
Specifications used 
as the basis 
for approval 
or rejection of 
components, 
containers, 
and closures will 
be more specific and 
uniform as additional data become available. 
It 
is vital that, 
at 
all 
stages, 
specifications used are fully documented. 
IV. 
PRODUCTION AND PROCESS CONTROLS 
Requirements 
Section 211.100 requires, 
in part, 
that procedures that have 
a 
bearing 
on quality 
of drug products 
be written, 
be approved 
by 
the quality control unit, 
and be followed and documented 
in the 
execution 
of 
the production 
and process controls. 
Guidance 
During the 
IND stage 
of drug development, 
written production and 
control procedures are developed and initially may be more 
general because 
such procedures 
and controls 
are usually 
undergoing considerable refinement. 
However, 
initial procedures 
should 
be 
as complete and detailed as knowledge and experience 
with the product and dosage 
form permit. 
It 
is important that 
initial procedures 
be reviewed and approved prior to 
implementation, 
that they 
be followed, 
and that they be 
documented"""
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "71017.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        page = pdf[6]
        lines = tokens.split("\n")
        for line in lines:
            text_instances = page.search_for(line)
            for inst in text_instances:
                higghlight = page.add_highlight_annot(inst)

        pdf.save(os.path.join(os.path.dirname(__file__), "../examples", "71017-positions.pdf"), garbage=4, deflate=True,
                 clean=True)

    def test_highlight2(self):
        tokens = """of drug development, 
written production and 
control procedures are developed and initially may be more 
general because 
such procedures 
and controls 
are usually 
undergoing considerable refinement. 
However, 
initial procedures 
should 
be 
as complete and detailed as knowledge and experience 
with the product and dosage 
form permit. 
It 
is important that 
initial procedures 
be reviewed and approved prior to 
implementation, 
that they 
be followed, 
and that they be 
documented 
at the time 
of performance. 
It 
is vital that actual 
specific process control procedures 
and conditions 
such 
as 
timing, 
temperature, 
pressure, 
and adjustments 
(e.g., 
mixing, 
filtration, 
drying) 
be fully documented to permit review and 
approval 
by the quality control unit 
and 
to permit development 
of 
more specific written production and control procedures 
as 
research and development reach conclusion. 
It 
is essential that 
all changes from initial procedures 
be fully documented, 
and be 
based 
on well-founded scientific data 
or expert knowledge 
of 
researcher having training 
and experience 
in the 
field 
of science 
being applied. 
Vv. 
CALCULATION 
OF YIELD 
Requirements 
Section 211.103 
requires calculations 
of actual yield 
and 
percentages 
of theoretical 
yield, 
at 
each appropriate phase of"""
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "71017.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        page = pdf[6]
        lines = tokens.split("\n")
        for line in lines:
            text_instances = page.search_for(line)
            for inst in text_instances:
                higghlight = page.add_highlight_annot(inst)

        pdf.save(os.path.join(os.path.dirname(__file__), "../examples", "71017-positions2.pdf"), garbage=4,
                 deflate=True,
                 clean=True)

    def test_highlight3(self):
        tokens = """inson, San Jose, CA, USA). A rabbit isotype antibody was used as a negative
control.
Immunocytochemistry and image analysis
Eosinophils were ﬁxed (acetone-methanol 1:1, v/v) on poly-L-lysine-coated
glass slides. Nonspeciﬁc labeling was blocked with 1% IgG-free BSA, 10%
human serum, 10% swine serum, and protein block. Cells were incubated with
B1R or B2R antibodies (2 h, room temperature), followed by AlexaFluor-
conjugated goat anti-rabbit IgG. As negative controls, a rabbit isotype antibody
was used, or primary antibody was omitted. Mounted slides were viewed on a
Bio-Rad MRC 1000/1024 UV laser-scanning confocal microscope (Bio-Rad,
Hercules, CA, USA) at a magniﬁcation of 600�. The ﬂuorescence intensity
over the area of a single cell was integrated, and nonspeciﬁc ﬂuorescence
(negative control) was subtracted. Net ﬂuorescence intensity was divided by
the average area of the eosinophil in �m2 and expressed as ﬂuorescence
intensity units (FIU)/�m2. For statistical analyses, average net intensity values
were calculated from a minimum of 100 cells per sample.
RNA extraction and RT-PCR
Total RNA was isolated from eosinophils and treated with DNase 1 (RNeasy
kit, Qiagen, Melbourne, Australia). Semiquantitative one-step RT-PCR
(Qiagen) was performed using B1R primers (sense: 5�-TTCTTATTCCAGGT-
GCAAGCAG-3�; antisense: 5�-CTTTCCTATGGGATGAAGATAT-3�), B2R
primers (sense: 5�-TGCTGCTGCTATTCATCATC-3�; antisense: 5�-CCAGTC-
CTGCAGTTTGTGAA-3�), and 18S rRNA primers (sense: 5�-CATGCTAAC-"""
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "pdf-3.pdf")
        pdf = fitz.open(pdf_path, filetype="pdf")
        page = pdf[1]
        lines = tokens.split("\n")
        for line in lines:
            text_instances = page.search_for(line, flags=fitz.TEXTFLAGS_TEXT)
            print(f"line:{line}, position:{text_instances}")
            for inst in text_instances:
                higghlight = page.add_highlight_annot(inst)

        pdf.save(os.path.join(os.path.dirname(__file__), "../examples", "pdf-3-positions.pdf"), garbage=4,
                 deflate=True,
                 clean=True)
