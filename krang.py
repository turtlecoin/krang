#!/usr/bin/env python2
# MODULES
from sys import argv
import os.path

# GLOBAL VARIABLES
tfsecpath = './resources/tf/secret.auto.tfvars'

# Pretty Colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# WELCOME MESSAGE
print "Welcome to Krang"
print "----------------"
print "(Will pay TRTL for ASCII Art) NOTE: Speak to bakedminds)"

## FUNCTION 1 = PRE-REQS
def check_file_exists(filepath):
	print "Check if %s exists" % filepath
	## THIS WILL FAIL IF RAN USING ../../../ location traversing to execute Krang - Figure that out later - Works if ran using ./krang.pl
	## EXTEND THIS CHECKING TO OTHER FILES LATER
	if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
		print bcolors.OKGREEN + "File exists and is readable" + bcolors.ENDC # RETURN TO CONTINE, SETUP TO RUN SETUP
		return True
	else:
		print bcolors.WARNING + "File is missing" + bcolors.ENDC #RUN SETUP
		return False


def digitalocean_setup():
	## FUNCTION 2 = DIGITALOCEAN SETUP
	print bcolors.OKBLUE + "This is where to ask which provider to be used (future). Currently only using Digital Ocean. NEXT" + bcolors.ENDC
	DO_API = raw_input("Please provide an API key to access your Digital Ocean Environment.\n>")
	target = open(tfsecpath, "w+")
	target.write('do_token = "' + DO_API + '"')
	target.close()
	fcheck = open(tfsecpath, "r")
	print fcheck.read()
	fcheck.close()

if check_file_exists(tfsecpath) is False:
	digitalocean_setup()
else:
	print ("Jobs Done")


## DESIGN / SCRIPT FLOW / FUNCTIONS

## PRE-REQS and SETUP
## - Select Providers
## - Check if secret.auto.tfvars file exists
## - If NOT CREATE and populate
## - Do Network Tests (OPTIONAL)
## - import and incroporate terrform module or a way to create Terraform files


