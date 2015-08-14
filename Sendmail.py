#!/usr/bin/env python
'''
Created on Nov 9, 2014

@author:  Furong Peng
@contact: pengfurong2009@gmail.com

'''
# Import smtplib for the actual sending function
import smtplib

# Import Configuration Parser 
import ConfigParser
from os.path import basename

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
import sys
# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.


def readConfig(cfgfile):
    config = ConfigParser.RawConfigParser()
    with open(cfgfile) as cfgfp:
        config.readfp(cfgfp)
        host=config.get("smtp","host")
        port=int(config.get("smtp","port"))
        SSL=bool(int(config.get("smtp","SSL")))
        me=config.get("account","me")
        username=config.get("account","username")
        password=config.get("account","password")
        you=config.get("maillist","you")
        you = you.split(',')
        you = map(str.strip,you)
        you = filter(bool, you)
    return host,port,SSL,me,username,password,you


def main(fileList):
    cfgfile = fileList[0]
    del fileList[0]
    msgfile = fileList[0]
    del fileList[0]
    
    host,port,SSL,me,username,password,to = readConfig(cfgfile)

    fp = open(msgfile, 'r')
    title = fp.readline().strip()
    body = MIMEText(fp.read())
    fp.close()

    # Create Email
    msg = MIMEMultipart( )
    msg['From'] = me
    msg['To'] = COMMASPACE.join(to)
    msg['Subject'] = title
    msg.attach(body)
    for f in fileList or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(f),
                Name=basename(f)
            ))
 
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    if SSL == True:
        s = smtplib.SMTP_SSL(host,port)
    else:
        s = smtplib.SMTP(host,port)
    #s.starttls()
    s.login(username,password)
    s.sendmail(me, to, msg.as_string())
    s.quit()


if __name__ == '__main__':
    if len(sys.argv) >2:
        main(sys.argv[1:])
    else:
        print "The input is file list:"
        print "1. configure file"
        print "2. message file"
        print "3. attatchment file..."
        print "For example:"
        print "Sendmail.py configfile messagefile attatchment1 attachment2 ..."

