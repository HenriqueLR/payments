#encoding: utf-8

from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings



def send_mail_template(reset, fail_silently=False):
	body_text = '''<p>Para criar uma nova senha, acesse o link:
			   <a href="http://192.168.0.104:8000/accounts/confirm_reset_password?key=%s"
			   title="Link para Criar Nova Senha">Criar Nova Senha</a></p>''' % (reset.key)
	message_txt = striptags(body_text)

	email = EmailMultiAlternatives(
        subject='Payments - RESET PASSWORD',
        body=message_txt,
        from_email='payments@payments.com',
        to=[reset.user.email],
    )

	email.attach_alternative(body_text, "text/html")
	email.send()