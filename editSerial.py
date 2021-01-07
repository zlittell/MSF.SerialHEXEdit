import os
import sys
import getopt
from textwrap import wrap

def baseN(num, base, numerals="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
      return ((num == 0) and numerals[0]) or (baseN(num // base, base, numerals).lstrip(numerals[0]) + numerals[num % base])

inputHex = ""
outputHex = ""
serialFile = ""
memoryLocation = ""
serialNumber = ""

# List options for arguments
short_options = "hi:o:l:t:s:"
long_option = ["help", "input=", "output=", "location=", "tracker=", "serial="]

# Convert arguments
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:] #Throw away first argument which is python script name
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_option)
except getopt.error as err:
    print(str(err))
    sys.exit(2)

help = '''
Serial Number Editor
Replaces serial numbers stored in hex files at specific memory locations.

The serial number needs to be stored on its own line in memory.
Extended memory access is not supported.
Serial numbers are 10 characters long and are stored as ascii characters.

-h --help
shows this help text

-i --input
Path to input file for editing

-o --output
Path to output file that will contain new serial

-l --location
Memory location line in hex to be replaced.
eg "3EF4"

-t --tracker
File for tracking serial numbers. This is just a simple file that stores the previously used serial number.

-s --serial
Manually inputted serial number. Enter it as 10 characters and it will be converted to ascii.
Useful for calling this file from a server that has more control of serial tracking (managing mfg date, production crew, etc in a database)
'''

# parse arguments
for current_argument, current_value in arguments:
    if current_argument in ("-h", "--help"):
        print(help)
        sys.exit(2)
    elif current_argument in ("-i","--input"):
        print("Input file name: " + current_value)
        inputHex = current_value
    elif current_argument in ("-o", "--output"):
        print ("Output file name: " + current_value)
        outputHex = current_value
    elif current_argument in ("-l", "--location"):
        print ("Serial Memory Location: " + current_value)
        memoryLocation = current_value
    elif current_argument in ("-t", "--tracker"):
        print ("Serial Tracker File: " + current_value)
        serialFile = current_value
    elif current_argument in ("-s", "--serial"):  
        print ("Manually using Serial #: " + current_value)
        serialNumber = current_value

# Verify correct arguments
if (inputHex == ""):
    print ("Must have input file argument")
    sys.exit(2)
if (outputHex == ""):
    print ("Must have output file argument")
    sys.exit(2)
if (memoryLocation == ""):
    print ("Must have a memory location argument")
    sys.exit(2)
if (serialFile == "") & (serialNumber == ""):
    print ("Must have a serial tracker file or manually provide a serial")
    sys.exit(2)


#Read in serial from serial file if specified
if (serialFile != ""):
    # Use serial file
    try:
        print("Opening file: " + serialFile)
        stWriter = open(serialFile, 'r+')
        serial = stWriter.readline()
    except IOError:
        try:
            print("File didn't exist, trying to create file")
            stWriter = open(serialFile, 'w')
            serial = ""
        except:
            print("Could not open or create tracker file")
            raise
    finally:
        if serial == "":
            # new file
            serial = "0000000001"
            print("New tracker file starting at serial: " + serial)
        else:
            # existing file
            #convert serial into a number with base 36 ((0-9)+(A-Z))
            numSerial = int(serial, 36)
            numSerial += 1
            #convert base 36 number back to string of characters
            serial = baseN(numSerial, 36)
            if len(serial) > 10:
                sys.exit("ERROR: Ran out of unused serial numbers. EXITING")
            #pad string to be 10 character serial again
            serialNumber = str(serial).zfill(10)
            print("Serial to use: " + serialNumber)

# Verify serial parameter and convert to ascii
if (len(serialNumber) == 10):
    convertedSerial = bytes(serialNumber, 'ascii').hex()
else:
    sys.exit("ERROR: Serial has to be 10 characters in length. EXITING")

# Process Files
with open(inputHex,'r') as inputWriter:
    with open(outputHex,'w') as outputWriter:
        for line in inputWriter:
            if memoryLocation in line:
                print ("Original serial line is: " + line, end='')
                rLine = "0A" + memoryLocation + "00" + convertedSerial
                #calculate checksum of byte string
                wrapped = wrap(rLine, 2)
                sumValue = 0;
                for value in wrapped:
                    sumValue += int(value, 16)
                checksumValue = -(sumValue % 256)
                checksumValue = '%2X' % (checksumValue & 0xFF)
                rLine += checksumValue
                rLine = ":" + rLine + "\n"
                print("New serial line is: " + rLine, end='')
                outputWriter.write(rLine)
            else:
                outputWriter.write(line)

        #write serial to file
        if (serialFile != ""):
            with open(serialFile, 'w') as stWriter:
                stWriter.write(serial)

print("File " + outputHex + " written successfully")