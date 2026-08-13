from rest_framework import status
from rest_framework.test import APITestCase

from common.responses import success_response


class SuccessResponseTests(APITestCase):

    def test_success_response(self):
        response = success_response(
            data={"id": 1},
            message="User retrieved successfully.",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data,
            {
                "statusCode": 200,
                "message": "User retrieved successfully.",
                "data": {"id": 1},
            },
        )

    def test_created_response(self):
        response = success_response(
            data={"id": 1},
            message="User created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["statusCode"],
            201,
        )