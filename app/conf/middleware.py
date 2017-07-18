from django.conf import settings
from django.utils import translation



class MenuLeft(object):
	'''
	Middleware init leftmenu status
	'''
	def process_request(self, request):
		if not request.session.has_key('leftmenu'):
			request.session['leftmenu'] = False


class ForceDefaultLanguage(object):
	'''
	Force language default settings
	'''
	def process_request(self, request):

		if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
			del request.META['HTTP_ACCEPT_LANGUAGE']

		request.LANG = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
		translation.activate(request.LANG)
		request.LANGUAGE_CODE = request.LANG