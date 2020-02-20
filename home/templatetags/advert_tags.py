from django import template
from home.models import Google
from home.models import Facebook
from home.models import Social


register = template.Library()

# Google snippets
@register.inclusion_tag('tags/google.html', takes_context=True)
def google_site_tag(context):
    return {
        'google_tags': Google.objects.all(),
        'request': context['request'],
    }

@register.simple_tag
def google_site_id():
    return Google.objects.first().site_tag


@register.inclusion_tag('tags/facebook.html', takes_context=True)
def facebook_site_tag(context):
    return {
        'facebook_tags': Facebook.objects.all(),
        'request': context['request'],
    }

@register.simple_tag
def facebook_site_id():
    return Facebook.objects.first().site_tag

@register.inclusion_tag('tags/social.html', takes_context=True)
def social_media_icons(context):
    return {
        'social_icons': Social.objects.all(),
        'request': context['request'],
    }