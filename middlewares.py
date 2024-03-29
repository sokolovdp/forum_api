from secure import SecureHeaders

secure_headers = SecureHeaders()


def setup_middleware(app):
    @app.middleware('response')
    async def set_secure_headers(request, response):
        secure_headers.sanic(response)
