#!/usr/bin/python
#-*- coding: utf8 -*-

class HistoryMiddleware(object):
    """ Middleware in charge of keeping the navigation history of
    the user """

    def process_request(self, request):
        if "history" not in request.session.keys():
            request.session['history'] = list()
        request.session['history'].append(request.get_full_path())
        return None
