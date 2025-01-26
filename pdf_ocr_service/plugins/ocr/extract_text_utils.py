import os
import re
import shutil
from pathlib import Path


def get_page_number(input_file_path: Path) -> int:
    """
    Given input_file_path it returns page number as integer

    e.g.:
      Path("/tmp/medis/000001_ocr.jpeg") => 0
      Path("/tmp/media/000022_ocr.txt") => 21
    """
    if not isinstance(input_file_path, (Path, str)):
        raise ValueError("Expecting Path or str instance as input.")
    if len(str(input_file_path)) < 6:
        raise ValueError("Expecting path to be at least 6 chars long.")

    PATTERN = r"\/(?P<page_num>\d{6})"
    match = re.search(PATTERN, str(input_file_path))
    if match:
        result = match.group('page_num')
        return int(result.lstrip("0")) - 1

    raise ValueError(f"Input {input_file_path} did not match expected pattern.")


def get_result_file_path(
        input_file_path: Path,
        *,
        base_dir: Path,
        output_ext):
    page_number = get_page_number(input_file_path)
    base_name = os.path.basename(input_file_path)
    root, _ = os.path.splitext(base_name)

    result_dir_path = Path(
        base_dir, f"{page_number}.{output_ext}")

    return result_dir_path


def copy_text(
        input_file_path: Path,
        output_dir: Path):
    output_file_path = get_result_file_path(
        input_file_path,
        base_dir=output_dir,
        output_ext='txt',
    )
    shutil.copy(input_file_path, output_file_path)
