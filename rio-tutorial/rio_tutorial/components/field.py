from __future__ import annotations

from dataclasses import KW_ONLY, field
from typing import *  # type: ignore

import rio

from .. import components as comps


class Field(rio.Component):
    value: Literal["X", "O", ""]
    dim: bool

    on_press: rio.EventHandler[[]] = None

    def build(self) -> rio.Component:
        # if the field is empty, allow the player to press on it. Since buttons
        # would look out of place here, cards are a nice alternative
        match self.value:
            case "":
                return rio.Card(
                    content=rio.Spacer(
                        width=3,
                        height=3,
                    ),
                    on_press=self.on_press,
                )
            case "X":
                color = rio.Color.RED
                icon = "material/close"
            case _:
                color = rio.Color.BLUE
                icon = "material/circle"

        # If a player has won, and this field isn't par of the winning
        # combination, dim it.
        if self.dim:
            color = color.replace(opacity=0.2)

        return rio.Icon(
            icon=icon,
            fill=color,
            width=3,
            height=3,
        )
