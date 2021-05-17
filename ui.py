import os, time, sys, subprocess, math

try:
	import colorama
except ImportError:
	print("Attempting to import colorama")
	print("\nIf you get an error concerning colorama.init()")
	print("you may have to re-start this script before it works correctly")
	input("Press Enter to continue")
	subprocess.check_call([sys.executable, "-m", "pip", "install", 'colorama'])
finally:
	import colorama

colorama.init()

''' Custom error handlers for use during development / debug '''
class AlignException(Exception):
	def __init__(self, message, errors):
		# Call Exception.__init__(message)
		# to use the same Message header as the parent class
		super().__init__(message)
		self.errors = errors
		# Display the errors
		print('Alignment error:')
		print(errors)	

class BoxPartException(Exception):
	def __init__(self, message, errors):
		# Call Exception.__init__(message)
		# to use the same Message header as the parent class
		super().__init__(message)
		self.errors = errors
		# Display the errors
		print('Box constuction error:')
		print(errors)

class ColorValueException(Exception):
	def __init__(self, message, errors):
		# Call Exception.__init__(message)
		# to use the same Message header as the parent class
		super().__init__(message)
		self.errors = errors
		# Display the errors
		print('Colour values error:')
		print(errors)		

class MatchingTagsException(Exception):
	def __init__(self, message, errors):
		# Call Exception.__init__(message)
		# to use the same Message header as the parent class
		super().__init__(message)
		self.errors = errors
		# Display the errors
		print('Colour tags error:')
		print(errors)		


colors = {} #data filled in in initialise()
sep = '~' # default separator character
# colorama foreColour constants
#BLACK = colorama.Fore.BLACK + colorama.Style.NORMAL		# '\x1b[30m'
BLACK = colorama.Fore.BLACK + colorama.Style.BRIGHT			# '\x1b[30m'
WHITE = colorama.Fore.LIGHTWHITE_EX							# '\x1b[97m'
GREY = colorama.Fore.WHITE + colorama.Style.NORMAL 			# '\x1b[37m'
GRAY = colorama.Fore.WHITE + colorama.Style.NORMAL 			# '\x1b[37m'
DGREY = colorama.Fore.LIGHTBLACK_EX							# '\x1b[90m'
DGRAY = colorama.Fore.LIGHTBLACK_EX							# '\x1b[90m'
BLUE = colorama.Fore.LIGHTBLUE_EX							# '\x1b[94m'
GREEN = colorama.Fore.LIGHTGREEN_EX							# '\x1b[92m'
CYAN = colorama.Fore.LIGHTCYAN_EX							# '\x1b[96m'
RED = colorama.Fore.LIGHTRED_EX								# '\x1b[91m'
MAGENTA = colorama.Fore.LIGHTMAGENTA_EX						# '\x1b[95m'
YELLOW = colorama.Fore.LIGHTYELLOW_EX						# '\x1b[93m'
DBLUE = colorama.Fore.BLUE + colorama.Style.NORMAL			# '\x1b[34m'
DGREEN = colorama.Fore.GREEN + colorama.Style.NORMAL		# '\x1b[32m'
DCYAN = colorama.Fore.CYAN + colorama.Style.NORMAL 			# '\x1b[36m'
DRED = colorama.Fore.RED + colorama.Style.NORMAL			# '\x1b[31m'
DMAGENTA = colorama.Fore.MAGENTA + colorama.Style.NORMAL	# '\x1b[35m'
DYELLOW = colorama.Fore.YELLOW + colorama.Style.NORMAL		# '\x1b[33m'

#backColour constants:
BLACKBG = colorama.Back.BLACK + colorama.Style.BRIGHT		# '\x1b[40m'
WHITEBG = colorama.Back.LIGHTWHITE_EX 						# '\x1b[107m'
GREYBG = colorama.Back.WHITE 								# '\x1b[47m'
DGREYBG = colorama.Back.LIGHTBLACK_EX 						# '\x1b[100m'
GRAYBG = colorama.Back.WHITE 								# '\x1b[47m'
DGRAYBG = colorama.Back.LIGHTBLACK_EX 						# '\x1b[100m'
BLUEBG = colorama.Back.LIGHTBLUE_EX							# '\x1b[104m'
GREENBG= colorama.Back.LIGHTGREEN_EX						# '\x1b[102m'
CYANBG = colorama.Back.LIGHTCYAN_EX							# '\x1b[106m'
REDBG = colorama.Back.LIGHTRED_EX							# '\x1b[101m'
MAGENTABG= colorama.Back.LIGHTMAGENTA_EX					# '\x1b[105m'
YELLOWBG = colorama.Back.LIGHTYELLOW_EX						# '\x1b[103m'
DBLUEBG = colorama.Back.BLUE								# '\x1b[44m'
DGREENBG= colorama.Back.GREEN								# '\x1b[42m'
DCYANBG = colorama.Back.CYAN								# '\x1b[46m'
DREDBG = colorama.Back.RED									# '\x1b[41m'
DMAGENTABG= colorama.Back.MAGENTA							# '\x1b[45m'
DYELLOWBG = colorama.Back.YELLOW							# '\x1b[43m'

RESET = colorama.Style.RESET_ALL							# '\x1b[0m'
NORMAL = colorama.Style.NORMAL								# '\x1b[22m'
BRIGHT = colorama.Style.BRIGHT								# '\x1b[1m'

CLEAR = colorama.ansi.clear_screen()						# '\033[2J'

# variables used as constants if user wants to change default colour tag from ~
black = sep + 'black' + sep			# ~black~
white = sep + 'white' + sep
grey = sep + 'grey' + sep
gray = sep + 'grey' + sep
dgrey = sep + 'dgrey' + sep
dgray = sep + 'dgrey' + sep
grey = sep + 'grey' + sep
blue = sep + 'blue' + sep
green = sep + 'green' + sep
cyan = sep + 'cyan' + sep
red = sep + 'red' + sep
magenta = sep + 'magenta' + sep
yellow = sep + 'yellow' + sep
dblue = sep + 'dblue' + sep
dgreen = sep + 'dgreen' + sep
dcyan = sep + 'dcyan' + sep
dred = sep + 'dred' + sep
dmagenta = sep + 'dmagenta' + sep
dyellow = sep + 'dyellow' + sep

blackbg = sep + 'blackbg' + sep			# ~blackbg~
whitebg = sep + 'whitebg' + sep
greybg = sep + 'greybg' + sep
graybg = sep + 'greybg' + sep
dgreybg = sep + 'dgreybg' + sep
dgraybg = sep + 'dgreybg' + sep
greybg = sep + 'greybg' + sep
bluebg = sep + 'bluebg' + sep
greenbg = sep + 'greenbg' + sep
cyanbg = sep + 'cyanbg' + sep
redbg = sep + 'redbg' + sep
magentabg = sep + 'magentabg' + sep
yellowbg = sep + 'yellowbg' + sep
dbluebg = sep + 'dbluebg' + sep
dgreenbg = sep + 'dgreenbg' + sep
dcyanbg = sep + 'dcyanbg' + sep
dredbg = sep + 'dredbg' + sep
dmagentabg = sep + 'dmagentabg' + sep
dyellowbg = sep + 'dyellowbg' + sep

