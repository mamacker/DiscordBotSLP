from crontab import CronTab

cron = CronTab(user=True)
job = cron.new(command='python3 /home/USER/DiscordBotSLP/DiscordBotSLP.py')
job.minute.every(99999999)

cron.write()