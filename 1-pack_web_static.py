#!/usr/bin/python3
# Tar file for shipping the code using Fabric

from fabric.api import local
from datetime import datetime


def do_pack():
    """ Creates a tar file from the folder web_static
    """
    a = datetime.now()
    file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(a.year,
                                                              a.month,
                                                              a.day,
                                                              a.hour,
                                                              a.minute,
                                                              a.second)
    try:
        print("Packing web_static to " + file_name)
        local("mkdir -p versions")

        local("tar -cvzf " + file_name + " web_static")
        return file_name
    except:
        return None
