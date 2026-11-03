# helios_auth/auth_systems/discourse.py

import base64
import hmac
import hashlib
import urllib.parse
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from helios_auth.utils import format_recipient

# Ensure these are defined in your main settings.py
SECRET = getattr(settings, 'DISCOURSE_SECRET', '')
DISCOURSE_URL = getattr(settings, 'DISCOURSE_URL', '')

# some parameters to indicate that status updating is not possible
STATUS_UPDATES = False

# helios_auth/auth_systems/discourse.py

def get_auth_url(request, redirect_url=None):
    """
    redirect_url: É a URL do Helios para onde o usuário deve voltar (ex: https://coletivo.net.br)
    """
    nonce = base64.b64encode(hashlib.sha256(SECRET.encode()).digest()).decode()[:16]
    request.session['discourse_nonce'] = nonce
    
    # 1. ATENÇÃO AQUI: O parâmetro DEVE ser estritamente 'return_sso_url'
    # E o valor dele DEVE ser a URL de retorno para o Helios (redirect_url)
    payload = f"nonce={nonce}&return_sso_url={redirect_url}"
    
    base64_payload = base64.b64encode(payload.encode()).decode()
    signature = hmac.new(SECRET.encode(), base64_payload.encode(), hashlib.sha256).hexdigest()
    
    query_string = urllib.parse.urlencode({'sso': base64_payload, 'sig': signature})
    
    # 2. O endpoint correto no Discourse que gerencia o fluxo de IdP externo
    return f"{DISCOURSE_URL}/session/sso_provider?{query_string}"


def get_user_info_after_auth(request):
    """Step 2: Handle the returning payload sent back from Discourse"""
    sso = request.GET.get('sso')
    sig = request.GET.get('sig')
    
    # Verify signature match
    expected_sig = hmac.new(SECRET.encode(), sso.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_sig, sig):
        return None
        
    # Decode and parse query string params sent by Discourse
    decoded = base64.b64decode(sso.encode()).decode()
    user_data = dict(urllib.parse.parse_qsl(decoded))
    
    # Validate session nonce to confirm origin integrity
    if user_data.get('nonce') != request.session.get('discourse_nonce'):
        return None
        
    return {
        'type': 'discourse',
        'user_id': user_data.get('username'), # Unique identifier for Helios
        'name': user_data.get('name') or user_data.get('username'),
        'info': {
            'email': user_data.get('email'),
            'avatar_url': user_data.get('avatar_url')
        },
        'token': None # DiscourseConnect manages sessions directly, no token storage needed
    }

def update_status(token, message):
    pass

def send_message(user_id, user_name, user_info, subject, body):
    email = user_info.get('email')
    if not email:
        return
    name = user_name or email
    send_mail(subject, '', settings.SERVER_EMAIL, [format_recipient(name, email)],
        fail_silently=False, html_message=body)

#
# Election Creation
#
def can_create_election(user_id, user_info):
    return True
