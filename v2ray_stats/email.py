import smtplib
from email.header import Header
from email.mime.text import MIMEText
from v2ray_stats.config import Config
from v2ray_stats.utils import V2RayLogger


def send_mail(month: str, data: list):
    """
    Send traffic report email to user.
    :param month: Report month
    :param data: Data
    :return:
    """

    V2RayLogger.debug('SMTP server: {0}:{1}.'.format(Config.get('mail_host'), Config.get('mail_port')))
    smtp = smtplib.SMTP_SSL(Config.get('mail_host'), Config.get('mail_port'))
    V2RayLogger.debug('SMTP login with: {0}:{1}.'.format(Config.get('mail_user'), Config.get('mail_pass')))
    smtp.login(Config.get('mail_user'), Config.get('mail_pass'))
    V2RayLogger.debug('SMTP login successful.')

    for row in data:
        V2RayLogger.debug('Send email: {0}:{1}.'.format(row[0], row[1]))
        message = '<tr align=left><th align="left">{0:30s}</th><th align="left">{1:9s}</th></tr>\n'.format(
            row[0], row[1])
        message = MIMEText(message, 'html')
        message['Subject'] = Header(Config.get('mail_subject') + ': {0}'.format(month))
        message['From'] = Config.get('mail_user')
        message['To'] = row[0]

        smtp.sendmail(Config.get('mail_user'), row[0], message.as_string())
        V2RayLogger.info('Send traffic to: {0}.'.format(row[0]))

