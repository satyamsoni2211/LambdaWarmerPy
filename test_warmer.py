from unittest.mock import patch, Mock
from unittest import TestCase
from warmer import warmer


@warmer(_concurrency=5)
def fake(*args, **kwargs):
    return "_response"


class TestWarmerFunction(TestCase):
    @patch("botocore.client.BaseClient._make_api_call")
    def test_warmer_concurrency(self, mock: Mock):

        # checking call for warmer event
        response = fake({"warmer": True}, {})
        mock.assert_called()
        print(mock.call_args_list)
        self.assertEqual(mock.call_count, 4)
        self.assertIn("statusCode", response)

        # testing call being passed to function on no warmer event
        self.assertAlmostEqual("_response", fake({}, {}))
