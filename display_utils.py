VERT = '|'
HBORDER = '='
HMID = '-'

end_width = 4
cup_width = 3

def _center_text(num, desired_width, justify_left=False):
    extra = desired_width - len(str(num))

    if extra % 2 == 0:
        return ' ' * (extra // 2) + str(num) + ' ' * (extra // 2)
    else:
        return ' ' * (extra // 2 + (not justify_left)) + str(num) + ' ' * (extra // 2 + justify_left)
   
def _row_to_string(row):
    return VERT + ' ' * end_width + VERT + VERT.join([_center_text(n, cup_width) for n in row]) + VERT + ' ' * end_width + VERT

def _display(buffer, animate):
    """ uses ansi escape codes to move the cursor up then prints each element of buffer on a new line """
    print(('\033[F' * (len(buffer) + 1) if animate else '') + '\n'.join(buffer))

def display_board(bottom_row, top_row, right_score, left_score, animate):
    """ display a board """
    assert len(bottom_row) == len(top_row)

    border_len = 2 * (end_width + 1) + len(top_row) * (cup_width + 1) + 1

    out = [
        HBORDER * border_len,
        _row_to_string(reversed(top_row)),  # reverse opponents row to see from player's perspective
        VERT + _center_text(left_score, end_width, True) + (VERT + HMID * 3) * len(top_row) + VERT + _center_text(right_score, end_width) + VERT,
        _row_to_string(bottom_row),
        HBORDER * border_len
    ]

    _display(out, animate)
