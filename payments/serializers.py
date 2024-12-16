from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """

    class Meta:
        model = Payment
        fields = "__all__"


class RequestAntecipationSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()

    def validate_payment_id(self, value):
        """
        Verifies if the payment exists by payment_id.
        """
        from payments.models import Payment

        try:
            payment = Payment.objects.get(id=value)
        except Payment.DoesNotExist:
            raise serializers.ValidationError("Pagamento não encontrado.")
        return value
