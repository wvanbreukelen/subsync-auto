# I know, it is ugly code. But it works.

import subprocess
import shlex
import sys

print("Scanning folder " + sys.argv[1])

languages = ["nl", "en"]

import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def walk(path, ext):
	files = []
	for file in os.listdir(path):
		if file.endswith(ext):
			files.append(file)
	return files

def run_command(command):
    #FNULL = open(os.devnull, 'w')
    process = subprocess.Popen(shlex.split(command),  stderr=subprocess.PIPE, universal_newlines=True) #subprocess.PIPE
    while True:
	#output, error = process.communicate()
	#print("LOL2")
        output = process.stderr.readline()
	#output  = process.stderr.readline()
	#moreOutput = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
	    #pass
        if output and "%|" in output:
	    #pass
	    #print("\x1b[2K\r'")
	    #sys.stdout.write('1')
            sys.stdout.write('\r')
	    sys.stdout.write(bcolors.OKBLUE)
	    sys.stdout.write(output.strip())
	    sys.stdout.write(bcolors.ENDC)
            #print output
	    #sys.stdout.flush()
	if output and "offset seconds: " in output:
	   sys.stdout.write('\n')
	   printg("--> Subtitle offset: " + output.strip().split("offset seconds: ")[1])
	  

	#if error:
	#    print "MORE OUTPUT!" + moreOutput
	#    sys.stdout.flush()

	#if error:
	#    sys.stdout.write(error.strip())
	#    sys.stdout.flush()
    rc = process.poll()
    return rc

def printg(text):
	print(bcolors.OKGREEN + text + bcolors.ENDC)

def printw(text):
	print(bcolors.WARNING + "[!] " + text + bcolors.ENDC)

def printb(text):
	print(bcolors.OKBLUE + text + bcolors.ENDC)

if sys.argv[1] == "revert":
	pass

for root, dirs, files in os.walk(sys.argv[1]): 
	for file in files:
		if file.endswith(".mp4") or file.endswith(".mkv"):
                        path = os.path.join(root, file)
                        #$files.append(file)                                                                                                                                                                                               			#withoutExt 
                                                                                                                                                                                                                                                                                                                                         
			#print(withoutExt)

			filename = os.path.basename(path)
			folder = os.path.dirname(os.path.abspath(path))
			#print(folder)

			srtFiles = walk(folder, ".srt")

			size = len(srtFiles)
			printb("--> Input video file: 	" + file)

			for srtFile in srtFiles:
				size = size - 1
				#print("--> Input subtitle file: " + srtFile)
				#print("--> REMAINING ITEMS: " + str(size) + "(" + str(((size * 15) / 60)) + " minutes)") 
				#print(srtFile, filename.split('.'))
				isValid = False
				for language in languages:
					temp = srtFile.split('.' + language + '.srt')

					#print(temp)
					if len(temp) > 0:
						if temp[0] in file:
							isValid = True
	
				if isValid:
					#printg("--> Syncing subtitle: " + srtFile)
					if os.path.isfile(folder + "/old/" + srtFile + ".old"):
						printw("--> Already synced " + srtFile + "! Skipping...")
						continue
					printg("--> Syncing subtitle: " + srtFile)
					try:
						run_command("subsync \"" + path + "\" -i \"" + folder + "/" + srtFile + "\" -o \"" + folder + "/" + srtFile + ".SYNC\"")
						printb("--> Checking creation of: \"" + folder + "/" + srtFile + ".SYNC\"") 
						if os.path.isfile(folder + "/" + srtFile + ".SYNC"):
							printg("--> Creation verified")
							if not os.path.exists(folder + "/old"):
								printb("--> Creating 'old' directory...")
								os.makedirs(folder + "/old")
							printg("--> Renaming " + folder + "/" + srtFile + " to " + folder + "/old/" + srtFile + ".old")
							os.rename(folder + "/" + srtFile, folder + "/old/" + srtFile + ".old")

							os.rename(folder + "/" + srtFile + ".SYNC", folder + "/" + srtFile)
					except KeyboardInterrupt:
						exit(0)
					#except:
					#	print("Error while processing file: " + srtFile)
			sys.stdout.flush()
