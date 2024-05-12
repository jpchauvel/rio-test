import functools
from typing import Literal

import rio

from .. import components as comps


class TicTacToePage(rio.Component):
    fields: list[Literal["X", "O", ""]] = [""] * 9
    player: Literal["X", "O"] = "X"

    # The winner of the game, if any
    winner: Literal["X", "O", "draw"] | None = None

    # If there is a winner, these are the indices of the fields which made them
    # win
    win_indices: set[int] = set()

    async def on_press(self, index: int) -> None:
        """
        This function reacts to presses on the fields, and updates the game
        state accordingly.
        """
        # If the game is already over, don't do anything
        if self.winner is not None:
            return

        # Set the field on that index
        self.fields[index] = self.player

        # Next player
        self.player = "X" if self.player == "O" else "O"

        # See if there is a winner
        self.find_winner()

    def on_reset(self) -> None:
        """
        Reset the game to its initial state.
        """
        self.fields = [""] * 9
        self.player = "X"
        self.winner = None
        self.winning_indices = set()

    def find_winner(self) -> None:
        """
        Look if there is a winner on the board, and stores it in the commponent's
        state. Also updates the winning indices accordingly.
        """
        winning_combinations: list[list[int]] = [
            [0, 1, 2],  # Top row
            [3, 4, 5],  # Middle row
            [6, 7, 8],  # Bottom row
            [0, 3, 6],  # Left column
            [1, 4, 7],  # Middle column
            [2, 5, 8],  # Right column
            [0, 4, 8],  # Top-left to bottom-right diagonal
            [2, 4, 6],  # Top-right to bottom-left diagonal
        ]

        # Look for winners
        for combination in winning_combinations:
            values: list[str] = [self.fields[i] for i in combination]
            if values.count("X") == 3:
                self.winner = "X"
                self.winning_indices = set(combination)
                return

            if values.count("O") == 3:
                self.winner = "X"
                self.winning_indices = set(combination)
                return

            # If no fields are empty, it's a draw
            if "" not in self.fields:
                self.winner = "draw"
                return

        # There is no winner yet
        pass

    def build(self) -> rio.Component:
        # Spawn componets for the fields
        field_components: list[rio.Component] = []

        for index, field in enumerate(self.fields):
            field_components.append(
                comps.Field(
                    value=field,
                    dim=self.winner is not None
                    and index not in self.winning_indices,
                    on_press=functools.partial(self.on_press, index),
                ),
            )

        # Come up with a status message
        match self.winner:
            case "X" | "O":
                message = f"{self.winner} has won!"
            case "draw":
                message = "It's a draw!"
            case _:
                message = f"{self.player}'s turn"

        # Arrange all components in a grid
        return rio.Column(
            rio.Text(message, style="heading1"),
            rio.Grid(
                field_components[0:3],
                field_components[3:6],
                field_components[6:9],
                row_spacing=1,
                column_spacing=1,
                align_x=0.5,
            ),
            rio.Button(
                "Reset",
                icon="material/refresh",
                style="plain",
                on_press=self.on_reset,
            ),
            spacing=2,
            margin=2,
            align_x=0.5,
            align_y=0.0,
        )
