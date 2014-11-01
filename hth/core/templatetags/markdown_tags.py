from django import template
from markdown import markdown

register = template.Library()


@register.filter
def markdownify(text):
    """
    Returns the text rendered to HTML via Markdown.
    """
    return markdown(text)
