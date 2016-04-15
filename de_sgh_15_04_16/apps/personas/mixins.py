class UrlSessionMixin(object):

    modulo = ''

    def dispatch(self, request, *args, **kwargs):
        request.session['modulo'] = self.modulo
        request.session['modulo_titulo'] = self.modulo
        request.session['id'] = kwargs['pk']
        request.session.modified = True
        return super(UrlSessionMixin, self).dispatch(request, *args, **kwargs)