s_symbols_top =    ['┌', '─', '┐', '┬']
s_symbols_bottom = ['└', '─', '┘', '┴']
s_symbols_body =   ['│', ' ', '│', '│']
s_symbols_mid =    ['├', '─', '┤', '┼']

d_symbols_top =    ['╔', '═', '╗', '╦']
d_symbols_bottom = ['╚', '═', '╝', '╩']
d_symbols_body =   ['║', ' ', '║', '║']
d_symbols_mid =    ['╠', '═', '╣', '╬']

dict_single = {
    'top'    : s_symbols_top,
    'body'   : s_symbols_body,
    'mid'    : s_symbols_mid,
    'bottom' : s_symbols_bottom
}

dict_double = {
    'top'    : d_symbols_top,
    'body'   : d_symbols_body,
    'mid'    : d_symbols_mid,
    'bottom' : d_symbols_bottom
}

'''
    The following 'global' variables will be changed in the initialise() function
    Python does not have a static class run-once 'constructor' as found in C#
	so this script runs initialise() on loading.
	Variables declared here are NOT truly global, as in Python they are read-only
	and need the global keyword inside any function that changes the value.
'''
is_console = True	# assume running on a console/terminal until checked in initialise()
window_width = 80 	# default console width
window_height = 25 	# default console height
is_coloured = False # assume not colour capable until checked in initialise()

def add_lines(num_lines, current_lines = None, fore_color = 'white' , back_color = 'blackbg'): #default 30 lines if not given
	''' overloaded Python function: supply None as 2nd parameter'''
	# use 1: add_lines(5) adds 5 additional blank lines
	# use 2: add_lines(5, 19) adds sufficient lines to fill console to last 5 lines (as 19 are already used)
	fore_color, back_color = validate_colors(fore_color, back_color)
	blank = "".rjust(window_width); #string of spaces across entire width of Console
	if current_lines is None:
		if num_lines > 0:
			for i in range(num_lines):
				colorprint(f"{fore_color}{back_color}{blank}") # "~white~~blackbg~ <spaces> "
	else:
		leave_lines = num_lines
		num_lines = window_height - current_lines - leave_lines;
		if num_lines > 0:
			for i in range(num_lines):
				colorprint(f"{fore_color}{back_color}{blank}") # "~white~~blackbg~ <spaces> "

	return num_lines;		

def change_separator(value):
	''' Allows use of different character to separate colour tags. Default is ~ '''
	sep = value[0]		# if user supplies more than 1 character, use the first only. Stored as string
	initialise()    # re-initialise to make use of new character
	
def clear():
	''' clears console using appropriate method for current platform'''
	if is_console:
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')
	else:
		add_lines(window_height)

def colorprint(value, newline = True):
	''' This uses the default char ~ to separate colour strings
	    It allows removal of colour commands if all output is sent with colour tags
		change the line:  sep = "~"  as required
		other possibles are ` (backtick) ¬ (?) any character you will not use
		example value = "~red~This is a line of red text"
	'''
	# print(f"{GREEN}{BLACKBG}This is green text on black background") = "\x1b[92m\x1b[40mThis is green text on black background" direct Colorama method
	# example value = "~red~~blackbg~This is a line of red text" 
	# if not in console, filter out all colour info eg for IDLE or other IDE
	num_lines = 0
	lineparts = split_clean(value, sep) #if already formatted then this will remain as 1 line: "\x1b[92m\x1b[40mThis is green text on black background"
	for line in lineparts: # more than 1 part = text formatted with colour constants in tags "red","blackbg","This is a line of red text"
		if line in colors: #red, blackbg
			if is_coloured:
				if line == "reset":
					print(RESET, end='')
				else:
					print(colors[line], end = '')
		else:
			print(line, end='')
			if "\n" in line:
				num_lines = num_lines +  1
	if is_coloured:
		if newline:		
			print(f'{RESET}')
			num_lines = num_lines +  1
		else:
			print(f'{RESET}', end='')
	else:
		print()
		num_lines = num_lines +  1

	return num_lines

def display_message(message, use_input, use_timer, fore_color = 'white', back_color = 'blackbg', delay = 2):
	''' print a message, either for timed amount, or requiring Enter key'''
	fore_color, back_color = validate_colors(fore_color, back_color)
	if isinstance(message, list): # mulitple lines passed as list not string (equivalent of C# overloaded function)
		if use_timer:
			for msg in message:
				colorprint(f"{fore_color}{back_color}{msg}")
				time.sleep(delay)
		else:
			get_input("Press Enter to continue", '...', fore_color, back_color)
	else:
		if use_timer:
			if message != '':	
				colorprint(f"{fore_color}{back_color}{message}")
				time.sleep(delay)
		if use_input:
			if message =='':
				message = 'Press Enter to continue'
			else:
				message = f"{fore_color}{back_color}{message}"
			get_input(message, '...', fore_color, back_color)

def display_setup(fore_color, back_color):
	''' Run on first use of program to check display is on a console or IDE. User confirms colour '''
	global is_coloured
	valid = False
	while not valid:	
		if is_console: #determined on load
			is_coloured = True # assume colour 
			clear()
			print("This program uses coloured text and formatted menus")
			print("This can only be seen when run in terminal or IDEs with ansi console:")
			print("(Visual Studio Code or Wing Personal with I/O set to external console)")			
			print()
			print(f"The terminal has been set to {window_width} x {window_height} with {fore_color} text on {back_color} background.")
			if os.name == 'nt': # Windows cmd
				print()
				print("If the font size is too small:")
				print()
				print("\t1) Right-click on the title bar and select 'Properties'")
				print("\t2) Select the 'Font' tab")
				print("\t3) Change the size to suit")
				print("\t4) Click 'Close' (The window will resize)")
				print()
			else:
				print()
				print("If the font size is too small:")
				print()
				print("\t1) Menu -> Edit -> Preferences")
				print("\t2) Select the 'Text' tab")
				print("\t3) Change the 'Size' to suit")
				print("\t4) Click 'OK' (The window will resize)")
				print("\t5) Repeat steps 1 and 4 if you change window position")
			print() #14
			colorprint("Do ~red~NOT~white~ resize this window as it will mess up the menus!")
			add_lines(5) #line 19
		else:
			print(" 1 This program uses coloured text and formatted menus\n 2")
			print(" 3 This can only be seen when run in terminal or IDEs with ansi console:")
			print(" 4 (Visual Studio Code or Wing Personal with I/O set to external console)")			
			print(" 5\n 6 Important!")
			print(" 6\n 7 A line of characters has been drawn on line 24 below")
			print(" 8 Resize the output window so you can see lines 1 to 25 only")
			print(" 9 Follow the instruction on line 25")
			for i in range(10,24):
				print(f"{i}")
			print("24 ", end ='')
			draw_line('d', white, blackbg, window_width-3) #line 24
			input("25 Enter to continue")
		if is_console:
			draw_line('d', red, blackbg)
			valid, user_input, message = get_boolean("Is the line above red on a black background? (y/n)", '_')
			if valid:
				is_coloured = user_input # User entered True/False
			else:
				colorprint(f"{red}{message}{magenta} retry in 2 secs...")
				time.sleep(2)	
		else:
			valid = True

	clear()
	if is_console:
		if not is_coloured:
			print("You are running from a non-compliant IDE\n")
			print("Coloured text will NOT be displayed\n")
			print("The game will still run!\n")
			if os.name == 'nt': # Windows cmd
				print("Try double-clicking 'program.py' in Windows Explorer")
				print("Or running 'python program.py' in cmd or powershell")
			else:
				print("Try typing 'python3 program.py' in terminal\n")
			print("(make sure you are in the correct directory!)")
			add_lines(14)
			draw_line('d', white) #line 21
			input("Press Enter to continue")
		clear()

