from config import settings
from django.core.mail import get_connection, EmailMessage, send_mass_mail, EmailMultiAlternatives
from celery import Task, shared_task
from config.celery import app

def send_auth_email(subject, body, receiver):
    default_mail_settings = settings.MULTIPLE_MAIL_SETTINGS.get('default')

    try:
        with get_connection(
                host=default_mail_settings.get('host'),
                port=default_mail_settings.get('port'),
                username=default_mail_settings.get('user'),
                password=default_mail_settings.get('password'),
                user_tls=default_mail_settings.get('tls')
        ) as connection:
            mail = EmailMessage(subject, body, default_mail_settings.get('user'), [receiver],
                                connection=connection)
            mail.content_subtype = 'html'
            res = mail.send()
        return res
    except Exception as e:
        print('************EMAIL ERROR***********')
        print(e)
        return  str(e)


@app.task
def send_user_notify_email(subject, body, receiver):
    default_mail_settings = settings.MULTIPLE_MAIL_SETTINGS.get('default')

    try:
        with get_connection(
                host=default_mail_settings.get('host'),
                port=default_mail_settings.get('port'),
                username=default_mail_settings.get('user'),
                password=default_mail_settings.get('password'),
                user_tls=default_mail_settings.get('tls')
        ) as connection:
            mail = EmailMessage(subject, body, default_mail_settings.get('user'), [receiver],
                                connection=connection)
            mail.content_subtype = 'html'
            mail.send()
        return True
    except Exception as e:
        print('************EMAIL ERROR***********')
        print(e)
        pass


@app.task
def offer_reward_email(subject, body, receiver):
    default_mail_settings = settings.MULTIPLE_MAIL_SETTINGS.get('default')

    try:
        with get_connection(
                host=default_mail_settings.get('host'),
                port=default_mail_settings.get('port'),
                username=default_mail_settings.get('user'),
                password=default_mail_settings.get('password'),
                user_tls=default_mail_settings.get('tls')
        ) as connection:
            mail = EmailMessage(subject, body, default_mail_settings.get('user'), [receiver],
                                connection=connection)
            mail.content_subtype = 'html'
            mail.send()
        return True
    except Exception as e:
        print('************EMAIL ERROR***********')
        print(e)
        pass

@app.task
def newsletter_email(subject, title, content, subscriber_list):
    # print(subject, title)
    default_mail_settings = settings.MULTIPLE_MAIL_SETTINGS.get('default')

    try:
        with get_connection(
                host=default_mail_settings.get('host'),
                port=default_mail_settings.get('port'),
                username=default_mail_settings.get('user'),
                password=default_mail_settings.get('password'),
                user_tls=default_mail_settings.get('tls')
        ) as connection:

            msq_q = []
            for subscriber in subscriber_list:
                msg = EmailMultiAlternatives(subject,content, "Analytics Steps<default_mail_settings.get('user')>", [subscriber])
                msg.attach_alternative(content, 'text/html')
                # print(msg)
                msq_q.append(msg)
            msg_t = tuple(msq_q)
            # res = send_mass_mail(msg_t,auth_user=default_mail_settings.get('user'), auth_password=default_mail_settings.get('password'),
            #                      connection=connection,fail_silently=False)
            res = connection.send_messages(msg_t)
        return res
    except Exception as e:
        print('************EMAIL ERROR***********')
        print(e)
        return str(e)

