# -*- coding: utf-8 -*-
"""
Tests for webapp2 RequestHandler
"""
import os
import sys
import unittest

from webtest import TestApp

from webapp2 import (RedirectHandler, Request, RequestHandler, Route,
    WSGIApplication, get_valid_methods)


class HomeHandler(RequestHandler):
    def get(self, **kwargs):
        self.response.out.write('home sweet home')

    def post(self, **kwargs):
        self.response.out.write('home sweet home - POST')


class MethodsHandler(HomeHandler):
    def put(self, **kwargs):
        self.response.out.write('home sweet home - PUT')

    def delete(self, **kwargs):
        self.response.out.write('home sweet home - DELETE')

    def head(self, **kwargs):
        self.response.out.write('home sweet home - HEAD')

    def trace(self, **kwargs):
        self.response.out.write('home sweet home - TRACE')

    def options(self, **kwargs):
        self.response.out.write('home sweet home - OPTIONS')


class UrlForHandler(RequestHandler):
    def get(self, **kwargs):
        assert self.url_for('home') == '/'
        assert self.url_for('home', foo='bar') == '/?foo=bar'
        assert self.url_for('home', _anchor='my-anchor', foo='bar') == '/?foo=bar#my-anchor'
        assert self.url_for('home', _anchor='my-anchor') == '/#my-anchor'
        assert self.url_for('home', _full=True) == 'http://localhost:80/'
        assert self.url_for('home', _full=True, _anchor='my-anchor') == 'http://localhost:80/#my-anchor'
        assert self.url_for('home', _secure=True) == 'https://localhost:80/'
        assert self.url_for('home', _secure=True, _full=False) == 'https://localhost:80/'
        assert self.url_for('home', _secure=True, _anchor='my-anchor') == 'https://localhost:80/#my-anchor'

        assert self.url_for('methods') == '/methods'
        assert self.url_for('methods', foo='bar') == '/methods?foo=bar'
        assert self.url_for('methods', _anchor='my-anchor', foo='bar') == '/methods?foo=bar#my-anchor'
        assert self.url_for('methods', _anchor='my-anchor') == '/methods#my-anchor'
        assert self.url_for('methods', _full=True) == 'http://localhost:80/methods'
        assert self.url_for('methods', _full=True, _anchor='my-anchor') == 'http://localhost:80/methods#my-anchor'
        assert self.url_for('methods', _secure=True) == 'https://localhost:80/methods'
        assert self.url_for('methods', _secure=True, _full=False) == 'https://localhost:80/methods'
        assert self.url_for('methods', _secure=True, _anchor='my-anchor') == 'https://localhost:80/methods#my-anchor'

        assert self.url_for('route-test', year='2010', month='07', name='test') == '/2010/07/test'
        assert self.url_for('route-test', year='2010', month='07', name='test', foo='bar') == '/2010/07/test?foo=bar'
        assert self.url_for('route-test', _anchor='my-anchor', year='2010', month='07', name='test', foo='bar') == '/2010/07/test?foo=bar#my-anchor'
        assert self.url_for('route-test', _anchor='my-anchor', year='2010', month='07', name='test') == '/2010/07/test#my-anchor'
        assert self.url_for('route-test', _full=True, year='2010', month='07', name='test') == 'http://localhost:80/2010/07/test'
        assert self.url_for('route-test', _full=True, _anchor='my-anchor', year='2010', month='07', name='test') == 'http://localhost:80/2010/07/test#my-anchor'
        assert self.url_for('route-test', _secure=True, year='2010', month='07', name='test') == 'https://localhost:80/2010/07/test'
        assert self.url_for('route-test', _secure=True, _full=False, year='2010', month='07', name='test') == 'https://localhost:80/2010/07/test'
        assert self.url_for('route-test', _secure=True, _anchor='my-anchor', year='2010', month='07', name='test') == 'https://localhost:80/2010/07/test#my-anchor'

        self.response.out.write('OK')


