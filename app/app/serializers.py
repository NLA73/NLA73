from rest_framework import serializers
from .models import User, Resume, BiayaMuat, BiayaBongkar

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nomor_sales', 'email', 'first_name', 'last_name']

class ResumeSerializer(serializers.ModelSerializer):
    pph = serializers.IntegerField(required=False, default=0)
    total_biaya = serializers.IntegerField(required=False, default=0)
    profit = serializers.IntegerField(required=False, default=0)
    
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['user']

class BiayaMuatSerializer(serializers.ModelSerializer):
    total_biaya = serializers.IntegerField(required=False, default=0)
    class Meta:
        model = BiayaMuat
        fields = '__all__'
        read_only_fields = ['user']

class BiayaBongkarSerializer(serializers.ModelSerializer):
    tot_by_bongkar = serializers.IntegerField(required=False, default=0)
    class Meta:
        model = BiayaBongkar
        fields = '__all__'
        read_only_fields = ['user']
