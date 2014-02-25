#!/usr/bin/env python
import argparse
import keyring
import papercut
import ConfigParser
import getpass
import time
import os

config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.papercut')])
try:
    username = config.get('papercut','username')
except ConfigParser.NoSectionError:
    username = None

p = argparse.ArgumentParser(description='Print some documents')
p.add_argument('--print', '-p', help='a filename to be printed', dest='printjob')
p.add_argument('--printer', '-r', help='a printer name to print to')
p.add_argument('--balance', '-b', nargs='?', const=True, help='display the user\' printing balance')
p.add_argument('--list', '-l', nargs='?', const=True, help='list available printers')
p.add_argument('--user', '-u', help='username')
p.add_argument('--password-options', '-o', choices=['save','prompt'], help='save: prompt for password and save to keyring,\n prompt: prompt for password')

args = p.parse_args()

if not username and not args.user:
    username = raw_input('enter username: ')

password = keyring.get_password('papercut', username)

def list_printers(sessID):
    printers = papercut.listPrinters(sessID)
    print "\nAvailable printers:"
    for i,printer in enumerate(printers):
        print i,"\t",printer[1], "." * (50 - len(printer[1])), printer[0]
    return printers

def get_balance(sessID):
    print '\nYour balance is now: $ %.2f' % (int(papercut.getBalance(sessID)) / 100.0)



if args.password_options or not password:
    password = getpass.getpass()
    
if args.password_options == 'save':
    keyring.set_password('papercut', username, password)
    print "password saved in keyring"

if args.list or args.balance or args.printjob or args.printer:
    sessID = papercut.login(username, password)
    if sessID:
        print '\nLogged in to PaperCut with session ID',sessID
        if args.list: list_printers(sessID)
        if args.balance: get_balance(sessID)
        if args.printjob:
            if not args.printer:
                printers = list_printers(sessID)
                args.printer = raw_input('select printer: ')
                try:
                    printerIndex = int(args.printer)
                    args.printer = printers[printerIndex][1]
                except ValueError:
                    pass
                printJobID = papercut.printFile(args.printjob, args.printer, sessID)
                print '\nJob sent to printer', args.printer
                
                status = papercut.getPrintStatus(printJobID)
                while(status['status'] == 'Submitting'):
                    time.sleep(0.1)
                    status = papercut.getPrintStatus(printJobID)
                print "\nJob queued for printing."

                while(not status['complete']):
                    time.sleep(0.1)
                    status = papercut.getPrintStatus(printJobID)
                print "\nComplete!"
                print "\nThis job cost $", status['cost']
#                print status
                get_balance(sessID)
        
    else:
        print '\nDid not successfully log in to PaperCut'
    


    
