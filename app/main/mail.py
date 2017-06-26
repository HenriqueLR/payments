#encoding: utf-8

from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings



def send_mail_template(reset, fail_silently=False):
	body_text = '''<p>Para criar uma nova senha, acesse o link:
			   <a href="http://192.168.0.103:8000/accounts/confirm_reset_password?key=%s"
			   title="Link para Criar Nova Senha">Criar Nova Senha</a></p>''' % (reset.key)
	message_txt = striptags(body_text)

	email = EmailMultiAlternatives(
        subject='Payments - Alterar Senha',
        body=message_txt,
        from_email='payments@payments.com',
        to=[reset.user.email],
    )

	email.attach_alternative(body_text, "text/html")
	email.send()


def send_mail_confirm_account(profile):
	body_text = '''<p>Bem Vindo a sua carteira virtual, estamos processando o seu cadastro</p>
				   <p>certifique-se de que completou todas as etapas, para liberação do sistema.</p>
				   <br>
				   <p>Se houver atraso na liberação do sistema, após o pagamento, entrar em contato</p>
				   <p>no telefone disponibilizado, no ato do pagamento.</p>
				'''
	message_txt = striptags(body_text)

	email = EmailMultiAlternatives(
		subject='Payments - Bem Vindo',
		body=message_txt,
		from_email='payments@payments.com',
		to=[profile.user.email],
	)

	email.attach_alternative(body_text, "text/html")
	email.send()