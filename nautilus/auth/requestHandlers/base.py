# external imports
from aiohttp_session import get_session
# local imports
from nautilus.network.http import RequestHandler
from nautilus.conventions.services import auth_service_name
from nautilus.conventions.auth import cookie_name as auth_cookie_name

class AuthRequestHandler(RequestHandler):

    async def get_current_user(self):
        """
            This function logs the given user in on the request request.
        """
        # grab the current session
        session = await get_session(self.request)

        try:
            # add the user to the session
            return session[self._token_name]
        # if the user is not logged in yet
        except KeyError:
            # there isn't a current user
            return None


    async def login_user(self, user):
        """
            This function logs the given user in on the request request.
        """
        # grab the current session
        session = await get_session(self.request)
        # add the user to the session
        session[self._token_name] = self._token_contents(user)



    async def logout_user(self, response):
        """
            This method logs the current user out by clearing the cookie.
        """
        # grab the current session
        session = await get_session(self.request)
        # remove entry in the session
        del session[self._token_name]


    @property
    def _token_name(self):
        """
            The name of the authentication cookie
        """
        return auth_cookie_name()


    def _token_contents(self, user):
        """
            This method provides the jwt contents for the given user.
        """
        return str(user['id'])
