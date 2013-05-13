from celery.task.schedules import crontab
from celery.decorators import periodic_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.sites.models import Site

from .models import Week


@periodic_task(run_every=crontab(hour="0", minute="0", day_of_week="1"))
def notify_last_week():
    current_site = Site.objects.get_current()
    domain = current_site.domain

    current_week = Week.get_current_week()

    #skip empty weeks
    while not current_week.is_filled:
        current_week = current_week.next_week()

    prev_week = current_week.previous_week()
    current_shifts = dict(map(lambda x: (x.task, x), current_week.shifts.all()))

    plaintext = get_template('schedule/email_last_week.txt')
    html = get_template('schedule/email_last_week.html')
    subject = get_template('schedule/email_last_week_subject.txt')

    for shift in prev_week.shifts.all():
        if not shift.done:
            d = Context({'user': shift.room.current_user(), 'task': shift.task, 'domain': domain, 'current_shift': current_shifts[shift.task]})

            to = [shift.room.current_user().email]
            subject_content = subject.render(d)
            text_content = plaintext.render(d)
            html_content = html.render(d)
            msg = EmailMultiAlternatives(subject=subject_content, body=text_content, to=to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@periodic_task(run_every=crontab(hour="0", minute="0", day_of_week="3"))
def notify_next_week():
    current_site = Site.objects.get_current()
    domain = current_site.domain

    current_week = Week.get_current_week()
    prev_week = current_week.previous_week()

    #skip empty weeks
    while not prev_week.is_filled:
        prev_week = prev_week.previous_week()

    prev_shifts = dict(map(lambda x: (x.task, x), prev_week.shifts.all()))

    plaintext = get_template('schedule/email_next_week.txt')
    html = get_template('schedule/email_next_week.html')
    subject = get_template('schedule/email_next_week_subject.txt')

    for shift in current_week.shifts.all():
        d = Context({'user': shift.room.current_user(), 'task': shift.task, 'domain': domain, 'prev_shift': prev_shifts[shift.task]})

        to = [shift.room.current_user().email]
        subject_content = subject.render(d)
        text_content = plaintext.render(d)
        html_content = html.render(d)
        msg = EmailMultiAlternatives(subject=subject_content, body=text_content, to=to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
