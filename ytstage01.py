import sys, subprocess

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

def main():
	print(f'Hello{colorama.Fore.RED + colorama.Style.BRIGHT} Coloured {colorama.Fore.GREEN + colorama.Style.BRIGHT}World{colorama.Style.RESET_ALL}')
	input("Enter to continue")

main()