def draw_box_body(style, text, box_align, fore_color, back_color, text_color = white, text_back_color = blackbg, text_align = "left", width = 0):
	''' print out single line body section of a box with text / spaces "║  text  ║"  '''
	style = fix_style(style)
	fore_color, back_color = validate_colors(fore_color, back_color)         # true = colours validated to const format: ~white~
	text_color, text_back_color = validate_colors(text_color, text_back_color)     # true = colours validated to const format: ~'blackbg'~
	box_align = validate_alignment(box_align)                            # check alignments are in permitted list
	text_align = validate_alignment(text_align)
	s = select_character_list("body", style)        # { "║", " ", "║", "║" };
	if (width > window_width or width <= 0):
		width = window_width
	output = pad_string(text, width - 2, " ", text_align)  # "  text  " -2 to allow for start/end margin chars
	sides = [ s[0], s[2] ]
	sides = pad_box_sides(sides, output, box_align)
	# fore_color border on back_color -> colour formatted text -> fore_color border on back_color
	colorprint(f"{fore_color}{back_color}{sides[0]}{text_color}{text_back_color}{output}{fore_color}{back_color}{sides[1]}")

	return 1 # single line used	

def draw_box_outline(style, part, fore_color, back_color, box_align = "left", width = 0, midMargin = False):
	''' Draw the top, mid or bottom of a box to width '''
	style = fix_style(style)
	fore_color, back_color = validate_colors(fore_color, back_color)                  # true = colours validated to const format: ~'white'~
	box_align = validate_alignment(box_align)
	part = validate_box_part(part)
	sides = [ "", "" ]
	s = select_character_list(part, style)
	if width > window_width or width <= 0:
		width = window_width
	sides[0] = s[0]                                            # start with left corner
	sides[1] = s[2]                                            # end with right corner
	if midMargin:
		sides[0] = select_character_list("mid", style)[0]        # "├"
		sides[1] = select_character_list("mid", style)[2]        # "┤"
	output = pad_string("", width - 2, s[1], box_align)          # -2 to allow for start/end margin chars
	sides = pad_box_sides(sides, output, box_align)
	# line padded, now do same for spaces around the line
	output = f"{fore_color}{back_color}{sides[0]}{output}{fore_color}{back_color}{sides[1]}"
	colorprint(output)

	return 1 # single line used

def draw_line(style, fore_color, back_color, width = 0, align = 'left'):
	''' Draw a single or double line to specified length and alignment '''
	style = fix_style(style)
	fore_color, back_color = validate_colors(fore_color, back_color)
	align = validate_alignment(align)
	if width > window_width or width <= 0:
		width = window_width;

	s = select_character_list("mid", style)
	output = ''
	if width == window_width:
		output = pad_string("", width, s[1], "left")     # -2 to allow for start/end margin chars
		output = f"{fore_color}{back_color}{output}"    # eg "~'white'~~'blackbg'~════════════════════"
	else:
		output = pad_string("", width, s[1], "left")
		output = pad_string(output, window_width, " ", align)
		output = f"{fore_color}{back_color}{output}"           #eg "~'white'~~'blackbg'~════════════════════"
	colorprint(output)

	return 1 # single line used	

def draw_multi_box_body(styles, sizes, fore_colors, back_colors, text_lines, alignments, padding = 0):
	''' print out single line mid section of multiple boxes with or without text '''
	if(len(styles) != len(sizes) and len(styles) != len(fore_colors) and len(styles) != len(back_colors) and len(styles)!= len(alignments)):
		raise MatchingTagsException("All supplied parameter lists must have the same number of items")
	for i in range(len(styles)):
		styles[i] = fix_style(styles[i])

	if len(fore_colors) != len(back_colors):
		raise color_value_exception("colour list error", f"DrawMultiBoxOutline: Number of foreColours must equal number of backColours")
	for i in range(len(fore_colors)): #validate supplied colours
		fore_color = fore_colors[i]
		back_color = back_colors[i]
		validate_colors(fore_color, back_color)
		fore_colors[i] = fore_color
		back_colors[i] = back_color
	for i in range(len(alignments)):
		align = alignments[i]
		align = validate_alignment(align)
		alignments[i] = align

	s = s_symbols_body #default
	outputs = []
	# calculate each box size from sizes: {15, 40, 25} 
	box_length = 0
	output = ''
	for i in range(len(sizes)):
		# size examples {15, 40, 25} = 80 cols
		s = select_character_list("body", styles[i])
		if i < len(sizes)- 1:
			box_length = sizes[i] - padding - 2;    # -2 as is box edge, and characters will be added both sides
		else:
			box_length = sizes[i] - 2
		l_side = s[0]                                                # start with left side char
		r_side = s[3]                                                # end with right side char
		#check length of string
		output = text_lines[i]
		color_tag_spaces, text, color_list = format_color_tags(output)
		if len(output) > sizes[i] - 2 + color_tag_spaces:
			output = output[0: sizes[i] - 2 + color_tag_spaces]
		output = pad_string(output, box_length, " ", alignments[i])
		output = f"{fore_colors[i]}{back_colors[i]}{l_side}{output}{fore_colors[i]}{back_colors[i]}{r_side}"
		outputs.append(output)                                  # create new list item with completed string

	output = ""
	for line in outputs:                        # concatenate all box outlines in outputs
		output += line
	colorprint(output)

	return 1; # single line used

