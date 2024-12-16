import logging

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .serializers import PaymentSerializer, RequestAntecipationSerializer
from .tasks import send_payment_email

logger = logging.getLogger("payments")


class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request):
        logger.info(f"Usuário {request.user} acessou a lista de pagamentos")
        return Response({"message": "Lista de pagamentos"})

    def get_queryset(self):
        """
        Filters payments so that each user can only see payments from their
        own vendors.
        """
        user = self.request.user
        return Payment.objects.filter(vendor__user=user)


class RequestAntecipation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"Usuário {request.user} acessou a aba de antecipação")
        return Response({"message": "Lista de antecipação"})

    def post(self, request):
        serializer = RequestAntecipationSerializer(data=request.data)
        if serializer.is_valid():
            payment_id = serializer.validated_data["payment_id"]
            try:
                payment = Payment.objects.get(
                    id=payment_id, vendor__user=request.user
                )

                if payment.status != Payment.AVAILABLE:
                    return Response(
                        {
                            "message": "Pagamento não disponível para antecipação."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                payment.status = Payment.ADVANCED
                payment.save()

                send_payment_email.delay(payment_id, "antecipado")

                return Response(
                    {
                        "message": "Solicitação de antecipação realizada com sucesso."
                    },
                    status=status.HTTP_200_OK,
                )
            except Payment.DoesNotExist:
                return Response(
                    {
                        "message": "Pagamento não encontrado ou não pertence ao usuário."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
