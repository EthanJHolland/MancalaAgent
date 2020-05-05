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

def option_list_to_text(options):
    """ converts a list of strings to a comma seperated list (example: ['1', '3', '4'] => '1, 3, or 4') """
    if not options:
        return ''
    elif len(options) == 1:
        return options[0]
    elif len(options) == 2:
        return f'{options[0]} or {options[1]}'
    else:  # length >= 2
        return f'{", ".join(options[:-1])}, or {options[-1]}'

def display_board(bottom_row, top_row, right_score, left_score, animate, options=None):
    """ display a board 
    params:
        - bottom_row: the number of marbles in each cup of the bottom row of the board from left to right
        - top_row: the number of marbles in each cup of the top row of the board from right to left (left to right from the top player's perspective)
        - right_score: the number of marbles in the right goal
        - left_score: the number of marbles in the left goal
        - animate: if true, 
        - options: bottom row cups which should be labeled (for use displaying options for a human agent)
    """
    assert len(bottom_row) == len(top_row)

    border_len = 2 * (end_width + 1) + len(top_row) * (cup_width + 1) + 1

    out = [
        HBORDER * border_len,
        _row_to_string(reversed(top_row)),  # reverse opponents row to see from player's perspective
        VERT + _center_text(left_score, end_width, True) + (VERT + HMID * 3) * len(top_row) + VERT + _center_text(right_score, end_width) + VERT,
        _row_to_string(bottom_row),
        HBORDER * border_len
    ]

    if options:
        option_strings = [(_center_text(i, cup_width) if i in options else (' ' * cup_width)) for i in range(len(bottom_row))]
        out.append(' ' * (end_width + 2) + ' '.join(option_strings))

    _display(out, animate)
