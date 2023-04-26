from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

register = template.Library()

PASSWORD_HELP = _('<p>If you upload a csv file containing the fields unique_id,email,full name, like the example bellow:</p>' \
                '<pre>' \
                '1122233344,eleitor@email.com,Eleitor Nonono<br>' \
                '12345678900,segundo@email.com,Segundo Nomomom <br>'\
                '</pre>' \
                '<p>the system will consider they are voters that will vote using a user and password ' \
                'unique for this election, one that will be sent by them by email. That is, once you freeze' \
                'the ballot, you\'ll have to sent the email to the voters, using the option <em> email voters.</em></p>'\
                '<p>Only after sending this email voters will have the election credentials and will be able to vote.</p>')

MISC_HELP = _('<p> Alternatively you can upload a voter file mixing voter types.' \
                'For instance, voter type password and voter type ldap or another'\
                'authentication system that is enabled for your helios installation </p>' \
                'For example: ' \
                '<pre>' \
                'password,1122233344,eleitor@email.com,Eleitor Nonono<br>' \
                'ldap,1122233344,eleitor@email.com,Eleitor Nonono <br>'\
                '</pre>' \
                '<p>If you provide voters of the <em>password</em> type, you have to sent an email '\
                'using the option <em> email voters.</em> in order to them receive their credentials to vote.</p>')

@register.simple_tag
def voters_help_text(type):
    print(type)
    if type == "default":
        if settings.DEFAULT_VOTER_TYPE == 'password':
            return mark_safe(PASSWORD_HELP)
        else:
            return ""
    if type == "misc":
        return mark_safe(MISC_HELP)