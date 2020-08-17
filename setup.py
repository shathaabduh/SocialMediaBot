import os
import time


if os.name == 'nt':
	os.system('cls')
else:
	os.system('clear')

print("\n[+] Installation Starting...")
time.sleep(5)

_ = os.system('pip install selenium bs4 --user')

print("\n\n[+] INSTALLATION COMPLETED...")

while 1:pass