def draw_multi_box_outline(styles, part, sizes, fore_colors, back_colors, padding = 0):
	''' Draw the top/bottoms of sizes.Count boxes, width in absolute values '''
	if len(styles) != len(sizes) and len(styles) != len(fore_colors) and len(styles) != len(back_colors):
		raise MatchingTagsException("List size error", "All supplied parameter lists must have the same number of items")
	for i in range(len(styles)):
		styles[i] = fix_style(styles[i])
	for i in range(len(fore_colors)):
		fore_color = fore_colors[i]
		back_color = back_colors[i]
		fore_color, back_color = validate_colors(fore_color, back_color)
		fore_colors[i] = fore_color
		back_colors[i] = back_color
	s = s_symbols_top
	outputs =[]
	box_length = 0
	output = ''
	for i in range(len(sizes)):
		# size examples {15, 40, 25} = 80 cols
		s = select_character_list(part, styles[i])
		if i < len(sizes) - 1:
			box_length = sizes[i] - padding - 2     # -2 as is box edge, and characters will be added both sides
		else:
			box_length = sizes[i] - 2
		l_side = s[0]                                                # start with left corner
		r_side = s[2]                                               # end with right corner
		output = pad_string("", box_length, s[1], "left")
		output = f"{fore_colors[i]}{back_colors[i]}{l_side}{output}{fore_colors[i]}{back_colors[i]}{r_side}"
		outputs.append(output)        # create new list item with completed string

	output = ''
	for line in outputs: # concatenate all box outlines in outputs
		output += line
	colorprint(output)

	return 1 #single line

def draw_grid_body(style, part, columns, box_color, box_back_color, text_color, text_back_color, text_lines, alignments):
	''' Draw the body of a grid to width '''
	style = fix_style(style)
	box_color, box_back_color = validate_colors(box_color, box_back_color)           # true = colours validated to const format: ~'white'~
	text_color, text_back_color, = validate_colors(text_color, text_back_color)         # true = colours validated to const format: ~'white'~
	s = select_character_list(part, style)              # "┌", "─", "┐", "┬"
	outputs = []
	output = ''
	for i in range(len(columns)):
		col_width = columns[i]                                # eg {10, 20, 20, 30 } = 80 cols
		l_side = s[0]                                       # "┌"
		r_side = s[2]                                        # "┐"
		if i == 0:
			l_side = s[0];                                           # "┌"
			r_side = s[3];                                           # "┬"

		elif i == len(columns)- 1:
			l_side = s[1];                                           # "─"
			r_side = s[2];                                           # "┐"
		else:
			l_side = s[1];                                           # "─"
			r_side = s[3];                                           # "┬"
		text = "";
		if i < len(text_lines):
			text = text_lines[i];
		output = pad_string(text, col_width - 2, " ", alignments[i]);          # -2 to allow for start/end margin chars
		output = f"{box_color}{box_back_color}{l_side}{text_color}{text_back_color}{output}{box_color}{box_back_color}{r_side}";
		outputs.append(output);                                        # create new list item with completed string
	output = ''
	for line in outputs: # concatenate all box outlines in outputs
		output += line

	colorprint(output)

	return 1 # single line used

def draw_grid_outline(style, part, columns, fore_color, back_color, midMargin = False):
	''' Draw the top, mid or bottom of a grid to width '''
	style = fix_style(style);
	fore_color, back_color = validate_colors(fore_color, back_color);             # true = colours validated to const format: ~'white'~
	s = select_character_list(part, style)              # "┌", "─", "┐", "┬"
	outputs = []
	output = ''
	for col in range(len(columns)):
		col_width = columns[col]                                # eg {10, 20, 20, 30 } = 80 cols
		l_side = s[0]                                       # "┌"
		r_side = s[2]                                        # "┐"
		if col == 0:
			l_side = s[0]                                           # "┌"
			if midMargin:
				l_side = select_character_list("mid", style)[0] # "├"
			r_side = s[3]                                           # "┬"
		elif col == len(columns) - 1:
			l_side = s[1]                                           # "─"
			r_side = s[2]                                           # "┐"
			if (midMargin):
				r_side = select_character_list("mid", style)[2] # "├"
		else:
			l_side = s[1]                                           # "─"
			r_side = s[3]                                           # "┬"
		output = pad_string("", col_width - 2, s[1], "left")         # -2 to allow for start/end margin chars
		output = f"{fore_color}{back_color}{l_side}{output}{r_side}"
		outputs.append(output);                                        # create new list item with completed string
	output = ''
	for line in outputs: # concatenate all box outlines in outputs
		output += line
	colorprint(output)

	return 1 # single line used

def draw_multi_line_box(style, text_lines, fore_color, back_color, text_color = "white", text_back_color = "blackbg", box_align = "left", text_align = "left", width = 0):
	'''  Draw a single box containing many lines of text '''
	if not isinstance(text_lines, list):
		text_lines = split_clean(text_lines, "\n")
	num_lines = 0
	style = fix_style(style)
	fore_color, back_color = validate_colors(fore_color, back_color)
	text_color, text_back_color = validate_colors(text_color, text_back_color)
	if width > window_width or width <= 0:
		width = window_width;
	num_lines += draw_box_outline(style, "top", fore_color, back_color, box_align, width)
	text_lines = get_formatted_lines(text_lines, width)
	for line in text_lines:
		num_lines += draw_box_body(style, line, box_align, fore_color, back_color, text_color, text_back_color, text_align, width)
	num_lines += draw_box_outline(style, "bottom", fore_color, back_color, box_align, width)

	return num_lines


def fix_style(style):
	''' checks developer has entered correct style choice '''
	style = style.lstrip().rstrip().lower()
	if style != "s" and style != "d":
		style = "s"

	return style

def format_color_tags(text):
	''' corrects in-line colour tags eg ~red~ ~blackbg~ '''
	color_list = []
	if text.count(sep) % 2 == 1: # check ~red~ not red~ or ~red
		raise MatchingTagsException("Matching tags error", f"The supplied text {text} does not have matching colour separators: {sep}")
	text = text.replace(sep, "¶" + sep + "¶") # "~red~some text~green~more text" -> "¶~¶red¶~¶some text¶~¶green¶~¶more text"
	data = split_clean(text, "¶") # {"~", "red", "~", "some text", "~","green", "~", "more text"}
	color_tag_spaces = 0
	start_tag = -1
	end_tag = -1
	color_data = -1
	for i in range(len(data)):
		if data[i] == sep: # found ~
			color_tag_spaces += 1
			if start_tag == -1:
				start_tag = i;
				color_data = i + 1;
				end_tag = i + 2;
			elif i == end_tag: #marked already, next data is normal text
				color_data = -1;
			else: # i not -1 and not end_tag
				start_tag = i;
				color_data = i + 1;
				end_tag = i + 2;		
		else:
			if i == color_data:
				# convert "~reD~" to "~red~"
				textColour = data[i].lower()
				if textColour in colors:
					#data[i] = colors[textColour]
					color_tag_spaces += len(data[i])
					color_list.append(data[i])
				color_data = -1

	# re-combine text_lines
	output = ''
	for line in data:
		output += line

	return color_tag_spaces, output, color_list

