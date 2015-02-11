#!/usr/bin/python
# coding=UTF-8

###########################################################################
# Hex IP Toolkit: Converts IP addresses to hexadecimal and vice versa.    #
#                 also links the IP addresses to given files              #
#                 written to assist in kickstart / preseed installations  #
#                                                                         #
# Copyright (C) 2009  Hakan Bayindir                                      #
#                                                                         #
# This program is free software: you can redistribute it and/or modify    #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# This program is distributed in the hope that it will be useful,         #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.   #
#                                                                         #
# @author:  Hakan Bayindir                                                #
# @contact: hbayindir@gmail.com                                           #
# @license: GNU/GPLv3                                                     #
# @status:  stable                                                        #
# @version: 1.0.1                                                         #
#                                                                         #
###########################################################################


# Return codes used in this program:
# 
# 0: Everything is OK.
# 1: Invalid IP address (hex or standard).
# 2: Linking failed, file exists.
# 3: Linking failed, unknown reason.
# 4: Operating system is not POSIX.
# 5: Author displayed.
# 6: Version displayed.
# 7: License displayed.
# 8: No argument supplied.

def convertIP(ip_address, link_target, force_link):

    #is this an integer (standard) IP address? Let me see...
    if re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip_address) <> None and len(ip_address) >= 7 and len(ip_address) < 16 and len(re.split("\.", ip_address)) == 4:
        
        hex_ip_parts  = []
        
        ip_parts = re.split("\.", ip_address);
        
        for ip_part in ip_parts:
            if int(ip_part) > 255 or int(ip_part) < 0:
                printError("Given IP address is not valid")
                sys.exit(1)
            
            temporary_hex = re.sub("0x", "", int(ip_part).__hex__())
            
            #pad single digit conversions with a single 0
            if len(temporary_hex) == 1:
                temporary_hex = "0" + temporary_hex
            
            hex_ip_parts.append(temporary_hex)
        
        if link_target == None:
            #now print out the result
            for ip_part in hex_ip_parts:
                sys.stdout.write(string.upper(ip_part))
            
            #write a nice newline before exit.
            sys.stdout.write("\n")
            sys.exit(0)
            
        else:
            #assemble a string hex IP address
            hex_ip = ""
            
            for ip_part in hex_ip_parts:
                hex_ip += string.upper(ip_part.__str__());
            
            link(hex_ip, link_target, force_link)
            sys.exit(0)
    
    #is this an HEX IP address?
    elif re.match("[0-9a-fA-F]{8,8}", ip_address) <> None and len(ip_address) == 8:
        
        divided_hex = []
        
        divided_hex.append("0x" + ip_address[0:2])
        divided_hex.append("0x" + ip_address[2:4])
        divided_hex.append("0x" + ip_address[4:6])
        divided_hex.append("0x" + ip_address[6:8])
        
        ip_address    = ""
        inserted_dots = 0
        
        for hex_part in divided_hex:
            ip_address += int(hex_part, 16).__str__()
            
            if inserted_dots < 3:
                ip_address += "."
                inserted_dots += 1
            
        if link_target == None:
            print ip_address;
            sys.exit(0)
        else:
            link(ip_address, link_target, force_link)
            sys.exit(0)    
    
    else:
        printError("Given IP address is not valid")
        sys.exit(1)


#a pretty standard error reporting function that prepends ERROR: to the message and writes to console.
def printError (errorMessage):
    print "ERROR: " + errorMessage
    
#Symbolic linking code. source is the link, destination is the real file, force is whether the link will be overwritten even if the link exists.
def link(source, target, force):
    try:
        os.symlink(target, source) #try to be nice here.
    except OSError, e:
        if e.errno == errno.EEXIST:
            if force == True: #if usage of deadly force is authorized, use it without thinking twice. (erase file and re-link it)
                os.remove(source)
                os.symlink(target, source)
            else:
                printError("Cannot link file, file already exists.") #else back-off with an error message.
                sys.exit(2)
        else:
            printError("A problem occurred during linking.") #if something happens that we don't understand, say it bravely
            sys.exit(3)
        
if __name__ == "__main__":
    #import the required things.
    import os, errno, sys, re, string
    from optparse import OptionParser
    
    #This program is intended to be used on POSIX compliant operating systems.
    if os.name <> "posix":
        print "This program is designed to run on POSIX compliant operating systems."
        sys.exit(4)
    
    #create the option parser that parses the options for us, the lazy programmers
    parser = OptionParser()
    
    #teach how our program works to the parser, so she can understand it too.
    parser.set_usage("[options] <IP ADDRESS>")
    parser.set_description("Converts IP addresses to hexadecimal equivalents or vice versa. Optionally links the resulting address to given target file.")
    parser.add_option("-l", "--link" , dest="link_target", help="symbolic link the result to the target file", metavar="TARGETFILE")
    parser.add_option("-n", "--noforce", action="store_false", dest="force_linking", default=True, help="doesn't overwrite links if file exists")
    parser.add_option("-L", "--license", action="store_true", dest="print_license", default=False, help="print licensing information and exit")
    parser.add_option("-a", "--author", action="store_true", dest="print_author", default=False, help="print author & contact information and exit")
    parser.add_option("-V", "--version", action="store_true", dest="print_version", default=False, help="print version information and exit")
    
    #Light the path, show the truth! (copy supplied options to options, copy remaining to arguments)
    (options, arguments) = parser.parse_args();
    
    #Handle the information request, author, version and license respectively
    if options.print_author == True:
        print "This program is written by Hakan Bayindir <hbayindir@gmail.com>"
        sys.exit(5)
        
    elif options.print_version == True:
        print parser.get_prog_name() + " version 1.0.5, build 20100102"
        sys.exit(6)
    
    elif options.print_license == True:
        print "\nHex IP Toolkit Copyright (C) 2009  Hakan Bayindir\nThis program is licensed under GNU/GPLv3 and comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it.under certain conditions.\nFor more information, visit http://www.gnu.org/licenses\n"
        sys.exit(7)


    #we need an IP address. not less, not more.
    if len(arguments) <> 1:
        parser.print_usage();
        print "To get complete help, try " + parser.get_prog_name() + " -h"
        sys.exit(8)
    
    #everything looks OK. Do your magic.
    convertIP(arguments[0], options.link_target , options.force_linking)
