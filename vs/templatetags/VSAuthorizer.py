from django import template

register = template.Library()

@register.simple_block_tag(takes_context=True)
def vsauthorizer(context, content):
    pass