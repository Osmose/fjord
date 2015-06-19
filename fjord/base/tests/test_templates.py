from fjord.base.middleware import MOBILE_COOKIE

from fjord.base.tests import eq_, LocalizingClient
from fjord.search.tests import ElasticTestCase


# This is an ElasticTestCase instead of a normal one because the front
# page (which this queries) uses ElasticSearch. Being an
# ElasticTestCase makes sure that the testing index is properly set
# up, instead of trying to access a possibly missing index.
class MobileQueryStringOverrideTest(ElasticTestCase):
    client_class = LocalizingClient

    def test_mobile_override(self):
        """Test mobile override and cookie behavior."""
        # Doing a request without specifying a mobile querystring
        # parameter should not set a cookie.
        resp = self.client.get('/')
        assert MOBILE_COOKIE not in resp.cookies

        # Doing a request and specifying the mobile querystring
        # parameter should persist that value in the MOBILE cookie.
        resp = self.client.get('/', {
            'mobile': 1
        })
        assert MOBILE_COOKIE in resp.cookies
        eq_(resp.cookies[MOBILE_COOKIE].value, 'yes')

        resp = self.client.get('/', {
            'mobile': 0
        })
        assert MOBILE_COOKIE in resp.cookies
        eq_(resp.cookies[MOBILE_COOKIE].value, 'no')
