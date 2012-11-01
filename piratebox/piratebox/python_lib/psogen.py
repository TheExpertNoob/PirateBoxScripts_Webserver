#!/usr/bin/python

# Modificated ShoutBox Library
#   enables further modifications for the ShoutBox
#   Run without to generate htmlfile
#   Run the following to enter a new line from command line
#     psogen.py input Anonymous default "Text" 

import os, datetime, re 

datafilename = os.environ["SHOUTBOX_CHATFILE"]
htmlfilename = os.environ["SHOUTBOX_GEN_HTMLFILE"]

try:
     broadcast_destination = eval ( os.environ["SHOUTBOX_BROADCAST_DESTINATIONS"] ) 
except KeyError:
     broadcast_destination = False 


#--------------
#  Generates Shoutbox-HTML-Frame  ... 
#           Imports:
#               content    -   String  containing preformatted data
#--------------
def generate_html(content):
    css = open("style.css", 'r')
    stl =  css.read()
    css.close()

    htmlstring =   "<html><head><meta name='GENERATOR' content='PyShoutOut'><title>Shout-Out Data</title><style type='text/css'>" 
    htmlstring +=  "<style>" + stl   + "</style></head><body>"  
    htmlstring +=  content 
    htmlstring +=  "</body></html>" 
    return htmlstring 

#--------------
#   Generates HTML Data based on given content  and write it to static html file
#          Imports: 
#               content    -   String  containing preformatted data
#--------------
def generate_html_into_file(content):
    css = open("style.css", 'r')
    stl =  css.read()
    css.close()

    htmlstring = generate_html ( content )

    htmlfile = open( htmlfilename , 'w' )
    htmlfile.write( htmlstring )
    htmlfile.close()

#--------------
# Generates HTML Data based on datafilename 's content 
#--------------
def generate_html_from_file():
    old =  read_data_file() 
    generate_html_into_file( old   )

#--------------
# Generates and Displays generated HTML
#--------------
def generate_html_to_display_from_file():    
    old =  read_data_file()
    htmlstring = generate_html ( old )
    print htmlstring 

#--------------
#  Reads Data file from datafilename given name
#--------------
def read_data_file():
    datafile = open(datafilename, 'r')
    old = datafile.read()
    datafile.close()
    return old

#--------------
# Function for saving new Shoubox-Content & Regenerate static HTML file -- usually called by HTML-Form
#--------------
def process_form( name , indata , color ):
    content = save_input(  name , indata , color ) 

    if broadcast_destination == False:
          generate_html_into_file ( content )


#--------------
# Acutally Saves SB-Content to datafile
#--------------
def save_input( name , indata , color ):

    content = prepare_line ( name, indata, color  )

    if broadcast_destination != False:
        pass 
    else:
        old = read_data_file()
        finalcontent = content  + old 
        datafile = open(datafilename, 'r+')
        datafile.write(finalcontent)
        #datafile.truncate(0)
        datafile.close()

    return finalcontent 

def prepare_line ( name, indata, color  ):
    datapass = re.sub("<", "&lt;", indata)
    data = re.sub(">", "&gt;", datapass)
    curdate = datetime.datetime.now()
    content = "<date>" + curdate.strftime("%H:%M:%S") + "</date>&nbsp;&nbsp;<name>" + name + ":</name>&nbsp;&nbsp;&nbsp;<data class='" + color + "'>" + data + "</data><br>\n" 
    return content

#--------------
#  Testing or Generating static HTML File
#--------------
if __name__ == "__main__":
  import sys
  if sys.argv.count("input") >= 1 :
     save_input(  sys.argv[2] ,  sys.argv[3] ,  sys.argv[4] )
     generate_html_to_display_from_file()
     print "Entered Text."
  
  generate_html_from_file ()
  print "Generated HTML-Shoutbox File."



