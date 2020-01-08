#!/usr/bin/python3
# deploy function that automates the deployment

from fabric.api import local, put, run, env
from datetime import datetime
import re


env.hosts = ['34.74.191.132', '34.74.231.8']
env.key_filename = "~/.ssh/holberton"
env.user = "ubuntu"


def do_pack():
    """ Creates a tar file from the folder web_static
    """
    a = datetime.now()
    file_name = "versions/web_static_{}{}{}{}{}{}.tgz\
".format(a.year if a.year > 999 else "0" + str(a.year),
         a.month if a.month > 9 else "0" + str(a.month),
         a.day if a.day > 9 else "0" + str(a.day),
         a.hour if a.hour > 9 else "0" + str(a.hour),
         a.minute if a.minute > 9 else "0" + str(a.minute),
         a.second if a.second > 9 else "0" + str(a.second))
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


def do_clean(number=0):
    """
    Cleans the current files, leaving only the n newer versions
    """
    res = run("ls /data/web_static/releases")

    number = int(number)
    list_names = str(res).split()
    date_list = []
    delete_list = []
    patt1 = re.compile(r'web_static_\d{14}')
    for name in list_names:
        if re.fullmatch(patt1, name):
            date_list.append(int(name[11:]))
        else:
            delete_list.append(name)

    for elem in delete_list:
        run("rm -Rf /data/web_static/releases/" + elem)

    if number == 0:
        list_names.remove("web_static_" + str(max(date_list)))
    else:
        for _ in range(0, number):
            newer = max(date_list)
            list_names.remove("web_static_" + str(newer))
            date_list.remove(newer)

    for names in list_names:
        run("rm -Rf /data/web_static/releases/" + names)

    res = local("ls versions")
    version_names = str(res).split()
    delete_list = []
    patt2 = re.compile(r'web_static_\d{14}\.tgz')
    for name in version_names:
        if re.fullmatch(patt2, name) is None:
            delete_list.append(name)
    for names in delete_list:
        local("rm -Rf versions/" + names)
    for names in list_names:
        local("rm -Rf versions/" + names + ".tgz")


def deploy():
    """ Deploys by calling the previous functions
    """
    new_archive = do_pack()

    if new_archive is None:
        return False

    res = do_deploy(new_archive)
    return res
