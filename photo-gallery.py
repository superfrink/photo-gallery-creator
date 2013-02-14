""" this script takes a list of image files and makes an HTML
    index page for them including thumbnails.

    run this script like:
      time python photo-gallery.py *.JPG

    N.B. this script relies on the ImageMagick programs being installed.
         in particular the 'convert' program must be in your search path.

    author: chad clark
    email:  chad.clark _AT_ gmail _DOT_ com
    web:    http://superfrink.net/

    created: 2007-02-17
    $Id$
"""

import commands
import os
import re
import shutil
import string
import sys
import time


# -- globals -----------------------------------------------------
THUMBNAIL_DIRECTORY = "thumbnails"
INDEX_FILE = "index.htm"


# -- subroutines -------------------------------------------------

def get_thumb_file_name(dir, file):
    """ get the name of a thumbnail file based on the name of the
        original file
    """
    return dir + "/" + file


def create_thumbnail(thumb_dir, file):
    """ take a file and create a thumbnail file for it
    """

    print "Creating thumbnail for %s ." % file

    thumb_file_name = get_thumb_file_name(thumb_dir, file)

    # if there is a thumbnail file move it aside
    if os.path.exists(thumb_file_name):
        date_str = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime(time.time()))
        new_file = thumb_file_name + "." + date_str
        print "move " + thumb_file_name + " " + new_file 
        shutil.move(thumb_file_name, new_file)

    cmd_line = "convert -thumbnail 300x300 %s %s" % (file, thumb_file_name)
    #print cmd_line
    (cmd_status, cmd_output) = commands.getstatusoutput(cmd_line)


def make_html_index(thumb_dir, file_list):

    print "\nCreating index.\n"

    # if there is an index file move it aside
    if os.path.exists(INDEX_FILE):
        date_str = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime(time.time()))
        new_file = INDEX_FILE + "." + date_str
        #print "move " + INDEX_FILE + " " + new_file 
        shutil.move(INDEX_FILE, new_file)

    # create the index file
    fh = open(INDEX_FILE, "w")
    try:
        fh.write("<html>\n")
        fh.write("<head>\n")
        fh.write("</head>\n")

        fh.write("<body>\n")

        fh.write("  <table align=\"center\">\n")
        fh.write("  <tr>\n")

        count_this_line = 0
        for file in file_list:

             is_new_row = (count_this_line % 3 == 0)

             if is_new_row:
                 fh.write("  </tr>\n")
                 fh.write("  <tr>\n")

             fh.write("    <td align=\"center\">\n")
             fh.write("    <a href=\"%s\">" % file)
             fh.write("<img src=\"%s\">" % get_thumb_file_name(thumb_dir, file) )
             fh.write("</a>\n")
             fh.write("    </td>\n")

             count_this_line += 1

        fh.write("  </tr>\n")
        fh.write("  </table>\n")

        fh.write("</body>\n")
        fh.write("</html>\n")

    finally:
        fh.close()

def make_thumbnails(thumb_dir, file_list):

    # make the thumbnail directory
    if not os.path.isdir(thumb_dir):
        os.mkdir(thumb_dir)

    for file in file_list:
        create_thumbnail(thumb_dir, file)

def usage_message(prog_name):

    usage_str = "\n"
    usage_str = usage_str + "Use: %s FILES\n" % prog_name
    usage_str = usage_str + "\n"
    usage_str = usage_str + "Where FILES is a list of image files.\n"
    usage_str = usage_str + "Examples:\n"
    usage_str = usage_str + "\n"
    usage_str = usage_str + "  %s *.jpg\n" % prog_name
    usage_str = usage_str + "  %s 1.jpg 2.jpg 3.jpg\n" % prog_name
    usage_str = usage_str + "\n"

    return usage_str

# -- main() ------------------------------------------------------

def main(argv=None):

    # get the command line arguments
    if argv is None:
        argv = sys.argv

    if (len(argv) ==1):
        print usage_message(argv[0])
        return 1

    # chop off the program name
    image_file_list = argv[1:]
    print "Image list: ", image_file_list , "\n"

    make_thumbnails(THUMBNAIL_DIRECTORY, image_file_list)
    make_html_index(THUMBNAIL_DIRECTORY, image_file_list)

    return 0


# -- start it up ------------------------------------------------

sys.exit(main())
