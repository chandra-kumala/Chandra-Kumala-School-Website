from django import template
from home.models import Social

register = template.Library()

# Social snippets
@register.inclusion_tag('tags/social.html', takes_context=True)
def social_media_icons(context):
    return {
        'social_icons': Social.objects.all(),
        'request': context['request'],
    }