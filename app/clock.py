from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings

from app.emailer import send_notices

sched = BlockingScheduler()

sched.add_job(
  func=send_notices,
  trigger='cron',
  day_of_week='mon-fri',
  timezone=settings.TIME_ZONE,
  hour=7,
  minute=30
)

sched.start()