class MenuLeft(object):

	def process_request(self, request):
		if not 'leftmenu' in request.session:
			request.session['leftmenu'] = False
