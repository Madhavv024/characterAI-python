
# This is a middleware to remove the prefix from the request path.
class RemovePrefixMiddleware(object):
    def __init__(self, app, prefix='/character-ai'):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        request_uri = environ.get('PATH_INFO', '')
        if request_uri.startswith(self.prefix):
            environ['PATH_INFO'] = request_uri[len(self.prefix):]
        return self.app(environ, start_response)
