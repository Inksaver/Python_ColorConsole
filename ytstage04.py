import os, sys, subprocess

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

# colorama foreColour constants
BLACK   = colorama.Fore.BLACK + colorama.Style.BRIGHT		# '\x1b[30m' \x1b = Hex 1B = 16 + 11 = 27 decimal: CHR$(27)
WHITE   = colorama.Fore.LIGHTWHITE_EX						# '\x1b[97m'
GREEN   = colorama.Fore.LIGHTGREEN_EX						# '\x1b[92m'
RED     = colorama.Fore.LIGHTRED_EX							# '\x1b[91m'
#backColour constants:
BLACKBG = colorama.Back.BLACK + colorama.Style.BRIGHT		# '\x1b[40m'
WHITEBG = colorama.Back.LIGHTWHITE_EX 						# '\x1b[107m'
RESET   = colorama.Style.RESET_ALL							# '\x1b[0m'

sep = '~'                                                   # default separator character
colors = {}                                                 # empty dictionary. Populate with keys corresponding to colour names

# much of the code here copy/pasted from C# so variable names are camelCase not snake_case
sSymbolsTop    = [ "┌", "─", "┐", "┬" ]
sSymbolsBottom = [ "└", "─", "┘", "┴" ]
sSymbolsBody   = [ "│", " ", "│", "│" ]
sSymbolsMid    = [ "├", "─", "┤", "┼" ]

dSymbolsTop    = [ "╔", "═", "╗", "╦" ]
dSymbolsBottom = [ "╚", "═", "╝", "╩" ]
dSymbolsBody   = [ "║", " ", "║", "║" ]
dSymbolsMid    = [ "╠", "═", "╣", "╬" ]

def clear():
	''' clears console using appropriate method for current platform'''
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

def colorprint(value, newline = True):
	''' This uses the default char ~ to separate colour strings
	It allows removal of colour commands if all output is sent with colour tags
	change the line:  sep = "~"  as required
	other possibles are ` (backtick) ¬ (?) any character you will not use
	example value = "~red~This is a line of red text"
	'''
	lineparts = value.split(sep) #if already formatted then this will remain as 1 line: "\x1b[92m\x1b[40mThis is green text on black background"
	for line in lineparts: # more than 1 part = text formatted with colour constants in tags "red","blackbg","This is a line of red text"
		#if line in color_list: #red, blackbg
		if line in colors: #red, blackbg
			if line == "reset":
				print(RESET, end='')
			else:
				print(colors[line], end = '')
		else:
			print(line, end='')
	if newline:
		if reset:
			print(f'{RESET}')
		else:
			print()
	else:
		if reset:
			print(f'{RESET}', end='')
		
def initialise():
	global colors
	colors.update({"black":BLACK})	              # colors["black"] = colorama.Fore.BLACK + colorama.Style.BRIGHT
	colors.update({"white": WHITE})
	colors.update({"green": GREEN})
	colors.update({"red": RED})
	colors.update({"blackbg": BLACKBG})
	colors.update({"whitebg": WHITEBG})
	# include keys for embedded colour tags in strings
	colors.update({f"{sep}black{sep}":BLACK})    # colors["~black~"] = colorama.Fore.BLACK + colorama.Style.BRIGHT
	colors.update({f"{sep}white{sep}":WHITE})
	colors.update({f"{sep}red{sep}":RED})
	colors.update({f"{sep}green{sep}":GREEN})
	colors.update({f"{sep}blackbg{sep}":BLACKBG})
	colors.update({f"{sep}whitebg{sep}":WHITEBG})
	
	colors.update({f"{sep}reset{sep}":RESET})	

def main():
	initialise()
	clear()
	#print(f'Hello{colorama.Fore.RED + colorama.Style.BRIGHT} Coloured {colorama.Fore.GREEN + colorama.Style.BRIGHT}World{colorama.Style.RESET_ALL}')
	#print(f"Hello{RED} Coloured {GREEN}World{RESET}") # same output using constants
	#colorprint("Hello~red~ Coloured ~green~World") # same output using embedded colour tags
	# draw a double full width box
	colorprint(f"{GREEN}{dSymbolsTop[0]}{''.ljust(78, dSymbolsTop[1])}{dSymbolsTop[2]}")
	colorprint(f"{GREEN}{dSymbolsBody[0]}{''.ljust(78, dSymbolsBody[1])}{dSymbolsBody[2]}")
	colorprint(f"{GREEN}{dSymbolsMid[0]}{''.ljust(78, dSymbolsMid[1])}{dSymbolsMid[2]}")
	colorprint(f"{GREEN}{dSymbolsBody[0]}{''.ljust(78, dSymbolsBody[1])}{dSymbolsBody[2]}")
	colorprint(f"{GREEN}{dSymbolsBottom[0]}{''.ljust(78, dSymbolsBottom[1])}{dSymbolsBottom[2]}")
	input("Enter to continue")

main()