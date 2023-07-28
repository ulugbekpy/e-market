from rest_framework import serializers
from models import Seller,User

class SellerSavingSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = Seller
        fields = ('id', 'phone', 'password',
                  'first_name', 'last_name', 'certificate', 'address')

    def create(self, validated_data):
        # Get the phone and password from the validated data
        phone = validated_data.pop('phone')
        password = validated_data.pop('password')

        # Check if a user already exists with the given phone
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                "A user with that phone already exists")

        # Create the user
        user = User(phone=phone)
        user.set_password(password)
        user.save()

        # Create the customer
        seller = Seller.objects.create(user=user, **validated_data)

        return seller

    def update(self, instance, validated_data):
        # Get the phone and password from the validated data
        phone = validated_data.pop('phone', None)
        password = validated_data.pop('password', None)

        if phone is not None:
            instance.user.phone = phone
            instance.user.save()

        if password is not None:
            instance.user.set_password(password)
            instance.user.save()

        for key in validated_data:
            setattr(instance, key, validated_data[key])

        return instance


class SellerGetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, source='user.phone')

    class Meta:
        model = Seller
        fields = ('username', 'first_name', 'last_name', 'address')