from warmer import warmer
from unittest import TestCase
from unittest.mock import patch, Mock


@warmer(_concurrency=5)
def fake_wsgi(*args, **kwargs):
    return "_response"


@warmer()
def fake_wsgi_with_concurrency_event(*args, **kwargs):
    return "_response"


class TestWarmerFunction(TestCase):
    @patch("botocore.client.BaseClient._make_api_call")
    def test_warmer_concurrency(self, mock: Mock):
        # checking call for warmer event
        response = fake_wsgi({"warmer": True}, {})
        mock.assert_called()
        self.assertEqual(mock.call_count, 4)
        self.assertIn("statusCode", response)

    @patch("botocore.client.BaseClient._make_api_call")
    def test_warmer_response_body(self, mock: Mock):
        # checking call for warmer event
        response = fake_wsgi({"warmer": True}, {})
        self.assertIn("statusCode", response)
        self.assertIn("isBase64Encoded", response)
        body = response.get("body")
        self.assertIn("eventFlag", body)
        self.assertEqual("warmed up", body.get("status"))

    def test_wsgi_function_response(self):
        # testing call being passed to function on no warmer event
        self.assertAlmostEqual("_response", fake_wsgi({}, {}))

    @patch("warmer.call_function_concurrently")
    def test_concurrency_function_args(self, mock: Mock):
        # function should be passed with same flag
        # with is an indetifier for the
        # warming event
        fake_wsgi({"warmer": True}, {})
        mock.assert_called()
        mock.assert_called_with(5, "warmer")

    @patch("botocore.client.BaseClient._make_api_call")
    def test_for_concurrency_using_event(self, mock: Mock):
        # function to check for concurrent calls when passed via event
        fake_wsgi_with_concurrency_event(
            {"warmer": True, "concurrency": 5}, {})
        self.assertEqual(mock.call_count, 4)

    @patch("botocore.client.BaseClient._make_api_call")
    def test_for_concurrency_using_default_event(self, mock: Mock):
        # No concurrent calls should be made in case
        # of concurrency = 1
        fake_wsgi_with_concurrency_event(
            {"warmer": True}, {})
        self.assertEqual(mock.call_count, 0)
        mock.assert_not_called()
