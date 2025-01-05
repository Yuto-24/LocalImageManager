"""
Heic 2 JPG or PNG Converter

You can just use it as below.

```python
import HeicConverter

heic_converter = HeicConverter(img_dir)
heic_converter.convert()
```
"""

import re
import os
from os.path import join, isfile, isdir
import time
import shutil

import pyheif
import piexif
from PIL import Image
from tqdm.notebook import tqdm

from config import config
from src.utils import logger


class HeicConverter:
    """
    When call convert
    1. Try to process all the HEIC files
    2. Check if output_file have not already exist
    3. Convert HEIC into JPG
    4. Save file
    5. Move HEIC file to ./Converted/
    """

    def __init__(self, image_dir: str):
        self.img_dir = image_dir
        self.img_path_list = [
            join(image_dir, f) for f in sorted(os.listdir(image_dir))
            if isfile(join(image_dir, f))
        ]
        self.heic_path_list = [
            f for f in self.img_path_list
            if f.endswith(".heic")
        ]
        self.skipped_heic_list = [].copy()
        self.cnt_converted_files = 0
        # logging
        # logger.debug("self.img_path_list:\n" + "\n".join(self.img_path_list))
        logger.debug("self.heic_path_list:\n" + "\n".join(self.heic_path_list))
        # logger.debug("self.skipped_heic_list:\n" + "\n".join(self.skipped_heic_list))

    def find_convert_list(self) -> dict:
        """
        Find the list of convert file.
        Return include the pair of heic and jpg which will be made.
        """
        ret_dict = {}.copy()

        for heic_file_path in self.heic_path_list:
            # Define output file
            output_file_path = self.__get_output_file_path(heic_file_path)
            ret_dict[heic_file_path] = {}
            ret_dict[heic_file_path]["moved_org"] = join(config.img_dir,
                                                         "HEIC",
                                                         re.sub(pattern=config.img_dir + "/",
                                                                repl="",
                                                                string=heic_file_path,
                                                                ),
                                                         )
            ret_dict[heic_file_path]["will_be_made"] = output_file_path

        return ret_dict

    def convert(self):
        """
        Don't need any input
        All HEIC file is converted into jpg

        TODO: use self.find_convert_list
        """
        start_time = time.time()
        for heic_file_path in tqdm(self.heic_path_list):
            # Define output file
            output_file_path = self.__get_output_file_path(heic_file_path)

            # Skip if output file is already exist
            if isfile(output_file_path):
                self.skipped_heic_list.append(heic_file_path)
                logger.debug(f"{output_file_path} is already exist. SKIP.")
                continue

            # Convert, move, count
            self.heic_to_jpeg_with_exif(heic_file_path, output_file_path)
            converted_dir = join(config.img_dir, "HEIC")
            if not isdir(converted_dir):
                os.makedirs(converted_dir)
            shutil.move(heic_file_path, join(converted_dir))
            self.cnt_converted_files += 1

        # Logging result
        process_time = time.time() - start_time
        logger.info(f"Process finished with {process_time:.2f} secs.")
        logger.info(f"{self.cnt_converted_files} files are successfully converted.")
        if self.skipped_heic_list:
            logger.warning("Below files are not converted because already file exist.\n" +
                           '\n'.join(self.skipped_heic_list))

    def heic_to_jpeg_with_exif(self, input_path: str, output_path: str):
        """
        Input: input_path, output_path
        Output: None

        When you call this function, heic will convert into output_path.
        """

        # HEIC画像を読み込み
        heif_file = pyheif.read(input_path)

        # EXIFデータの取得
        exif_data = None
        for metadata in heif_file.metadata or []:
            if metadata['type'] == 'Exif':
                exif_data = metadata['data']
                break

        # PIL Imageに変換
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )

        # JPEGに変換して保存
        if exif_data:
            exif_dict = piexif.load(exif_data)
            exif_bytes = piexif.dump(exif_dict)
            image.save(output_path, "jpeg", exif=exif_bytes)
        else:
            image.save(output_path, "jpeg")

        logger.trace(f"Converted {input_path} to {output_path}")

    def __get_output_file_path(self, input_file_path: str):
        return input_file_path.replace(".heic", ".jpg")
