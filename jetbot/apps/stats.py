# Written by SparkFun Electronics June 2019
# Author: Wes Furuya
# 
# *Shell scripts were taken from original jetbot stats.py code.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warrranty of
# MERCHANABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.

# You should have reciede a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/license>

import time
import qwiic_micro_oled
from jetbot.utils.utils import get_ip_address
import subprocess


# Default Address for Micro OLED
micro_oled_address=0x3D

# Screen Width
LCDWIDTH = 64

# Initialization
disp = qwiic_micro_oled.QwiicMicroOled(micro_oled_address)
disp.begin()
disp.scrollStop()
disp.setFontType(0) # Set Font
# Could replace line spacing with disp.getFontHeight, but doesn't scale properly

while True:
	# Checks Eth0 and Wlan0 Connections-------------------------
	a = 0
	b = 0
	c = 0

	
	# Check Ethernet
	try:
		eth = get_ip_address('eth0')
		if eth != None:
			a = a + 1

		#Check String Length
		if len(eth) > 10:
			
			# Find '.' to loop numerals
			while b != -1:
				x1 = LCDWIDTH - disp._font.width * (len(eth)-b)
				i = b+1
				b = eth.find('.', i)

	except Exception as e:
		print(e)
	
	# Check WiFi
	try:
		wlan = get_ip_address('wlan0')
		if wlan != None:
			a = a + 2

		#Check String Length
		if len(wlan) > 10:
			
			# Find '.' to loop numerals
			while c != -1:
				x2 = LCDWIDTH - disp._font.width * (len(wlan)-c)
				j = c+1
				c = wlan.find('.', j)

	except Exception as e:
		print(e)
	
	
	# Check Resource Usage--------------------------------------
	# Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-$
		
	# CPU Load
	cmd = "top -bn1 | grep load | awk '{printf \"%.1f%%\", $(NF-2)}'"
	CPU = subprocess.check_output(cmd, shell = True )
	
	# Memory Use
	cmd = "free -m | awk 'NR==2{printf \"%.1f%%\", $3*100/$2}'"
	Mem_percent = subprocess.check_output(cmd, shell = True )
	cmd = "free -m | awk 'NR==2{printf \"%.2f/%.1f\", $3/1024,$2/1024}'"
	MemUsage = subprocess.check_output(cmd, shell = True )
	
	# Disk Storage
	cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
	Disk_percent = subprocess.check_output(cmd, shell = True )
	cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%d\", $3,$2}'"
	DiskUsage = subprocess.check_output(cmd, shell = True )



	# Displays IP Address (if available)--------------------------------
	
	# Clear Display
	disp.clear(disp.PAGE)
	disp.clear(disp.ALL)
	
	#Set Cursor at Origin
	disp.setCursor(0,0)

	# Prints IP Address on OLED Display
	if a == 1:
		disp.print("eth0:")
		disp.setCursor(0,8)
		if b != 0:
			disp.print(str(eth[0:i]))
			disp.setCursor(x1,16)
			disp.print(str(eth[i::]))
		else:
			disp.print(str(eth))
		
	elif a == 2:
		disp.print("wlan0: ")
		disp.setCursor(0,8)
		if c != 0:
			disp.print(str(wlan[0:j]))
			disp.setCursor(x2,16)
			disp.print(str(wlan[j::]))
		else:
			disp.print(str(wlan))
		
	elif a == 3:
		disp.print("eth0:")
		disp.setCursor(0,8)
		if b != 0:
			disp.print(str(eth[0:i]))
			disp.setCursor(x1,16)
			disp.print(str(eth[i::]))
		else:
			disp.print(str(eth))
		
		disp.setCursor(0,24)
		disp.print("wlan0: ")
		disp.setCursor(0,32)
		if c != 0:
			disp.print(str(wlan[0:j]))
			disp.setCursor(x2,40)
			disp.print(str(wlan[j::]))
		else:
			disp.print(str(wlan))
		
	else:
		disp.print("No Internet!")
	
	disp.display()
	time.sleep(10) #Pause 10 sec
	disp.scrollStop() #Stops scrolling


	# Displays Resource Usage-------------------------------------------
	# ------------------------------------------------------------------

	# Percentage--------------------------------------------------------
	# Clear Display
	disp.clear(disp.PAGE)
	disp.clear(disp.ALL)

	#Set Cursor at Origin
	disp.setCursor(0,0)

	# Prints Percentage Use on OLED Display
	disp.print("CPU: " + str(CPU.decode('utf-8')))
	disp.setCursor(0,10)
	disp.print("Mem: " + str(Mem_percent.decode('utf-8')))
	disp.setCursor(0,20)	
	disp.print("Disk:  " + str(Disk_percent.decode('utf-8')))
	
	disp.display()
	time.sleep(7.5) #Pause 10 sec
	
	# Size--------------------------------------------------------------
	# Clear Display
	disp.clear(disp.PAGE)
	disp.clear(disp.ALL)

	#Set Cursor at Origin
	disp.setCursor(0,0)
	
	# Prints Capacity Use on OLED Display
	disp.print("Mem:")
	disp.setCursor(0,10)
	disp.print(str(MemUsage.decode('utf-8')) + "GB")
	disp.setCursor(0,20)
	disp.print("Disk:")
	disp.setCursor(0,30)
	disp.print("  " + str(DiskUsage.decode('utf-8')) + "GB")
	
	disp.display()
	time.sleep(7.5) #Pause 10 sec


