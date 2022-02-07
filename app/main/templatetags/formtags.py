from django.template import Library
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.encoding import force_text

register = Library()


@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='placeholder')
def placeholder(value, arg):
	value.field.widget.attrs["placeholder"] = arg
	return value


@register.filter(name='textarea')
def textarea(value, arg):
	value.field.widget.attrs["rows"] = arg
	return value


@register.filter(name='decimal_to_real')
def decimal_to_real(value, precision=2):
	value = floatformat(value, precision)
	value, decimal = force_text(value).split(',')
	value = intcomma(value)
	value = value.replace(',', '.') + ',' + decimal
	return value