from rest_framework import serializers
from .models import *


class userDetailsserializers(serializers.ModelSerializer):

    class Meta:
        model = userDetails
        fields = "__all__"


class expenseDetailsserializers(serializers.ModelSerializer):

    class Meta:
        model = expenseDetails
        fields = "__all__"
