# CLI to generate .env file, shell script, and crontab
import os
import stat
import getpass
from crontab import CronTab

CURRENT_DIR = os.getcwd()


def print_divider():
    print("---------------")


def welcome():
    print("Garden Pi Setup")
    print_divider()


def create_env():
    # .env file
    api_endpoint = input("Enter API Endpoint: ")
    api_key = input("Enter API KEY: ")
    plant_name = input("Enter Plant name: ")

    print_divider()
    env_filename = ".env"
    print("Writing .env file: {}".format(env_filename))
    env_file = open(env_filename, "w+")

    env_file.write("API_URL={}\n".format(api_endpoint))
    env_file.write("API_GATEWAY_KEY={}\n".format(api_key))
    env_file.write("PLANT_NAME={}\n".format(plant_name))

    env_file.close()

    print_divider()


def create_sh_script():
    sh_filename = "garden_party.sh"
    print("Writing cron script: {}".format(sh_filename))
    sh_file = open(sh_filename, "w+")

    sh_script = """#!/bin/bash
PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin

# current directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pushd $DIR
pipenv run update >> $DIR/update.log 2>&1
popd"""

    sh_file.write(sh_script)

    # make executable
    st = os.stat("{0}/{1}".format(CURRENT_DIR, sh_filename))
    os.chmod("{0}/{1}".format(CURRENT_DIR, sh_filename),
             st.st_mode | stat.S_IEXEC)

    print_divider()


def create_cron_job():
    # crontab
    cron = CronTab(user=getpass.getuser())

    # clear existing
    cron.remove_all()

    job = cron.new(
        command="{0}/garden_party.sh >> {0}/crontab.log 2>&1".format(CURRENT_DIR))
    job.minute.every(30)

    cron.write()

    print("Writing crontab: ")
    for item in cron:
        print(item)

    print_divider()


def run():
    welcome()
    create_env()
    create_sh_script()
    create_cron_job()
    print("Done!")


# run me
run()