def get_formatted_lines(text_lines, max_length = 0, noBorder = False):
	'''takes a list of lines , checks length of each and adds additional lines if required, returns list'''
	if not isinstance(text_lines, list):
		text_lines = split_clean(text_lines, "\n")	
	# check length of each line max = shared.term_width - 2

	if max_length > window_width or max_length <= 0:
		max_length = window_width
	if not noBorder:
		max_length -= 2 #default    
	new_lines = []
	for index in range(len(text_lines)):   # 3 lines in this example as contains  2 * \n
		line = text_lines[index].lstrip().rstrip()              # remove leading/trailing spaces
		color_tag_spaces = 0
		# now check the length of each line and cut into shorter sections if required
		if len(line) == 0:
			new_lines.append(line) # add empty
		else:
			while len(line) > max_length + color_tag_spaces:                 # line length > 77 in 80 col terminal
				text = get_max_length_string(line, max_length)
				new_lines.append(text)
				line = line[len(text):].rstrip().lstrip()				
			if len(line) > 0:
				new_lines.append(line)        # partial line left over from the while loop ( <max_length) or short line
	return new_lines

def get_max_length_string(text, max_length):
	''' takes a line of text and chops it to suitable lengths to fit in the console without breaking words '''
	colorTagSpaces, output, colorTagList = format_color_tags(text)
	if len(text) > max_length + colorTagSpaces:
		text = text[0: max_length + colorTagSpaces]
		ending = text.rindex(" ")
		text = text[0: ending]
	return text.lstrip().rstrip()

def get_input(prompt, prompt_end, fore_color, back_color):
	''' Get keyboard input from user (requires Enter ) '''
	fore_color, back_color = validate_colors(fore_color, back_color)
	# check if prompt contains embedded colours
	color_tag_spaces, prompt, embeddedColors = format_color_tags(prompt)
	if color_tag_spaces > 0: #use built in colours
		colorprint(f"{prompt + prompt_end}", False); #do not use newline
	else: # use supplied or default colors
		colorprint(f"{fore_color}{back_color}{prompt + prompt_end}", False); #do not use newline
	return input()

def get_boolean(prompt, prompt_end, text_color = 'white', back_color = 'blackbg'):
	''' gets a boolean (yes/no) type entries from the user '''
	text_color, back_color = validate_colors(text_color, back_color)
	valid, user_input, message =  process_input(prompt, prompt_end, text_color, back_color, 1, 3, "bool")
	return valid, user_input, message

def get_integer(prompt, prompt_end, text_color = 'white', back_color = 'blackbg', min = 0, max = 65536): # min and max can be over-ridden by calling code
	''' Public Method: gets an integer from the user '''
	text_color, back_color = validate_colors(text_color, back_color)
	valid, user_input, message =  process_input(prompt, prompt_end, text_color, back_color, min, max, "int")		
	return valid, user_input, message

def get_real_number(prompt, prompt_end, text_color = 'white', back_color = 'blackbg', min = -1000000.0, max = 1000000.0): # min and max can be over-ridden by calling code
	''' Public Method: gets a real number from the user '''
	text_color, back_color = validate_colors(text_color, back_color)
	valid, user_input, message =  process_input(prompt, prompt_end, text_color, back_color, min, max, "real")	
	return valid, user_input, message

def get_string(prompt, prompt_end, text_color = 'white', back_color = 'blackbg', with_title = False, min = 0, max = 20): # with_title, min and max can be over-ridden by calling code
	''' Public method: Gets a string from the user, with options for Title Case, length of the string. Set min to 0 to allow empty string return '''
	text_color, back_color = validate_colors(text_color, back_color)
	valid, user_input, message =  process_input(prompt, prompt_end, text_color, back_color, min, max, "string")	

	if with_title and valid:
		user_input = to_title(user_input)

	return valid, user_input, message

def initialise():
	''' runs on load to create lists/dictionaries of colour variables '''
	global window_width, window_height, colors, is_console
	try:
		window_width = os.get_terminal_size().columns # this will fail if NOT in a console
		window_height = os.get_terminal_size().lines # this will fail if NOT in a console
	except:
		window_width = 80
		window_height = 25
		is_console = False
	
	colors.clear()
	colors.update({"black":BLACK})
	colors.update({"grey": GREY})
	colors.update({"gray": GRAY})
	colors.update({"dgrey": DGREY})
	colors.update({"dgray": DGRAY})
	colors.update({"white": WHITE})
	colors.update({"blue": BLUE})
	colors.update({"green": GREEN})
	colors.update({"cyan": CYAN})
	colors.update({"red": RED})
	colors.update({"magenta": MAGENTA})
	colors.update({"yellow": YELLOW})
	colors.update({"dblue": DBLUE})
	colors.update({"dgreen": DGREEN})
	colors.update({"dcyan": DCYAN})
	colors.update({"dred": DRED})
	colors.update({"dmagenta": DMAGENTA})
	colors.update({"dyellow": DYELLOW})
	colors.update({"whitebg": WHITEBG})
	colors.update({"blackbg": BLACKBG})
	colors.update({"greybg": GREYBG})
	colors.update({"graybg": GRAYBG})
	colors.update({"dgreybg": DGREYBG})
	colors.update({"dgraybg": DGRAYBG})
	colors.update({"bluebg": BLUEBG})
	colors.update({"greenbg": GREENBG})
	colors.update({"cyanbg": CYANBG})
	colors.update({"redbg": REDBG})
	colors.update({"magentabg": MAGENTABG})
	colors.update({"yellowbg": YELLOWBG})
	colors.update({"dbluebg": DBLUEBG})
	colors.update({"dgreenbg": DGREENBG})
	colors.update({"dcyanbg": DCYANBG})
	colors.update({"dredbg": DREDBG})
	colors.update({"dmagentabg": DMAGENTABG})
	colors.update({"dyellowbg": DYELLOWBG})
	colors.update({"reset": RESET})

	colors.update({f"{sep}black{sep}":BLACK})
	colors.update({f"{sep}grey{sep}": GREY})
	colors.update({f"{sep}gray{sep}": GRAY})
	colors.update({f"{sep}dgrey{sep}": DGREY})
	colors.update({f"{sep}dgray{sep}": DGRAY})
	colors.update({f"{sep}white{sep}": WHITE})
	colors.update({f"{sep}blue{sep}": BLUE})
	colors.update({f"{sep}green{sep}": GREEN})
	colors.update({f"{sep}cyan{sep}": CYAN})
	colors.update({f"{sep}red{sep}": RED})
	colors.update({f"{sep}magenta{sep}": MAGENTA})
	colors.update({f"{sep}yellow{sep}": YELLOW})
	colors.update({f"{sep}dblue{sep}": DBLUE})
	colors.update({f"{sep}dgreen{sep}": DGREEN})
	colors.update({f"{sep}dcyan{sep}": DCYAN})
	colors.update({f"{sep}dred{sep}": DRED})
	colors.update({f"{sep}dmagenta{sep}": DMAGENTA})
	colors.update({f"{sep}dyellow{sep}": DYELLOW})
	colors.update({f"{sep}whitebg{sep}": WHITEBG})
	colors.update({f"{sep}blackbg{sep}": BLACKBG})
	colors.update({f"{sep}greybg{sep}": GREYBG})
	colors.update({f"{sep}graybg{sep}": GRAYBG})
	colors.update({f"{sep}dgreybg{sep}": DGREYBG})
	colors.update({f"{sep}dgraybg{sep}": DGRAYBG})
	colors.update({f"{sep}bluebg{sep}": BLUEBG})
	colors.update({f"{sep}greenbg{sep}": GREENBG})
	colors.update({f"{sep}cyanbg{sep}": CYANBG})
	colors.update({f"{sep}redbg{sep}": REDBG})
	colors.update({f"{sep}magentabg{sep}": MAGENTABG})
	colors.update({f"{sep}yellowbg{sep}": YELLOWBG})
	colors.update({f"{sep}dbluebg{sep}": DBLUEBG})
	colors.update({f"{sep}dgreenbg{sep}": DGREENBG})
	colors.update({f"{sep}dcyanbg{sep}": DCYANBG})
	colors.update({f"{sep}dredbg{sep}": DREDBG})
	colors.update({f"{sep}dmagentabg{sep}": DMAGENTABG})
	colors.update({f"{sep}dyellowbg{sep}": DYELLOWBG})	

