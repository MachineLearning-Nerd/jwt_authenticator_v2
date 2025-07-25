from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.utils import url_path_join
import jwt
from tornado import (
    gen,
    web,
)
from traitlets import (
    Bool,
    List,
    Unicode,
)
from urllib import parse


def print_exception():
    import sys
    import traceback
    exc_type, exc_value, exc_tb = sys.exc_info()
    except_string = traceback.format_exception(exc_type, exc_value, exc_tb)
    print(except_string)
    return except_string

# import logging
# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# logf = open("app.log", "a")

def log_create():
    logr = open('app.log', 'a')
    exceptions = print_exception()
    logr.write(f"Failed to load: {str(exceptions)}\n")

def log_text(text):
    logr = open('app.log', 'a')
    logr.write(f"Log: {str(text)}\n")


class JSONWebTokenLoginHandler(BaseHandler):
    # async def get(self):
    #     try:
    #         header_name = self.authenticator.header_name
    #         cookie_name = self.authenticator.cookie_name
    #         param_name = self.authenticator.param_name
    #     except:
    #         raise web.HTTPError(402)


    #     try:
    #         auth_header_content = self.request.headers.get(header_name, "") if header_name else None
    #         auth_cookie_content = self.get_cookie(cookie_name, "") if cookie_name else None
    #         auth_param_content = self.get_argument(param_name, default="") if param_name else None
    #     except:
    #         raise web.HTTPError(403)

    #     try:
    #         signing_certificate = self.authenticator.signing_certificate
    #         secret = self.authenticator.secret
    #         algorithms = self.authenticator.algorithms

    #         username_claim_field = self.authenticator.username_claim_field
    #         extract_username = self.authenticator.extract_username
    #         audience = self.authenticator.expected_audience

    #         auth_url = self.authenticator.auth_url
    #         retpath_param = self.authenticator.retpath_param
    #     except:
    #         raise web.HTTPError(404)

    #     try:
    #         _url = url_path_join(self.hub.server.base_url, 'home')
    #         next_url = self.get_argument('next', default=False)
    #         if next_url:
    #             _url = next_url
    #             if param_name:
    #                 auth_param_content = parse.parse_qs(parse.urlparse(next_url).query).get(param_name, "")
    #                 if isinstance(auth_param_content, list):
    #                     auth_param_content = auth_param_content[0]
    #     except:
    #         raise web.HTTPError(405)

    #     try:
    #         if auth_url and retpath_param:
    #             auth_url += ("{prefix}{param}=https://{host}{url}".format(
    #                 prefix='&' if '?' in auth_url else '?',
    #                 param=retpath_param,
    #                 host=self.request.host,
    #                 url=_url,
    #             ))
    #     except:
    #         raise web.HTTPError(406)

    #     try:
    #         if bool(auth_header_content) + bool(auth_cookie_content) + bool(auth_param_content) > 1:
    #             raise web.HTTPError(400)
    #         elif auth_header_content:
    #             token = auth_header_content
    #         elif auth_cookie_content:
    #             token = auth_cookie_content
    #         elif auth_param_content:
    #             token = auth_param_content
    #         else:
    #             return self.auth_failed(auth_url)
    #     except:
    #         raise web.HTTPError(407)

    #     try:
    #         if secret:
    #             claims = self.verify_jwt_using_secret(token, secret, algorithms, audience)
    #         elif signing_certificate:
    #             claims = self.verify_jwt_with_claims(token, signing_certificate, audience)
    #         else:
    #             return self.auth_failed(auth_url)
    #     except jwt.exceptions.InvalidTokenError:
    #         return self.auth_failed(auth_url)

    #     try:
    #         username = self.retrieve_username(claims, username_claim_field, extract_username=extract_username)
    #         user = await self.auth_to_user({'name': username})
    #         self.set_login_cookie(user)
    #     except:
    #         raise web.HTTPError(408)

    #     try:
    #         self.redirect(_url)
    #     except:
    #         raise web.HTTPError(409)

    async def get(self):
        try:
            try:
                param_name = self.authenticator.param_name
                log_text('param_name:' + str(param_name))
            except Exception as e:
                log_create()
                raise web.HTTPError(402)


            try:
                auth_param_content = self.get_argument(param_name, default="") if param_name else None
                log_text('auth_param_content:' + str(auth_param_content))
            except Exception as e:
                log_create()
                raise web.HTTPError(403)

            try:
                secret = self.authenticator.secret
                algorithms = self.authenticator.algorithms
                username_claim_field = self.authenticator.username_claim_field
                audience = self.authenticator.expected_audience
            except Exception as e:
                log_create()
                raise web.HTTPError(404)

            try:
                _url = url_path_join(self.hub.server.base_url, 'home')
                next_url = self.get_argument('next', default=False)
                log_text('next:' + str(next_url))
                log_text('_url:' + str(_url))
                if next_url:
                    _url = next_url
                #     if param_name:
                #         auth_param_content = parse.parse_qs(parse.urlparse(next_url).query).get(param_name, "")
                #         if isinstance(auth_param_content, list):
                #             auth_param_content = auth_param_content[0]
            except Exception as e:
                log_create()
                raise web.HTTPError(405)

            try:
                if auth_param_content:
                    token = auth_param_content
                else:
                    raise Exception('Error')
            except Exception as e:
                log_create()
                raise web.HTTPError(407)

            try:
                try:
                    log_text('secret:' + str(secret))
                    log_text('audience:' + str(audience))
                    log_text('algorithms:' + str(algorithms))
                    if secret:
                        claims = self.verify_jwt_using_secret(token, secret, algorithms, audience)
                        log_text('claims:' + str(claims))
                except jwt.exceptions.InvalidTokenError:
                    raise web.HTTPError(406)
            except Exception as e:
                log_create()
                raise web.HTTPError(406)

            try:
                username = self.retrieve_username(claims, username_claim_field, extract_username=False)
                log_text('username:' + str(username))
                user = await self.auth_to_user({'name': username})
                log_text('user:' + str(user))
                self.set_login_cookie(user)
            except Exception as e:
                log_create()
                raise web.HTTPError(408)

            try:
                self.redirect(_url)
            except Exception as e:
                log_create()
                raise web.HTTPError(409)
        except:
            raise web.HTTPError(417)

    def auth_failed(self, redirect_url):
        if redirect_url:
            self.redirect(redirect_url)
        else:
            raise web.HTTPError(401)

    @staticmethod
    def verify_jwt_with_claims(token, signing_certificate, audience):
        opts = {"verify_aud": False}
        with open(signing_certificate, 'r') as rsa_public_key_file:
            return jwt.decode(token, rsa_public_key_file.read(), audience=audience, options=opts)

    @staticmethod
    def verify_jwt_using_secret(json_web_token, secret, algorithms, audience):
        opts = {"verify_aud": False}
        return jwt.decode(json_web_token, key=secret, algorithms=algorithms, options=opts)

    @staticmethod
    def retrieve_username(claims, username_claim_field, extract_username):
        username = claims[username_claim_field]
        return username.lower()


