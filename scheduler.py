from apscheduler.schedulers.background import BackgroundScheduler
import main

def my_task():
    main.run()

job = BackgroundScheduler()
# Run my_task every 3 hours
job.add_job(my_task, 'interval', hours=3)

try:
    job.start()
except (KeyboardInterrupt, SystemExit):
    pass
