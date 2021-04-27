from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import (
    Prefetch,
    F,
    Case,
    When,
    Value as V,
    Count,
    Sum,
    ExpressionWrapper,
    OuterRef,
    Subquery,
    Func,
)
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat
from rest_framework import status, views
from rest_framework.response import Response


class CheckViewSet(ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Check.objects.annotate(
            checkStatusText=F("checkStatus__name"),
            borrowerName=Case(
                When(
                    Q(loan__borrower__recordType="BD"),
                    then=F("loan__borrower__business__tradeName"),
                ),
                When(
                    Q(loan__borrower__recordType="ID"),
                    then=Concat(
                        F("loan__borrower__individual__firstname"),
                        V(" "),
                        F("loan__borrower__individual__middlename"),
                        V(" "),
                        F("loan__borrower__individual__lastname"),
                    ),
                ),
            ),
        ).order_by("id")
        checkId = self.request.query_params.get("checkId", None)

        borrowerId = self.request.query_params.get("borrowerId", None)
        dateReceivedFrom = self.request.query_params.get("dateReceivedFrom", None)
        dateReceivedTo = self.request.query_params.get("dateReceivedTo", None)
        pnNo = self.request.query_params.get("pnNo", None)
        bankBranch = self.request.query_params.get("bankBranch", None)
        checkNo = self.request.query_params.get("checkNo", None)
        accountNo = self.request.query_params.get("accountNo", None)
        checkDateFrom = self.request.query_params.get("checkDateFrom", None)
        checkDateTo = self.request.query_params.get("checkDateTo", None)
        amountFrom = self.request.query_params.get("amountFrom", None)
        amountTo = self.request.query_params.get("amountTo", None)
        checkStatus = self.request.query_params.get("checkStatus", None)

        if checkId is not None:
            queryset = queryset.filter(id=checkId)

        if borrowerId is not None:
            queryset = queryset.filter(loan__borrower=borrowerId)

        if dateReceivedFrom is not None and dateReceivedTo is not None:
            queryset = queryset.filter(dateReceived__date__gte=dateReceivedFrom).filter(
                dateReceived__date__lte=dateReceivedTo
            )

        if pnNo is not None:
            queryset = queryset.filter(pnNo=pnNo)

        if bankBranch is not None:
            queryset = queryset.filter(bankBranch=bankBranch)

        if checkNo is not None:
            queryset = queryset.filter(checkNo=checkNo)

        if accountNo is not None:
            queryset = queryset.filter(accountNo=accountNo)

        if checkDateFrom is not None and checkDateTo is not None:
            queryset = queryset.filter(checkDate__date__gte=checkDateFrom).filter(checkDate__date__lte=checkDateTo)

        if amountFrom is not None and amountTo is not None:
            queryset = queryset.filter(amount__gte=amountFrom).filter(amount__lte=amountTo)

        if checkStatus is not None:
            queryset = queryset.filter(checkStatus=checkStatus)

        return queryset


class CheckStatusViewSet(ModelViewSet):
    queryset = CheckStatus.objects.all()
    serializer_class = CheckStatusSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PaymentStatusViewSet(ModelViewSet):
    queryset = PaymentStatus.objects.all()
    serializer_class = PaymentStatusSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = PaymentStatus.objects.order_by("id")
        paymentStatusId = self.request.query_params.get("paymentStatusId", None)
        paymentStatusName = self.request.query_params.get("paymentStatusName", None)

        if paymentStatusId is not None:
            queryset = queryset.filter(id=paymentStatusId)

        if paymentStatusName is not None:
            queryset = queryset.filter(name=paymentStatusName)

        return queryset


class PaymentTypeViewSet(ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = PaymentType.objects.order_by("id")
        paymentTypeId = self.request.query_params.get("paymentTypeId", None)
        paymentTypeName = self.request.query_params.get("paymentTypeName", None)

        if paymentTypeId is not None:
            queryset = queryset.filter(id=paymentTypeId)

        if paymentTypeName is not None:
            queryset = queryset.filter(name=paymentTypeName)

        return queryset


class SkipPaymentView(views.APIView):

    # @method_decorator(csrf_protect)
    def post(self, request):

        amortizationItemId = request.data.get("amortizationItemId")

        if amortizationItemId:
            amortizationItem = AmortizationItem.objects.get(pk=amortizationItemId)

            amortizationItem.amortizationStatus = AmortizationStatus.objects.get(pk=7)  # bayanihan
            amortizationItem.save()

            return Response(
                {
                    "message": "Skip Payment",
                    "amortizationItemId": amortizationItemId,
                },
                status=status.HTTP_202_ACCEPTED,
            )

        return Response({"error": "Error on skip payment"}, status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Payment.objects.annotate(
            borrowerName=Case(
                When(Q(loan__borrower__recordType="BD"), then=F("loan__borrower__business__tradeName")),
                When(
                    Q(loan__borrower__recordType="ID"),
                    then=Concat(
                        F("loan__borrower__individual__firstname"),
                        V(" "),
                        F("loan__borrower__individual__middlename"),
                        V(" "),
                        F("loan__borrower__individual__lastname"),
                    ),
                ),
            ),
            pnNo=F("loan__pnNo"),
        ).order_by("id")
        paymentId = self.request.query_params.get("paymentId", None)

        borrowerId = self.request.query_params.get("borrowerId", None)
        principalFrom = self.request.query_params.get("principalFrom", None)
        principalTo = self.request.query_params.get("principalTo", None)

        interestFrom = self.request.query_params.get("interestFrom", None)
        interestTo = self.request.query_params.get("interestTo", None)
        accruedInterestFrom = self.request.query_params.get("accruedInterestFrom", None)
        accruedInterestTo = self.request.query_params.get("accruedInterestTo", None)

        paymentDateFrom = self.request.query_params.get("paymentDateFrom", None)
        paymentDateTo = self.request.query_params.get("paymentDateTo", None)
        totalPaymentFrom = self.request.query_params.get("totalPaymentFrom", None)
        totalPaymentTo = self.request.query_params.get("totalPaymentTo", None)
        paymentType = self.request.query_params.get("paymentType", None)
        status = self.request.query_params.get("status", None)

        if paymentId is not None:
            queryset = queryset.filter(id=paymentId)

        if borrowerId is not None:
            queryset = queryset.filter(borrower__borrowerId=borrowerId)

        if principalFrom is not None and principalTo is not None:
            queryset = queryset.filter(principal__gte=principalFrom).filter(principal__lte=principalTo)

        if interestFrom is not None and interestTo is not None:
            queryset = queryset.filter(interestPayment__gte=interestFrom).filter(interestPayment__lte=interestTo)

        if accruedInterestFrom is not None and accruedInterestTo is not None:
            queryset = queryset.filter(accruedInterestPayment__gte=accruedInterestFrom).filter(
                accruedInterestPayment__lte=accruedInterestTo
            )

        if paymentDateFrom is not None and paymentDateTo is not None:
            queryset = queryset.filter(datePayment__date__gte=paymentDateFrom).filter(
                datePayment__date__lte=paymentDateTo
            )

        if totalPaymentFrom is not None and totalPaymentTo is not None:
            queryset = queryset.filter(total__gte=totalPaymentFrom).filter(total__lte=totalPaymentTo)

        if paymentType is not None:
            queryset = queryset.filter(paymentType__name=paymentType)

        if status is not None:
            queryset = queryset.filter(paymentStatus__name=status)

        for payment in queryset:
            payment.paidInterest = payment.interestPayment + payment.accruedInterestPayment + payment.additionalInterest

        return queryset
