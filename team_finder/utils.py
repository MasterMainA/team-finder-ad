import os
from dataclasses import dataclass
from io import BytesIO
from urllib.parse import urlencode

from django.core.files.base import ContentFile
from django.http import HttpRequest
from PIL import Image, ImageDraw, ImageFont

from team_finder import constants


@dataclass
class PaginatorInfo:
    has_other_pages: bool
    has_previous: bool
    page_range: list[int]
    current_page_number: int
    previous_page_number: int
    has_next: bool
    next_page_number: int


def get_font(size):
    for path in constants.FONT_PATHS:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except (OSError, IOError, TypeError):
                continue

    return ImageFont.load_default()


def build_query_prefix_from_request(
    request: HttpRequest, params_from_url_to_save_in_query: list[str]
):
    filtered_params = {
        key: value
        for key, value in request.GET.items()
        if key in params_from_url_to_save_in_query
    }

    if not filtered_params:
        return ""

    query_string = urlencode(filtered_params)
    return f"{query_string}&"


def generate_avatar_from_initials(user):
    name_char = user.name[0] if user.name else "U"
    surname_char = user.surname[0] if user.surname else ""
    initials = (name_char + surname_char).upper()

    img = Image.new(
        "RGB",
        (constants.AVATAR_SIZE, constants.AVATAR_SIZE),
        color=constants.AVATAR_COLOR,
    )
    draw = ImageDraw.Draw(img)
    font = get_font(size=constants.AVATAR_FONT_SIZE)

    bbox = draw.textbbox((0, 0), initials, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    position = (
        (constants.AVATAR_SIZE - w) // 2,
        (constants.AVATAR_SIZE - h - constants.AVATAR_FONT_SIZE // 2) // 2,
    )

    draw.text(position, initials, fill="white", font=font)
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    user.avatar.save(
        f"avatar_{user.username}.png", ContentFile(buffer.getvalue()), save=False
    )


async def get_paginator_info(
    projects_total_count, page_number: int, elements_per_page: int
):
    pages_cnt = (
        projects_total_count // elements_per_page + 1
        if projects_total_count % elements_per_page
        else 0
    )
    return PaginatorInfo(
        projects_total_count > elements_per_page,
        page_number >= 2,
        [_ for _ in range(1, pages_cnt + 1)],
        page_number,
        page_number - 1,
        page_number != pages_cnt,
        page_number + 1,
    )
