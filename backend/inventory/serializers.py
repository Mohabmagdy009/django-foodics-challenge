# region Imports
from .models import Order, Product, Ingredient, OrderProduct
from django.core.mail import send_mail
from utils.importinglibs.data_manipulation_libs import settings, os, transaction, serializers
# endregion


# region Serializers
class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'products']
        extra_kwargs = {
            'user_id_create': {'required': False},
            'user_id_update': {'required': False},
        }

    def create(self, validated_data):
        """
        Create an order, check inventory, process each product in the order,
        update ingredient stock, and send email notifications if stock is low.
        """
        try:
            with transaction.atomic():
                stock_limit = float(os.environ.get('STOCK_LIMIT'))  # Retrieve the stock limit (e.g. 0.5)

                # region Step 1: Acquire order data and create the order instance
                products_data = validated_data.pop('products')
                order = Order.objects.create(**validated_data)
                user_id_create, user_id_update = validated_data.pop('user_id_create'), validated_data.pop(
                    'user_id_update')
                # endregion

                # region Step 2: Check inventory before processing the order
                insufficient_ingredients = self.check_inventory(products_data)
                if insufficient_ingredients:
                    raise serializers.ValidationError({
                        'insufficient_stock': f"Insufficient stock for the following ingredients: "
                                              f"{', '.join(insufficient_ingredients)}"
                    })
                # endregion

                # region Step 3: Process each product, update stock, and create OrderProduct entries
                updated_ingredients = []  # List to hold ingredients that need to be updated

                for product_data in products_data:
                    # Fetch the product and its related ingredients
                    product = Product.objects.prefetch_related('productingredient_set__ingredient').get(
                        pk=product_data['product'].id)
                    quantity = product_data['quantity']

                    # Process the ingredients associated with the product
                    for product_ingredient in product.productingredient_set.all():
                        ingredient = product_ingredient.ingredient
                        total_consumption = product_ingredient.quantity * quantity

                        # Update ingredient stock
                        ingredient.stock -= total_consumption
                        ingredient.user_id_update = user_id_update

                        # Check for stock threshold and set the email flag
                        if ingredient.stock < ingredient.stock_initial * stock_limit and not ingredient.email_sent:
                            self.notify_low_stock(ingredient, stock_limit)
                            ingredient.email_sent = True
                        elif ingredient.stock >= ingredient.stock_initial * stock_limit:
                            ingredient.email_sent = False

                        # Add the ingredient to the list of updated ingredients
                        updated_ingredients.append(ingredient)

                    # Create the association between the order and the product
                    OrderProduct.objects.create(order=order, product=product, quantity=quantity,
                                                user_id_create=user_id_create, user_id_update=user_id_update)

                    # Perform a bulk update for all modified ingredients
                    if updated_ingredients:
                        Ingredient.objects.bulk_update(updated_ingredients, ['stock', 'email_sent', 'user_id_update'])
                        updated_ingredients = []

                return order
                # endregion

        except Exception as e:
            # Catch any exception during the order creation and raise a validation error
            raise serializers.ValidationError(f"Error occurred while creating the order: {e}")

    # region Inventory Check Method
    @staticmethod
    def check_inventory(products_data):
        """
        Checks if the stock is sufficient for each ingredient required in the order.
        Returns a list of ingredient names that have insufficient stock.
        """
        insufficient_ingredients = []

        # Step 1: Track total ingredient consumption across all products in the order
        ingredient_consumption = {}

        # Create a list of product IDs to avoid querying inside the loop
        product_ids = [product_data['product'].id for product_data in products_data]

        # Fetch all products and their related ingredients in one go
        products = Product.objects.prefetch_related('productingredient_set__ingredient').filter(id__in=product_ids)

        # Convert the list of products to a dictionary for faster lookup
        product_dict = {product.id: product for product in products}

        # Step 2: Calculate total ingredient consumption across all products in the order
        for product_data in products_data:
            product = product_dict.get(product_data['product'].id)
            if not product:
                continue  # Skip if product is not found

            quantity = product_data['quantity']

            # Check each product's ingredients and calculate the total consumption
            for product_ingredient in product.productingredient_set.all():
                ingredient = product_ingredient.ingredient
                total_consumption = product_ingredient.quantity * quantity

                # Track the total consumption of each ingredient
                if ingredient.id not in ingredient_consumption:
                    ingredient_consumption[ingredient.id] = 0
                ingredient_consumption[ingredient.id] += total_consumption

        # Step 3: Check if the total consumption exceeds the stock for each ingredient
        for ingredient_id, total_required in ingredient_consumption.items():
            ingredient = Ingredient.objects.get(id=ingredient_id)

            # If the stock is insufficient, add the ingredient to the list
            if ingredient.stock < total_required:
                insufficient_ingredients.append(ingredient.name)

        return insufficient_ingredients

    # endregion

    # region Email Notification Method
    @staticmethod
    def notify_low_stock(ingredient, stock_limit):
        """
        Sends an email notification when the stock for an ingredient is below the defined threshold.
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(
            "Stock Alert",
            f"The stock for {ingredient.name} is below {stock_limit * 100}%.",
            from_email=from_email,
            recipient_list=['merchant@example.com'],
            fail_silently=False,
        )

        # Update the ingredient's email_sent flag to avoid sending duplicate emails
        ingredient.email_sent = True
        ingredient.save()
    # endregion

# endregion