class AppUrlForHandler(RequestHandler):
    def get(self, **kwargs):
        assert self.app.url_for('home') == '/'
        assert self.app.url_for('home', foo='bar') == '/?foo=bar'
        assert self.app.url_for('home', _anchor='my-anchor', foo='bar') == '/?foo=bar#my-anchor'
        assert self.app.url_for('home', _anchor='my-anchor') == '/#my-anchor'
        assert self.app.url_for('home', _full=True) == 'http://localhost:80/'
        assert self.app.url_for('home', _full=True, _anchor='my-anchor') == 'http://localhost:80/#my-anchor'
        assert self.app.url_for('home', _secure=True) == 'https://localhost:80/'
        assert self.app.url_for('home', _secure=True, _full=False) == 'https://localhost:80/'
        assert self.app.url_for('home', _secure=True, _anchor='my-anchor') == 'https://localhost:80/#my-anchor'

        assert self.app.url_for('methods') == '/methods'
        assert self.app.url_for('methods', foo='bar') == '/methods?foo=bar'
        assert self.app.url_for('methods', _anchor='my-anchor', foo='bar') == '/methods?foo=bar#my-anchor'
        assert self.app.url_for('methods', _anchor='my-anchor') == '/methods#my-anchor'
        assert self.app.url_for('methods', _full=True) == 'http://localhost:80/methods'
        assert self.app.url_for('methods', _full=True, _anchor='my-anchor') == 'http://localhost:80/methods#my-anchor'
        assert self.app.url_for('methods', _secure=True) == 'https://localhost:80/methods'
        assert self.app.url_for('methods', _secure=True, _full=False) == 'https://localhost:80/methods'
        assert self.app.url_for('methods', _secure=True, _anchor='my-anchor') == 'https://localhost:80/methods#my-anchor'

        assert self.app.url_for('route-test', year='2010', month='07', name='test') == '/2010/07/test'
        assert self.app.url_for('route-test', year='2010', month='07', name='test', foo='bar') == '/2010/07/test?foo=bar'
        assert self.app.url_for('route-test', _anchor='my-anchor', year='2010', month='07', name='test', foo='bar') == '/2010/07/test?foo=bar#my-anchor'
        assert self.app.url_for('route-test', _anchor='my-anchor', year='2010', month='07', name='test') == '/2010/07/test#my-anchor'
        assert self.app.url_for('route-test', _full=True, year='2010', month='07', name='test') == 'http://localhost:80/2010/07/test'
        assert self.app.url_for('route-test', _full=True, _anchor='my-anchor', year='2010', month='07', name='test') == 'http://localhost:80/2010/07/test#my-anchor'
        assert self.app.url_for('route-test', _secure=True, year='2010', month='07', name='test') == 'https://localhost:80/2010/07/test'
        assert self.app.url_for('route-test', _secure=True, _full=False, year='2010', month='07', name='test') == 'https://localhost:80/2010/07/test'
        assert self.app.url_for('route-test', _secure=True, _anchor='my-anchor', year='2010', month='07', name='test') == 'https://localhost:80/2010/07/test#my-anchor'

        self.response.out.write('OK')


class RedirectToHandler(RequestHandler):
    def get(self, **kwargs):
        self.redirect_to('route-test', _anchor='my-anchor', year='2010',
            month='07', name='test', foo='bar')


class BrokenHandler(RequestHandler):
    def get(self, **kwargs):
        raise ValueError('booo!')


class BrokenButFixedHandler(BrokenHandler):
    def handle_exception(self, exception, debug_mode):
        # Let's fix it.
        self.response.set_status(200)
        self.response.out.write('that was close!')


class Handle404(RequestHandler):
    def get(self, **kwargs):
        self.response.out.write('404 custom handler')
        self.response.set_status(404)


class Handle405(RequestHandler):
    def get(self, **kwargs):
        self.response.out.write('405 custom handler')
        self.response.set_status(405, 'Custom Error Message')
        self.response.headers['Allow'] = 'GET'


class Handle500(RequestHandler):
    def get(self, **kwargs):
        self.response.out.write('500 custom handler')
        self.response.set_status(500)


class PositionalHandler(RequestHandler):
    def get(self, month, day, slug=None):
        self.response.out.write('%s:%s:%s' % (month, day, slug))


class HandlerWithError(RequestHandler):
    def get(self, **kwargs):
        self.response.out.write('bla bla bla bla bla bla')
        self.error(403)


def get_redirect_url(handler, **kwargs):
    return handler.url_for('methods')


app = WSGIApplication([
    (Route('/', name='home'), HomeHandler),
    (Route('/methods', name='methods'), MethodsHandler),
    (Route('/broken'), BrokenHandler),
    (Route('/broken-but-fixed'), BrokenButFixedHandler),
    (Route('/url-for'), UrlForHandler),
    (Route('/app-url-for'), AppUrlForHandler),
    (Route('/<year:\d{4}>/<month:\d\d>/<name>', name='route-test'), None),
    (Route('/<:\d\d>/<:\d{2}>/<slug>', name='positional'), PositionalHandler),
    (Route('/redirect-me', defaults={'url': '/broken'}), RedirectHandler),
    (Route('/redirect-me2', defaults={'url': get_redirect_url}), RedirectHandler),
    (Route('/redirect-me3', defaults={'url': '/broken', 'permanent': False}), RedirectHandler),
    (Route('/redirect-me4', defaults={'url': get_redirect_url, 'permanent': False}), RedirectHandler),
    (Route('/redirect-me5'), RedirectToHandler),
    (Route('/lazy'), 'resources.handlers.LazyHandler'),
    (Route('/error'), HandlerWithError),
], debug=False)

test_app = TestApp(app)

DEFAULT_RESPONSE = """Status: 404 Not Found
content-type: text/html; charset=utf8
Content-Length: 52

404 Not Found

The resource could not be found.

   """

