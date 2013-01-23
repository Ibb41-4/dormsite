from dns.resolver import query
import smtplib
import threading

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address
from django.utils.encoding import force_bytes


class EmailBackend(BaseEmailBackend):

    def __init__(self, fail_silently=False, **kwargs):
        super(EmailBackend, self).__init__(fail_silently=fail_silently)
        self._lock = threading.RLock()

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        if not email_messages:
            return
        with self._lock:
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False
        from_email = sanitize_address(email_message.from_email, email_message.encoding)
        recipients = [sanitize_address(addr, email_message.encoding)
                      for addr in email_message.recipients()]
        message = email_message.message()
        charset = message.get_charset().get_output_charset() if message.get_charset() else 'utf-8'
        try:
            for recipient in recipients:
                self._send_one_mail(recipient, from_email, force_bytes(message.as_string(), charset))
        except:
            if not self.fail_silently:
                raise
            return False
        return True

    def _send_one_mail(self, to, sfrom, body):
        hostname = to.split('@')[-1]

        hosts = self._resolve_hosts(hostname)

        success = False

        for host in hosts:
            success = self._send_actual_mail(host, to, sfrom, body)

            if success:
                break

        if not success and to != settings.EMAIL_ERROR_ADDRESS:
            self._send_one_mail(settings.EMAIL_ERROR_ADDRESS, sfrom, body)

    def _resolve_hosts(self, hostname):
        return map(lambda x: str(x.exchange)[0:-1], sorted(query(hostname, 'MX')))

    def _send_actual_mail(self, host, to, sfrom, body):
        try:
            # setup server
            server = smtplib.SMTP(host)

            try:
                server.sendmail(sfrom, [to], body)
            except:
                result = False
            else:
                result = True
        except:
            if not self.fail_silently:
                raise
            result = False
        else:
            #close connection
            try:
                server.quit()
            except:
                pass

        return result
