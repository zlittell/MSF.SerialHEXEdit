# **Serial Number Editor**

Replaces serial numbers stored in hex files at specific memory locations.

The serial number needs to be stored on its own line in memory.
Extended memory access is not supported.
Serial numbers are 10 characters long and are stored as ascii characters.

***
*-h --help*
shows this help text

*-i --input*
Path to input file for editing

*-o --output*
Path to output file that will contain new serial

*-l --location*
Memory location line in hex to be replaced.
eg "3EF4"

*-t --tracker*
File for tracking serial numbers. This is just a simple file that stores the previously used serial number.

*-s --serial*
Manually inputted serial number. Enter it as 10 characters and it will be converted to ascii.
Useful for calling this file from a server that has more control of serial tracking (managing mfg date, production crew, etc in a database)
***
