import logging
import re
from typing import Optional, Union

from burplist.utils.styles import styles

logger = logging.getLogger(__name__)


def parse_name(raw_name: str) -> str:
    """
    Sanitize product name
    """
    logger.info(f'Parsing raw_name "{raw_name}".')

    remove_brackets = re.sub(r'[\(\[].*?[\]\)]', '', raw_name)  # E.g.: "Somersby Blackberry Cider [CANS] 330ml"
    remove_non_word_characters = re.sub(r'[^a-zA-Z0-9%.\']', ' ', remove_brackets)
    remove_spaces = re.sub(' +', ' ', remove_non_word_characters)

    return remove_spaces.strip()


def parse_style(raw_style: str) -> Optional[str]:
    return next((style for style in styles if style.lower() in raw_style.lower()), None)


def parse_origin(raw_origin: str) -> Optional[str]:
    pass


def parse_abv(raw_abv: str) -> Optional[float]:
    has_float_abv = re.search(r'(\d{1,2}\.\d{1,2})%', raw_abv)
    if has_float_abv:
        return float(has_float_abv.group(1))

    has_int_abv = re.search(r'(\d{1,2})%', raw_abv)
    if has_int_abv:
        return float(has_int_abv.group(1))


def parse_volume(raw_name: str) -> Optional[int]:
    """
    Get product volume from name
    """
    has_volume = re.search(r'(\d{3}) ?ml', raw_name, flags=re.IGNORECASE)
    if has_volume:
        return int(has_volume.group(1))


def parse_quantity(raw_name: Union[str, int]) -> int:
    """
    Get product quantity from name
    """
    if isinstance(raw_name, int):
        return raw_name

    # Carlsberg 490ml x 24 Cans (BBD: Oct 2021)
    is_n_package = re.search(r'(\d{1,2}) ?(?:Bottle|Btl|Can|Case|Pack|Pint)', raw_name, flags=re.IGNORECASE)
    if is_n_package:
        return int(is_n_package.group(1))

    # Carlsberg Danish Pilsner Beer Can 490ml (Pack of 24) Green , Carlsberg Smooth Draught Beer Can, 320ml [Bundle of 24]
    is_package_of = re.search(r'(?:Bundle|Case|Pack|Package|Pint) of (\d{1,2})', raw_name, flags=re.IGNORECASE)
    if is_package_of:
        return int(is_package_of.group(1))

    # Tiger Lager Beer Can 40x320ml, Guinness Foreign Extra Stout 24 x 500ml
    is_ml = re.search(r'(\d{1,2}) ?[x] ?', raw_name, flags=re.IGNORECASE)
    if is_ml:
        return int(is_ml.group(1))

    # Heineken Beer 330ml x 24 can
    is_ml_reverse = re.search(r' ?[x] ?(\d{1,2}) ?', raw_name, flags=re.IGNORECASE)
    if is_ml_reverse:
        return int(is_ml_reverse.group(1))

    return 1
