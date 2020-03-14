from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'url']

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, user, validated_data):
        user.username = validated_data.get('username', user.username)
        
        if(validated_data.get('password')):
            user.set_password(validated_data['password'])

        user.save()

        return user