def input_box(style, return_type, title, box_message, input_prompt, prompt_end, fore_color = white, back_color = blackbg, width = 0, min_return_len = 1, max_return_len = 20, with_title = False):
	''' Draw an inputBox with title, message, input area
	Example "bool", "File Exists Warning", "Are you sure you want to over-write?", "Confirm over-write (y/n)_" '''
	style = fix_style(style)
	fore_color, back_color = validate_colors(fore_color, back_color); # true = colours validated to const format: ~'white'~
	if (width > window_width or width <= 0):
		width = window_width
	valid = False
	user_input = ""
	while not valid:
		clear();
		lines = get_formatted_lines(box_message); # returns alist of lines max length of any line Console.window_width - 3
		num_lines = draw_box_outline(style, "top", fore_color, back_color, "centre", width); # draw top of box double line, yellow
		num_lines += draw_box_body(style, f"{title}", "centre", fore_color, back_color, fore_color, back_color, "centre", width); # draw title
		num_lines += draw_box_outline(style, "mid", fore_color, back_color, "centre", width); # draw single line
		for line in lines:
			num_lines += draw_box_body(style,  f"{line}", "centre", fore_color, back_color, fore_color, back_color, "left", width); # draw each line of text
		num_lines += draw_box_body(style, "", "centre", fore_color, back_color, fore_color, back_color, "centre", width); # draw empty line
		num_lines += draw_box_outline(style, "bottom", fore_color, back_color, "centre", width); # draw bottom of box double line, yellow
		add_lines(5, num_lines)
		draw_line("d", white, blackbg)
		if return_type == "str" or return_type == "string":
			valid, user_input, message = get_string(input_prompt, prompt_end, fore_color, back_color, with_title , min_return_len, max_return_len)
		elif (return_type == "int"):
			valid, user_input, message = get_integer(input_prompt, prompt_end)
		elif (return_type == "real" or return_type == "float" or return_type == "double"):
			valid, user_input, message = get_real_number(input_prompt, prompt_end)
		elif (return_type == "bool" or return_type == "boolean"):
			valid, user_input, message = get_boolean(input_prompt, prompt_end)

		if not valid:
			colorprint(f"{red}{message}{magenta} retry in 2 secs...");
			time.sleep(2)
	return user_input # string eg filename typed in, || bool

def menu(style, title, prompt_end, text_lines, fore_color = 'white', back_color = blackbg, align = "left", width = 0):
	''' displays a menu using the text in 'title', and a list of menu items (string)
		This menu will re-draw until user enters correct data '''
	style = fix_style(style)
	fore_color, back_color, = validate_colors(fore_color, back_color)                  # true = colours validated to const format: ~'white'~
	if width > window_width or width <= 0:
		width = window_width
	user_input = 0;
	is_valid = False;
	message = ""

	for i in range(len(text_lines)):
		if i < 9:
			text_lines[i] = f"     {i + 1}) {text_lines[i]}"
		else:
			text_lines[i] = f"    {i + 1}) {text_lines[i]}"
	while not is_valid:
		clear()
		num_lines = draw_box_outline(style, "top", fore_color, back_color)           # draw top of box double line
		num_lines += draw_box_body(style, "", "centre", fore_color, back_color)       # draw empty line
		num_lines += draw_box_body(style, f"{title}", "left", fore_color, back_color) # draw title
		num_lines += draw_box_body(style, "", "centre", fore_color, back_color)       # draw empty line
		for i in range(len( text_lines)):
			num_lines += draw_box_body(style, f"{text_lines[i]}", "left", fore_color, back_color) # draw menu options
		num_lines += draw_box_body(style, "", "centre", fore_color, back_color);       # draw empty line
		num_lines += draw_box_outline(style, "bottom", fore_color, back_color);        # draw top of box double line, yellow
		add_lines(5, num_lines);
		draw_line("d", white, blackbg);
		is_valid, user_input, message = get_integer(f"Type the number of your choice (1 to {len(text_lines)})", prompt_end, 'white', 'blackbg', 1, len(text_lines));
		if not is_valid:
			colorprint(f"{red}{message}{magenta} retry in 2 secs...")
			time.sleep(2)

	return user_input - 1

