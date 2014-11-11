# Auto-document Django models
# Copied and adapted from https://djangosnippets.org/snippets/2533/

import inspect
from django.utils.html import strip_tags
from django.utils.encoding import force_text
from django.db import models


def process_docstring(app, what, name, obj, options, lines):

    # Only look at objects that inherit from Django's base model class
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        fields = obj._meta.fields

        for field in fields:
            help_text = strip_tags(force_text(field.help_text))
            verbose_name = force_text(field.verbose_name).capitalize()
            field_type = type(field).__name__

            if help_text:
                lines.append(':param %s: %s' % (field.attname, help_text))
            else:
                lines.append(':param %s: %s' % (field.attname, verbose_name))

            lines.append(':type %s: %s' % (field.attname, field_type))

    # Return the extended docstring
    return lines


def setup(app):
    app.connect('autodoc-process-docstring', process_docstring)
