
# Python program to explain os.get_terminal_size() method  

# importing os module  
import os 

def clear():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

def resize(rows, cols):
	if os.name == 'nt':
		os.system(f'mode {cols},{rows}')
	else:    
		cmd = f"'\\e[8;{rows};{cols}t'"
		#os.popen("echo -e " + cmd) 
		os.system("echo -e " + cmd) 
		

# Get the size of the terminal 
size = os.get_terminal_size() 
# Print the size of the terminal 
print(size)
resize(20, 100)
size = os.get_terminal_size() 
print(size) 
input("\nEnter to quit")