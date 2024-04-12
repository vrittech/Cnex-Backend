from rest_framework import serializers
from ..models import ShippingAddress
from ..utilities.permission import SecureFields
from accounts import roles

class ShippingAddressReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class ShippingAddressWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

    def get_fields(self):
        model_fields = super().get_fields()
        SecureFields(self,model_fields,['profile'],['PATCH','PUT'],[roles.ADMIN,roles.SUPER_ADMIN])
        # SecureFields(self,model_fields,['provider'],['PATCH','PUT'],[]) #if empty [] it means it is striction for all
        return model_fields
    
    