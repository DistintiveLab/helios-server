'''
Script para teste de envio de email pela aplicação.
No ambiente containerizado, você pode executar a partir do host:

docker exec -it <nome do container da aplicação> python test-send-mail.py email1@example.com email2@example.com

Se aplicação instalada direto no host, executar apenas python test-send-mail.py email1@example.com  a partir do diretório do script. Se instalado em ambiente virtual, não esquecer de ativar o ambiente.

Se não passar nenhum email adicional de parâmetro, ele vai utilizar o email cadastrado em 
settings.ADMINS
'''

import argparse
import os
import django
from django.conf import settings
from django.core.mail import send_mail
 
# Configuração para acesso às variáveis de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

# Cria parser dos argumentos, para passagem de parâmetros na chamada do script
parser = argparse.ArgumentParser()
parser.add_argument('email', nargs='*')
args = parser.parse_args()

subject = 'Teste envio django via shell'
from_email = settings.DEFAULT_FROM_EMAIL
message = 'Teste de envio pelo django via shell'
recipient_list = settings.ADMINS
html_message = '<h1>Teste de envio pelo django via shell</h1>'\
'<p>Esse teste demonstra que o django está conseguindo enviar emails.<br>'\
'Portanto, se algum email de eleição não foi recebido, pode ser outro problema, '\
'como destinatário inexistente, remetente recusado, etc.</p>'

# Adiciona emails passados por parâmetro na linha de comando
for email in args.email:
    recipient_list.append(email)
    
print(f'Este teste, se bem sucedido, será enviado para: {recipient_list}')

if recipient_list:
    send_mail(subject, message, from_email, recipient_list, 
            fail_silently=False, html_message=html_message)
else:
    print('Nenhum email disponível para envio de teste')
