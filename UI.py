class colors:
    reset = "\033[0m"

    # Black
    fgBlack = "\033[30m"
    fgBrightBlack = "\033[30;1m"
    bgBlack = "\033[40m"
    bgBrightBlack = "\033[40;1m"

    # Red
    fgRed = "\033[31m"
    fgBrightRed = "\033[31;1m"
    bgRed = "\033[41m"
    bgBrightRed = "\033[41;1m"

    # Green
    fgGreen = "\033[32m"
    fgBrightGreen = "\033[32;1m"
    bgGreen = "\033[42m"
    bgBrightGreen = "\033[42;1m"

    # Yellow
    fgYellow = "\033[33m"
    fgBrightYellow = "\033[33;1m"
    bgYellow = "\033[43m"
    bgBrightYellow = "\033[43;1m"

    # Blue
    fgBlue = "\033[34m"
    fgBrightBlue = "\033[34;1m"
    bgBlue = "\033[44m"
    bgBrightBlue = "\033[44;1m"

    # Magenta
    fgMagenta = "\033[35m"
    fgBrightMagenta = "\033[35;1m"
    bgMagenta = "\033[45m"
    bgBrightMagenta = "\033[45;1m"

    # Cyan
    fgCyan = "\033[36m"
    fgBrightCyan = "\033[36;1m"
    bgCyan = "\033[46m"
    bgBrightCyan = "\033[46;1m"

    # White
    fgWhite = "\033[37m"
    fgBrightWhite = "\033[4m"
    bgWhite = "\033[47m"
    bgBrightWhite = "\033[47;1m"

    # Functions
    Questions = "\033[92m"
    Tables = "\033[40m"
    Saved_files = "\033[95m"
    Informational_Headers = "\033[96m\33[4m" # Gives information for decision making, all caps.
    Process_Headers = "\033\1m\033[7m" # Announces which part of the process the user is currently in.
    Categories = fgBlue
    Names = fgYellow
    Errors = "\033[31m"

# c = ''
# for i in range(0,256):
#     c += str(i) + '\33[' + str(i) + 'm,  '
# print(c)
# print(colors.Process_Headers + 'word' + colors.reset)