def pad_box_sides(sides, body, box_align):
	''' works on the characters used to draw box sides, padding to correct alignment '''
	if box_align == "left": #pad r_side 
		length = window_width - len(body) - 2 # 80 - 78 - 2 = 0
		if length > 0:
			sides[1] = pad_string(sides[1], length, " ", "right")    # "║    "
	elif box_align == "right": #pad l_side 
		length = window_width - len(body) - 2 # 80 - 78 - 1 = 1
		if length > 0:
			sides[0] = pad_string(sides[0], window_width - len(body) - 1, " ", "left")     # "    ║"
	else: # centre
		color_tag_spaces, text, color_list = format_color_tags(body) #extract any colour info from body eg ~red~);
		length = window_width - len(body) - 2 + color_tag_spaces # 80 - 78 - 2 = 0
		if length >= 2:
			sides[0] = pad_string(sides[0], length // 2, " ", "right")
			length = window_width - len(body) - len(sides[0]) + color_tag_spaces
			if length > 0:
				sides[1] = pad_string(sides[1], length, " ", "left")
	return sides

def pad_string(text, width, pad_char, align = "left"):
	''' width should be width of the part to be padded, so excludes left/right margin characters '''
	output = text
	color_tag_spaces = 0
	if sep in text: # colour tag(s) present
		color_tag_spaces, text, color_list = format_color_tags(output) #extract any colour info from output eg ~red~ returns additional spaces required and fomats output by ref
	if align == "centre" or align == "center":
		output = output.ljust(((width - len(output) + color_tag_spaces) // 2) + len(output), pad_char) #eg output 10 chars long, pad to half of width - 2 and allow for chars used by colour tag
		output = output.rjust(width + color_tag_spaces, pad_char)
	elif align == "right":
		output = output.rjust(width + color_tag_spaces, pad_char) # right align = .PadLeft in C#
	else: #left align = PadRight
		output = output.ljust(width + color_tag_spaces, pad_char)  #eg output 10 chars long, pad to width - 2 and allow for chars used by colour tag

	return output

def print_line(text, text_colour, back_colour):
	''' basic line printing statement '''
	text_color, back_color = validate_colors(text_color, back_color)
	colorprint(f'{text_colour}{back_colour}{text}')

def print_message(message, delay, message_color = red, delay_color = magenta):
	''' basic message disply with timer '''
	dummy = 'blackbg'
	message_color, dummy = validate_colors(message_color, dummy)
	delay_color, dummy = validate_colors(delay_color, dummy)
	colorprint(f'{message_color}{message}')
	colorprint(f'{delay_color}Retry in {delay} secs...')
	time.sleep(delay)

def process_input(prompt, prompt_end, text_color, back_color, min, max, data_type):
	''' This function is not called directly from other files. Python does not have a 'Private' keyword'''
	data_type = data_type.lower()
	message = ''
	valid = False
	user_input = get_input(prompt, prompt_end, text_color, back_color)
	if data_type[:3] == 'str':
		if len(user_input) == 0 and min > 0:
			message = "Just pressing the Enter key doesn't work..."
		elif len(user_input) > max:
			message = f"Try entering between {min} and {max} characters..."
		else:
			valid = True
	else: #integer, float, bool
		if data_type[:4] == "bool":
			if user_input[:1].lower() == "y":
				user_input = "True"
				valid = True
			elif user_input[:1].lower() == "n":
				user_input = "False";
				valid = True;
			else:
				message = "Only anything starting with y or n is accepted...";
		else: # int, real
			if data_type[:3] == "int":
				try:
					user_input = int(user_input)
					if user_input >= min and user_input <= max:
						valid = True
					else:
						message = f"Try a number from {min} to {max}..."
				except:
					message = ""
			elif data_type == "real" or data_type == "float":
				try:
					user_input = float(user_input)
					if user_input >= min and user_input <= max:
						valid = True
					else:
						message = f"Try a number from {min} to {max}..."
				except:
					message = ""
			if not valid and message == "":
				if user_input == "":
					message = "Try entering a number: 'Enter' does not work..."
				else:
					if data_type == "int":
						message = f"Try entering a whole number: {user_input} cannot be converted..."
					else:
						message = f"Try entering a decimal number: {user_input} cannot be converted..."			

	return valid, user_input, message

def quit(withConfirm = True):
	if withConfirm:
		input("Press Enter to quit")

def reset_separator():
	sep = "~"
	initialise()
			
def resize(window_width, window_height):
	if is_console:
		if os.name == 'nt':
			os.system(f'mode {window_width},{window_height}')
		else:    
			cmd = f"'\\e[8;{window_height};{window_width}t'"
			os.system("echo -e " + cmd) 
		clear()
def	select_character_list(part, style):
	''' select correct character list depending on style and part '''
	s = s_symbols_top
	if part == "top":             # 0 1 2 3 <- index
		s = s_symbols_top         # ┌ ─ ┐ ┬
		if style == "d":
			s = d_symbols_top     # ╔ ═ ╗ ╦

	elif part == "mid":
		s = s_symbols_mid         # ├ ─ ┤ ┼
		if (style == "d"):
			s = d_symbols_mid     # ╠ ═ ╣ ╬
	elif part == "bottom":
		s = s_symbols_bottom      # └ ─ ┘ ┴ 
		if (style == "d"):
			s = d_symbols_bottom  # ╚ ═ ╝ ╩
	elif part == "body":
		s = s_symbols_body        # └ ─ ┘ ┴ 
		if (style == "d"):
			s = d_symbols_body    # ╚ ═ ╝ ╩
	return s

def set_console(cols, rows, fore_color, back_color, initialise = False):
	global window_width, window_height
	'''
	In Windows the default terminal color is COLOR 07, white on black color bgfg
	Colour attributes are specified by 2 of the following hex digits. There should be no space between the two color numbers.
	Each digit can be any of the following values:
	0 = Black    1 = Blue       2 = Green       3 = Cyan       4 = Red       5 = magenta       6 = Yellow       7 = White
	8 = Gray     9 = Light Blue A = Light Green B = Light Aqua C = Light Red D = Light Purple E = Light Yellow F = Bright White
	'''
	windows = {
        'black':'0', 'red':'4',  'green':'2', 'yellow':'6',
        'blue':'1', 'magenta':'5',  'cyan':'3',  'white':'7',
		'grey' : '8', 'lightblue' : '9', 'lightgreen' : 'A', 'lightaqua' : 'B',
		'lightred' : 'C', 'lightpurple' : 'D', 'lightyellow' : 'E', 'brightwhite' : 'F'		
    }
	linux_fg = {
        'black':'30', 'red':'31',  'green':'32', 'yellow':'33',
        'blue':'34', 'magenta':'35',  'cyan':'36',  'white':'37'
    }
	linux_bg = {
        'black':'40', 'red':'41',  'green':'42', 'yellow':'43',
        'blue':'44', 'magenta':'45',  'cyan':'46',  'white':'47'
    }    
	# set the shared values for size and colours
	winwindow_width = cols 				# set global variable window_width
	window_height = rows				# set global variable window_height
	resize(window_width, window_height) # resize terminal using global window_height, window_width
	# set colours to global fore, back
	if is_console: #defined on module load
		if os.name == 'nt': # Windows 
			os.system(f'color {windows[back_color]}{windows[fore_color]}') # white on black preferred
		else: # Linux / Mac
			#send ansi codes directly to terminal
			fc = f"'\\e[{linux_fg[fore_color]}m'"
			bc = f"'\\e[1{linux_bg[back_color]}m'" # 1 = set bold. 22 = set normal        
			os.system("echo -e " + bc)
			os.system("echo -e " + fc)
			#reset()
		clear()
		
	if initialise:
		display_setup(fore_color, back_color)

def split_clean(string_to_split, sep_char):
	''' .split often gives empty array elements. This returns a list of non-empty strings '''
	ret_value = []
	temp = string_to_split.split(sep_char)
	for part in temp:
		if len(part) > 0 or sep_char == '\n': # allow empty elements if \n\n supplied to create blank lines
			ret_value.append(part)

	return ret_value;

def teletype(text, delay, fore_color = white, back_color = blackbg):
	'''This text prints out slowly'''
	#colorprint(f'{fore_color}{back_color}', False)
	print(f"{colors[fore_color]}{colors[back_color]}", end = '')
	for letter in text:
		sys.stdout.write(letter)
		sys.stdout.flush()
		time.sleep(delay)
	return 1

def validate_alignment(align):
	''' check and correct align strings, else error '''
	align = align.lstrip().rstrip().lower()
	check = ["left", "centre", "center", "right"]
	if not align in check:
		raise AlignException("Align Error", "Align parameter must be: 'left', 'centre', 'center', 'right'");
	return align

def validate_box_part(part):
	''' check and correct box part strings, else error '''
	part = part.lstrip().rstrip().lower()
	check = [ "top", "mid", "bottom", "body" ]
	if not part in check:
		raise BoxPartException("Part parameter must be: 'top', 'mid', 'bottom', 'body'")
	return part

def validate_colors(fore_color, back_color):
	''' Fore and back colours corrected
	    example: fore_color = 'white', back_color = 'black' or 'blackbg'
		fore_color, back_color = validate_colors(fore_color, back_color)
		return colors tagged with current separator (sep): a global variable default = ~
		return '~white~', '~blackbg~'
	'''
	modified_fore_color = fore_color.lower() # ReD -> red , ~RED~ -> ~red~
	modified_back_color = back_color.lower() # Black -> black , ~BLACK~ -> ~black~
	modified_fore_color = modified_fore_color.replace(sep, '')
	modified_back_color = modified_back_color.replace(sep, '')
	if not modified_fore_color in colors:
		raise ColorValueException("Colour tag error", f"foreground colour must match format 'white' or 'WhiTE' not {fore_color}")
	if not modified_back_color in colors:
		raise ColorValueException("Colour matching error", f"background colour must match format 'black' or 'bLACk' or' blackbg' not {back_color}")	

	modified_fore_color = f"{sep}{fore_color}{sep}" # add separators front and back
	if modified_back_color.endswith("bg"):
		modified_back_color = f"{sep}{back_color}{sep}"
	else:
		modified_back_color = f"{sep}{back_color}bg{sep}"

	return modified_fore_color, modified_back_color	

def to_title(input_text):
	''' Private Method: makes text into Title Case '''
	temp_list = list(input_text.lower())
	for index in range(len(temp_list)):
		if index == 0:
			temp_list[0] = temp_list[0].upper()
		elif temp_list[index - 1] == " ":
			temp_list[index] = temp_list[index].upper()

	return ''.join(temp_list)

initialise() # setup variables required for use
''' ColorConsole demo methods '''
def color_print_demo():
	clear()
	colorprint(WHITE + "WHITE + This line is white on black.")
	colorprint(GREY + "GREY + This line is grey on black.")
	colorprint(DGREY + "DGREY + This line is dark grey on black.")
	colorprint(BLUE + "BLUE + This line is blue on black.")
	colorprint(GREEN + "GREEN + This line is green on black.")
	colorprint(CYAN + "CYAN + This line is cyan on black.")
	colorprint(RED + "RED + This line is red on black.")
	colorprint(MAGENTA + "MAGENTA + This line is magenta on black.")
	colorprint(YELLOW + "YELLOW + This line is yellow on black.")
	colorprint(DBLUE + "DBLUE + This line is dark blue on black.")
	colorprint(DGREEN + "DGREEN + This line is dark green on black")
	colorprint(DCYAN + "DCYAN + This line is dark cyan on black.")
	colorprint(DRED + "DRED + This line is dark red on black.")
	colorprint(DMAGENTA + "DMAGENTA + This line is dark magenta on black.")
	colorprint(DYELLOW + "DYELLOW + This line is dark yellow on black.")
	colorprint(BLACK + WHITEBG + "BLACK + WHITEBG + This line is black on white.")
	colorprint(WHITE + "WHITE + This line is white, and now " + RED + " + RED + red on black.")
	colorprint(GREEN + REDBG + "GREEN + REDBG + This line is green " + RED + GREENBG + "RED + GREENBG +  on red.")
	colorprint(RED + GREENBG + "RED + GREENBG + This line is red" + GREEN + REDBG + " + GREEN + REDBG +  on green.")
	add_lines(5, 19)
	draw_line("d", 'white', 'blackbg')
	display_message("Press Enter to continue...", True, False)

def get_input_demo(demo_type, description):
	'''	Most UI operations should be done within this UI class
	Try to keep all I/O operations out of other classes
	This will make transfer of code to a GUI much easier    '''
	valid = False
	user_input = ''
	message = ''
	while not valid:
		clear()
		num_lines = draw_multi_line_box("s", description, "yellow", "black", "white", "black", "left")
		add_lines(5, num_lines) # pad Console to leave 5 empty lines
		draw_line("d", "white", "black") # now leaves 4 empty lines
		if demo_type == "string":
			# GetString(prompt, promptChar, textColor, backColor, withTitle, min, max)
			valid, user_input, message = get_string("get_string: Type your name (1-10 chars)", ">_", "green", "black", True, 1, 10)
		elif demo_type == "int" :
			valid, user_input, message = get_integer("get_integer: Type your age (5-100)", ">_", "cyan", "black", 5, 100)
		elif demo_type == "real":
			valid, user_input, message = get_real_number("get_real_number: Type your height in metres (0.5 to 2.0)", ">_", "magenta", "black", 0.5, 2)
		elif demo_type == "bool":
			valid, user_input, message = get_boolean("get_boolean: Is this library useful (y/n)?", ">_", "blue", "black")

		if message != '':
			display_message(message, False, True, "red", "black")

	return user_input

def game_play_game(secretNumber):
	guess = 0
	attempts = 0
	while guess != secretNumber:
		attempts = attempts + 1
		clear()
		user_input = input_box("s", "int", "~magenta~Guess The Number", "~cyan~See if you can guess the number",
			"Type your guess for the secret number,(1 to 100)", ">_", "white", "black", 60, 1, 100);
		guess = int(user_input)
		if guess > secretNumber:
			display_message(f"Sorry, your guess {guess} was too high", False, True, "magenta", "black", 3)
		elif guess < secretNumber:
			display_message(f"Sorry, your guess {guess} was too low", False, True, "cyan", "black", 3)

	return attempts

def game_show_ending(description):
	clear()
	numLines = draw_multi_line_box("s", description, "yellow", "black", "white", "black", "centre", "centre")
	numLines = numLines + add_lines(2)
	add_lines(5, numLines)
	draw_line("d", "white", "black")
	display_message("", True, False)

def game_show_intro(description, intro):
	clear()
	numLines = draw_multi_line_box("s", description, "yellow", "black", "white", "black", "centre", "center", 60)
	numLines = numLines + add_lines(2)
	intro = intro.rjust(((window_width - len(intro)) // 2) + len(intro))
	intro = intro.ljust(window_width)
	numLines = numLines + teletype(intro, .02, 'white', 'redbg')
	add_lines(5, numLines)
	draw_line("d", "white", "black")
	display_message("", True, False)

