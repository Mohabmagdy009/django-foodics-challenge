# region Imports
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product, Ingredient, Order, OrderProduct, ProductIngredient
from utils.models import User
from unittest.mock import patch
# endregion


class OrderTestCase(APITestCase):

    # region Token Retrieval
    def get_token(self, username, password):
        token_response = self.client.post(
            "http://127.0.0.1:8001/utils/api/token/",
            {"email": username, "password": password},
            format="json"
        )
        return token_response

    # endregion

    # region Test Setup: User and Database Setup
    def setUp(self):
        # Create superuser and non-superuser for testing
        self.user_email = "iwanttojoinfoodex@foodex.com"
        self.user_password = "accept_me_in_foodex"
        user, created = User.objects.get_or_create(
            email=self.user_email,
            defaults={"first_name": "Mohab", "last_name": "Abbas", "is_superuser": True, "phone": "+201159119534"}
        )
        user.set_password(self.user_password)
        user.save()

        # Create a non-superuser for permission testing
        self.user_email_disable = "cannotaccess@foodex.com"
        self.user_password_disable = "reject_me_in_foodex"
        user_disable, created = User.objects.get_or_create(
            email=self.user_email_disable,
            defaults={"first_name": "Ahmed", "last_name": "Ali", "is_superuser": False, "phone": "+201159119633"}
        )
        user_disable.set_password(self.user_password_disable)
        user_disable.save()

        # Seed the database with ingredients and products
        user_create_and_update = {"user_id_create": user, "user_id_update": user}
        self.beef = Ingredient.objects.create(name="beef", stock=20000, **user_create_and_update)
        self.cheese = Ingredient.objects.create(name="cheese", stock=5000, **user_create_and_update)
        self.onion = Ingredient.objects.create(name="onion", stock=1000, **user_create_and_update)

        # Create product and associate ingredients
        self.burger = Product.objects.create(name="burger", **user_create_and_update)
        ProductIngredient.objects.create(product=self.burger, ingredient=self.beef, quantity=150,
                                         **user_create_and_update)
        ProductIngredient.objects.create(product=self.burger, ingredient=self.cheese, quantity=30,
                                         **user_create_and_update)
        ProductIngredient.objects.create(product=self.burger, ingredient=self.onion, quantity=20,
                                         **user_create_and_update)

        # Endpoint for creating orders
        self.order_url = reverse('order-list')

        # Get authentication token for the superuser
        token_response = self.get_token(self.user_email, self.user_password)
        self.assertEqual(token_response.status_code, 200, "Token retrieval failed")
        self.token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    # endregion

    # region Test Case: Order Creation
    def test_order_creation(self):
        # Payload for order creation
        payload = {"products": [{"product": self.burger.id, "quantity": 2}]}

        # Send POST request to create the order
        response = self.client.post(self.order_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Ensure order creation

        # Verify the order is saved and correct quantity is associated
        order = Order.objects.first()
        self.assertEqual(Order.objects.count(), 1)
        order_product = order.orderproduct_set.all()
        self.assertEqual(order_product.count(), 1)
        self.assertEqual(order_product.first().quantity, 2)

    # endregion

    # region Test Case: Order has no sufficient ingredients
    def test_order_creation(self):
        # Payload for order creation
        payload = {"products": [{"product": self.burger.id, "quantity": 100}]}

        # Send POST request to create the order
        response = self.client.post(self.order_url, payload, format='json')

        # Ensure order failure using status_code and reponse message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient", str(response.data.get('message', '')))

    # endregion

    # region Test Case: Endpoint Permission for Non-Superuser
    def test_endpoint_permission(self):
        # Get token for non-superuser
        token_response = self.get_token(self.user_email_disable, self.user_password_disable)
        self.assertEqual(token_response.status_code, 200, "Token retrieval failed")
        self.token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Attempt to access order creation endpoint as non-superuser
        response = self.client.get(self.order_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # endregion

    # region Test Case: Stock Update After Order
    def test_stock_update_after_order(self):
        # Payload for order creation
        payload = {"products": [{"product": self.burger.id, "quantity": 2}]}

        # Create the order and validate stock update
        self.client.post(self.order_url, payload, format='json')
        self.beef.refresh_from_db()
        self.cheese.refresh_from_db()
        self.onion.refresh_from_db()
        self.assertEqual(self.beef.stock, 20000 - (150 * 2))
        self.assertEqual(self.cheese.stock, 5000 - (30 * 2))
        self.assertEqual(self.onion.stock, 1000 - (20 * 2))

    # endregion

    # region Test Case: Email Notification When Stock Reaches Threshold
    def test_email_notification(self):
        # Reduce stock to trigger email
        self.beef.stock = 10000  # Exactly at 50%
        self.beef.save()

        payload = {"products": [{"product": self.burger.id, "quantity": 1}]}  # Consume 1.5kg

        # Mock email sending function
        with patch('inventory.serializers.OrderSerializer.notify_low_stock') as mock_notify:
            # First order: Email should be triggered
            response = self.client.post(self.order_url, payload, format='json')
            self.assertEqual(response.status_code, 201)
            mock_notify.assert_called_once_with(self.beef, 0.5)

        # Verify the email_sent flag
        self.beef.refresh_from_db()
        self.assertTrue(self.beef.email_sent)

    # endregion

    # region Test Case: Email Triggered Only Once When Stock Goes Below 50%
    def test_email_sent_only_once_when_below_threshold(self):
        # Set initial stock to 50%
        self.beef.stock = 10000
        self.beef.save()

        # Payloads for testing
        payload_1 = {"products": [{"product": self.burger.id, "quantity": 1}]}  # Consume 150g
        payload_2 = {"products": [{"product": self.burger.id, "quantity": 2}]}  # Consume 300g

        # Mock email sending function
        with patch('inventory.serializers.OrderSerializer.notify_low_stock') as mock_notify:
            # First order: Email should be triggered
            response_1 = self.client.post(self.order_url, payload_1, format='json')
            self.assertEqual(response_1.status_code, 201)
            mock_notify.assert_called_once_with(self.beef, 0.5)

            # Second order: Email should not be triggered
            response_2 = self.client.post(self.order_url, payload_2, format='json')
            self.assertEqual(response_2.status_code, 201)
            mock_notify.assert_called_once()  # Ensure no additional email sent

        # Validate stock update
        self.beef.refresh_from_db()
        expected_stock = 10000 - (150 + 300)
        self.assertEqual(self.beef.stock, expected_stock)

    # endregion

    # region Test Case: Email Triggered on Stock Fluctuations
    def test_email_triggered_on_stock_fluctuation(self):
        # Set initial stock above 50%
        self.beef.stock = 10400
        self.beef.save()

        # Payloads for multiple orders
        payload_1 = {"products": [{"product": self.burger.id, "quantity": 3}]}  # Consume 450g
        payload_2 = {"products": [{"product": self.burger.id, "quantity": 1}]}  # Consume 150g
        payload_3 = {"products": [{"product": self.burger.id, "quantity": 10}]}  # Consume 1500g

        with patch('inventory.serializers.OrderSerializer.notify_low_stock') as mock_notify:
            # First order: Email should be triggered
            response_1 = self.client.post(self.order_url, payload_1, format='json')
            self.assertEqual(response_1.status_code, 201)
            mock_notify.assert_called_once_with(self.beef, 0.5)

            # Replenish stock above 50%
            self.beef.stock = 11000
            self.beef.save()

            # Second order: No email should be triggered
            response_2 = self.client.post(self.order_url, payload_2, format='json')
            self.assertEqual(response_2.status_code, 201)
            mock_notify.assert_called_once()

            # Third order: Email should be triggered again
            response_3 = self.client.post(self.order_url, payload_3, format='json')
            self.assertEqual(response_3.status_code, 201)
            self.assertEqual(mock_notify.call_count, 2)
    # endregion
