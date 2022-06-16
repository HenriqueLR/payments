from django.conf import settings
from django.utils import translation



class MenuLeft:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if not request.session.has_key('leftmenu'):
			request.session['leftmenu'] = True
		response = self.get_response(request)			
		return response		


class ForceDefaultLanguage:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if 'HTTP_ACCEPT_LANGUAGE' in request.META:
			del request.META['HTTP_ACCEPT_LANGUAGE']

		request.LANG = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
		translation.activate(request.LANG)
		request.LANGUAGE_CODE = request.LANG
		response = self.get_response(request)
		return response		