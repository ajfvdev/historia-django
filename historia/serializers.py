from rest_framework.serializers import ModelSerializer
from .models import Contract, Rate

class ContractSearializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        
class RatesSearializer(ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'