class JSONWebTokenAuthenticator(Authenticator):
    """
    Accept the authenticated JSON Web Token from header.
    """
    auth_url = Unicode(
        config=True,
        help="""URL for redirecting to in the case of invalid auth token""")

    retpath_param = Unicode(
        config=True,
        help="""Name of query param for auth_url to pass return URL""")

    header_name = Unicode(
        config=True,
        help="""HTTP header to inspect for the authenticated JSON Web Token.""")

    cookie_name = Unicode(
        config=True,
        help="""The name of the cookie field used to specify the JWT token""")

    param_name = Unicode(
        config=True,
        help="""The name of the query parameter used to specify the JWT token""")

    signing_certificate = Unicode(
        config=True,
        help="""
        The public certificate of the private key used to sign the incoming JSON Web Tokens.

        Should be a path to an X509 PEM format certificate filesystem.
        """
    )

    secret = Unicode(
        config=True,
        help="""Shared secret key for siging JWT token. If defined, it overrides any setting for signing_certificate""")

    algorithms = List(
        default_value=['HS256'],
        config=True,
        help="""Specify which algorithms you would like to permit when validating the JWT""")

    username_claim_field = Unicode(
        default_value='username',
        config=True,
        help="""
        The field in the claims that contains the user name. It can be either a straight username,
        of an email/userPrincipalName.
        """
    )

    extract_username = Bool(
        default_value=True,
        config=True,
        help="""
        Set to true to split username_claim_field and take the part before the first `@`
        """
    )

    expected_audience = Unicode(
        default_value='',
        config=True,
        help="""HTTP header to inspect for the authenticated JSON Web Token."""
    )

    def get_handlers(self, app):
        try:
            return [
                (r'/login', JSONWebTokenLoginHandler),
            ]
        except Exception as e:
            raise web.HTTPError(417)

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()


class JSONWebTokenLocalAuthenticator(JSONWebTokenAuthenticator, LocalAuthenticator):
    """
    A version of JSONWebTokenAuthenticator that mixes in local system user creation
    """
    pass
