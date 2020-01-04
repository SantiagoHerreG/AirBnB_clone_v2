#!/usr/bin/python3
# deploy function that automates the deployment

from fabric.api import local, put, run, env
from datetime import datetime
import os


env.hosts = ['34.74.191.132', '34.74.231.8']
env.key_filename = "~/.ssh/holberton"


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


def do_deploy(archive_path):
    """ Saves the uncompressed files in the server
    and links to the web server configuration
    """
    if not os.path.isfile(archive_path):
        return False

    try:
        file_name = archive_path[9:]
        file_n_short = file_name[:-4]
        curr_path = os.getcwd()
        full_path = curr_path + "/" + archive_path
        put(full_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/" + file_n_short)
        run("tar -xzf /tmp/" + file_name + " -C /data/web_static/releases/" +
            file_n_short + "/")
        run("rm /tmp/" + file_name)
        run("mv /data/web_static/releases/" + file_n_short +
            "/web_static/* /data/web_static/releases/" + file_n_short + "/")
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/" +
            file_n_short + " /data/web_static/current")
        return True
    except:
        print("error")
        return False


def deploy():
    """ Deploys by calling the previous functions
    """
    new_archive = do_pack()

    if new_archive is None:
        return False

    res = do_deploy(new_archive)
    return res
