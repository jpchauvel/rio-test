from __future__ import annotations

from pathlib import Path
from typing import *  # type: ignore

import rio

from . import pages
from . import components as comps

# Define a theme for Rio to use.
#
# You can modify the colors here to adapt the appearance of your app or website.
# The most important parameters are listed, but more are available! You can find
# them all in the docs
#
# https://rio.dev/docs/api/theme
theme = rio.Theme.from_colors(
    primary_color=rio.Color.from_hex("01dffdff"),
    secondary_color=rio.Color.from_hex("0083ffff"),
    light=True,
)


# Create the Rio app
app = rio.App(
    name="rio tutorial",
    pages=[
        rio.Page(
            name="Home",
            page_url="",
            build=pages.TicTacToePage,
        ),
    ],
    theme=theme,
    assets_dir=Path(__file__).parent / "assets",
)
