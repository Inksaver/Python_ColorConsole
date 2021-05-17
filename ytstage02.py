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
BLACK 	= colorama.Fore.BLACK + colorama.Style.BRIGHT		# '\x1b[30m' \x1b = Hex 1B = 16 + 11 = 27 decimal: CHR$(27)
WHITE 	= colorama.Fore.LIGHTWHITE_EX						# '\x1b[97m'
GREEN 	= colorama.Fore.LIGHTGREEN_EX						# '\x1b[92m'
RED 	= colorama.Fore.LIGHTRED_EX							# '\x1b[91m'
#backColour constants:
BLACKBG = colorama.Back.BLACK + colorama.Style.BRIGHT		# '\x1b[40m'
WHITEBG = colorama.Back.LIGHTWHITE_EX 						# '\x1b[107m'
RESET 	= colorama.Style.RESET_ALL							# '\x1b[0m'

def clear():
	''' clears console using appropriate method for current platform'''
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

def main():
	clear()
	print(f'Hello{colorama.Fore.RED + colorama.Style.BRIGHT} Coloured {colorama.Fore.GREEN + colorama.Style.BRIGHT}World{colorama.Style.RESET_ALL}')
	print(f"Hello{RED} Coloured {GREEN}World{RESET}") # same output using constants
	input("Enter to continue")

main()