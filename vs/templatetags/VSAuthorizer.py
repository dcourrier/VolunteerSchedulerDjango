from django import template

register = template.Library()

@register.simple_tag
def vsauthorizer(feature):
    pass