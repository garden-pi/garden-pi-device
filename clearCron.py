import getpass
from crontab import CronTab

# crontab
cron = CronTab(user=getpass.getuser())

# clear existing
cron.remove_all()

cron.write()

for item in cron:
    print(item)

print("Done!")