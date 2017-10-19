#!/usr/bin/python

import os
import subprocess
import sys
import argparse

MAX_BRIGHTNESS = 150    # Highest brightness (there is no cap with xrandr)
MIN_BRIGHTNESS = 0      # Lowest brightness (0 means pitch black)

# Parser for command line options
parser = argparse.ArgumentParser()
actiongroup = parser.add_mutually_exclusive_group() 

actiongroup.add_argument('-set', metavar='percent', help='Sets brightness to the specified level.')
actiongroup.add_argument('-inc', metavar='percent', help='Increases brightness by the specified amount.')
actiongroup.add_argument('-dec', metavar='percent', help='Decreases brightness by the specified amount.')
actiongroup.add_argument('-get',action='store_true',help='Print out the current backlight brightness of each output with such a control. The brightness is represented as a percentage of the maximum brightness supported. ')
parser.add_argument('-help',help='Print out a summary of the usage and exit.',action='help')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()

# Get screen identifier
commandToGetScreen = "xrandr --listmonitors | grep \"^ \" | cut -f 6 -d' '"
screen = subprocess.check_output(commandToGetScreen, shell=True)
screen = screen.rstrip() # strips away /n at the end of the line


# Get current brightness 
commandToGetCurrentBrightness = "xrandr --verbose | grep Brightness | cut -f 2 -d' '"
brightness = subprocess.check_output(commandToGetCurrentBrightness, shell=True)
brightness = brightness.rstrip()

# Check first if no arguments are supplied
if len(sys.argv) == 1:
    print "No arguments supplied. Use -h or --help or -help to get more information."


if args.set:
    newbrightness = float(args.set)/100.00
    
    if newbrightness < (MIN_BRIGHTNESS/100.00):
        newbrightness = MIN_BRIGHTNESS/100.00

    if newbrightness > (MAX_BRIGHTNESS/100.00):
        newbrightness = MAX_BRIGHTNESS/100.00

    os.system("xrandr --output " + screen + " --brightness " + str(newbrightness))
    
    sys.exit(1)

if args.inc:
    newbrightness = float(brightness) + float(args.inc)/100.00
    
    if not newbrightness > (MAX_BRIGHTNESS/100.00):
        os.system("xrandr --output " + screen + " --brightness " + str(newbrightness))
    else:
        os.system("xrandr --output " + screen + " --brightness " + str(MAX_BRIGHTNESS/100.00))

    sys.exit(1)

if args.dec:
    newbrightness = float(brightness) - float(args.dec)/100.00
    
    if not newbrightness < (MIN_BRIGHTNESS/100.00):
        os.system("xrandr --output " + screen + " --brightness " + str(newbrightness))
    else:
        os.system("xrandr --output " + screen + " --brightness " + str(MIN_BRIGHTNESS/100.00))
    
    sys.exit(1)

if args.get:
    percentbrightness = float(brightness)*100.00
    print "Current brightness is set at: " + str(percentbrightness)

    sys.exit(1)