class TestHandler(unittest.TestCase):
    def tearDown(self):
        app.error_handlers = {}

    def test_lazy_handler(self):
        res = test_app.get('/lazy')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'I am a laaazy view.')

    def test_handler_with_error(self):
        res = test_app.get('/error', status=403)
        self.assertEqual(res.status, '403 Forbidden')
        self.assertEqual(res.body, '')

    def test_debug_mode(self):
        app = WSGIApplication([
            (Route('/broken'), BrokenHandler),
        ], debug=True)

        test_app = TestApp(app)
        self.assertRaises(ValueError, test_app.get, '/broken')

    def test_200(self):
        res = test_app.get('/')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'home sweet home')

    def test_404(self):
        res = test_app.get('/nowhere', status=404)
        self.assertEqual(res.status, '404 Not Found')

    def test_405(self):
        res = test_app.put('/', status=405)
        self.assertEqual(res.status, '405 Method Not Allowed')
        self.assertEqual(res.headers.get('Allow'), 'GET, POST')

    def test_500(self):
        res = test_app.get('/broken', status=500)
        self.assertEqual(res.status, '500 Internal Server Error')

    def test_500_but_fixed(self):
        res = test_app.get('/broken-but-fixed')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'that was close!')

    def test_custom_error_handlers(self):
        app.error_handlers = {
            404: Handle404,
            405: Handle405,
            500: Handle500,
        }

        res = test_app.get('/nowhere', status=404)
        self.assertEqual(res.status, '404 Not Found')
        self.assertEqual(res.body, '404 custom handler')

        res = test_app.put('/', status=405)
        self.assertEqual(res.status, '405 Custom Error Message')
        self.assertEqual(res.body, '405 custom handler')
        self.assertEqual(res.headers.get('Allow'), 'GET')

        res = test_app.get('/broken', status=500)
        self.assertEqual(res.status, '500 Internal Server Error')
        self.assertEqual(res.body, '500 custom handler')

    def test_methods(self):
        """Can't test HEAD, OPTIONS and TRACE with webtest?"""
        res = test_app.get('/methods')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'home sweet home')

        res = test_app.post('/methods')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'home sweet home - POST')

        res = test_app.put('/methods')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'home sweet home - PUT')

        res = test_app.delete('/methods')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'home sweet home - DELETE')

        req = Request.blank('/methods')
        req.method = 'HEAD'
        res = req.get_response(app)
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, '')

        req = Request.blank('/methods')
        req.method = 'OPTIONS'
        res = req.get_response(app)
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'home sweet home - OPTIONS')

        req = Request.blank('/methods')
        req.method = 'TRACE'
        res = req.get_response(app)
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'home sweet home - TRACE')

        # 501 Not Implemented
        req = Request.blank('/methods')
        req.method = 'FOOBAR'
        res = req.get_response(app)
        self.assertEqual(res.status, '501 Not Implemented')

    def test_url_for(self):
        res = test_app.get('/url-for')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'OK')

    def test_app_url_for(self):
        res = test_app.get('/app-url-for')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'OK')

    def test_positional(self):
        res = test_app.get('/07/31/test')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, '07:31:test')

        res = test_app.get('/10/18/wooohooo')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, '10:18:wooohooo')

    def test_redirect(self):
        res = test_app.get('/redirect-me')
        self.assertEqual(res.status, '301 Moved Permanently')
        self.assertEqual(res.body, '')
        self.assertEqual(res.headers['Location'], 'http://localhost/broken')

    def test_redirect_with_callable(self):
        res = test_app.get('/redirect-me2')
        self.assertEqual(res.status, '301 Moved Permanently')
        self.assertEqual(res.body, '')
        self.assertEqual(res.headers['Location'], 'http://localhost/methods')

    def test_redirect_not_permanent(self):
        res = test_app.get('/redirect-me3')
        self.assertEqual(res.status, '302 Found')
        self.assertEqual(res.body, '')
        self.assertEqual(res.headers['Location'], 'http://localhost/broken')

    def test_redirect_with_callable_not_permanent(self):
        res = test_app.get('/redirect-me4')
        self.assertEqual(res.status, '302 Found')
        self.assertEqual(res.body, '')
        self.assertEqual(res.headers['Location'], 'http://localhost/methods')

    def test_redirect_to(self):
        res = test_app.get('/redirect-me5')
        self.assertEqual(res.status, '302 Found')
        self.assertEqual(res.body, '')
        self.assertEqual(res.headers['Location'], 'http://localhost/2010/07/test?foo=bar#my-anchor')

    def test_run(self):
        os.environ['REQUEST_METHOD'] = 'GET'

        app.run()
        self.assertEqual(sys.stdout.getvalue(), DEFAULT_RESPONSE)

    def test_run_bare(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        app.run(bare=True)

        self.assertEqual(sys.stdout.getvalue(), DEFAULT_RESPONSE)

class TestHandlerHelpers(unittest.TestCase):
    def test_get_valid_methods(self):
        self.assertEqual(get_valid_methods(BrokenHandler).sort(),
            ['GET'].sort())
        self.assertEqual(get_valid_methods(HomeHandler).sort(),
            ['GET', 'POST'].sort())
        self.assertEqual(get_valid_methods(MethodsHandler).sort(),
            ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE', 'TRACE'].sort())
