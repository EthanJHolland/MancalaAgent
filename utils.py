def display(buffer, animate):
    """ uses ansi escape codes to move the cursor up then prints each element of buffer on a new line """
    print(('\033[F' * (len(buffer) + 1) if animate else '') + '\n'.join(buffer))