from celery.task.schedules import crontab
from celery.decorators import periodic_task

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from .models import Shift, Week

# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab
@periodic_task(run_every=crontab(hour="0", minute="0", day_of_week="2"))
def notify_schedule():    
    notify_last_week()
    notify_next_week()



def notify_last_week():
	current_week = Week.get_current_week()
	prev_week = current_week.previous()

	plaintext = get_template('schedule/email_last_week.html')
	html      = get_template('schedule/email_last_week.html')
	subject   = get_template('schedule/email_last_week_subject.txt')

	for shift in prev_week.shifts.all():
		if not shift.done:
			d = Context({ 'user': shift.room.user, 'task': shift.task })

			from_email, to = 'no-reply@huissite.hmvp.nl', shift.room.user.email
			subject_content = subject.render(d)
			text_content = plaintext.render(d)
			html_content = html.render(d)
			msg = EmailMultiAlternatives(subject_content, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()


def notify_next_week():
	current_week = Week.get_current_week()
	next_week = current_week.next()

	plaintext = get_template('schedule/email_next_week.html')
	html      = get_template('schedule/email_next_week.html')
	subject   = get_template('schedule/email_next_week_subject.txt')

	for shift in next_week.shifts.all():
		d = Context({ 'user': shift.room.user, 'task': shift.task })

		from_email, to = 'no-reply@huissite.hmvp.nl', shift.room.user.email
		subject_content = subject.render(d)
		text_content = plaintext.render(d)
		html_content = html.render(d)
		msg = EmailMultiAlternatives(subject_content, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
