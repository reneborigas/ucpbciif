from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from loans.models import AmortizationStatus, Amortization, AmortizationItem, Status
from users.models import CustomUser
from django.db.models import Q

# from borrowers.serializers import BorrowerSerializer

from loans import PMT


def excludeWeekends(amortizationItems):

    for amortizationItem in amortizationItems.all():
        print("weekno")
        print(amortizationItem.schedule)

        weekno = amortizationItem.schedule.weekday()
        print(weekno)
        print("weekno")

        if weekno == 5:
            amortizationItem.schedule = amortizationItem.schedule + timezone.timedelta(days=2)
        if weekno == 6:
            amortizationItem.schedule = amortizationItem.schedule + timezone.timedelta(days=1)

        amortizationItem.save()


def generateAmortizationSchedule(loan, lastPayment, currentAmortization):
    paidItems = loan.amortizations.filter(amortizationStatus__name="PAID").count()

    cycle = currentAmortization.cycle
    termDays = currentAmortization.termDays

    schedule = loan.dateReleased + timezone.timedelta(days=loan.term.principalPaymentPeriod.paymentCycle)
    noOfPaymentSchedules = termDays / cycle
    pmt = PMT()

    print(pmt.payment)
    print(pmt.nextStartingValue)
    print(pmt.interest)
    print(pmt.principal)

    loanAmount = loan.amount

    amortization = Amortization(
        loan=loan,
        # dateReleased = loan.dateReleased  + timezone.timedelta(days=1),
        dateReleased=loan.dateReleased,
        amortizationStatus=AmortizationStatus.objects.get(pk=1),
        createdBy=CustomUser.objects.get(pk=1),
        schedules=noOfPaymentSchedules,
        cycle=cycle,
        termDays=termDays,
    )
    amortization.save()

    currentAmortization.amortizationItems.all()

    # for i in range(int(noOfPaymentSchedules)):
    i = 1
    loanAmount = lastPayment.outStandingBalance

    for amortizationItem in currentAmortization.amortizationItems.order_by("id").all():
        print(currentAmortization.amortizationItems.all().count())
        print("count")
        print(amortizationItem.total)

        print(paidItems)
        print(i)
        print("heres")
        if i <= (paidItems):

            print(loanAmount)
            print("pasok")
            amortizationItem.amortization = amortization
            payments = amortizationItem.payments.all()

            amortizationItem.pk = None
            if i == (paidItems):
                amortizationItem.principalBalance = loanAmount
                # amortizationItem.total =  lastPayment.total - ( lastPayment.additionalInterest + lastPayment.penalty )
                # amortizationItem.days =  lastPayment.days
                amortizationItem.days = cycle

                amortizationItem.schedule = schedule
                # amortizationItem.principal = lastPayment.principal
                # amortizationItem.interest = lastPayment.interest
                amortizationItem.daysExceed = lastPayment.daysExceed
                amortizationItem.daysAdvanced = lastPayment.daysAdvanced
                amortizationItem.additionalInterest = lastPayment.additionalInterest
                amortizationItem.penalty = lastPayment.penalty
                lastCheck = amortizationItem.getPDC()

                print(lastCheck)
                if lastCheck:
                    lastCheck.amortizationItem = amortizationItem
                    lastCheck.save()
                # print(lastPayment.balance)
                # if lastPayment.balance > 0:
                #     print(lastPayment.balance)
                #     print("balance2")
                #     amortizationItem.amortizationStatus = AmortizationStatus.objects.get(pk=3) #partial
                #     amortizationItem.principal = lastPayment.balance
                #     amortizationItem.interest = principalBalance * (loan.interestRate.interestRate/100) * loan.term.paymentPeriod.paymentCycle/360

            amortizationItem.save()
            lastPayment.amortizationItem = amortizationItem
            lastPayment.save()

            for payment in payments:
                payment.amortizationItem = amortizationItem
                payment.save()

            # schedule = lastPayment.datePayment
        else:
            if loanAmount > 0:
                pmt = pmt.getPayment(
                    loanAmount,
                    loan.interestRate.interestRate,
                    termDays,
                    noOfPaymentSchedules,
                    noOfPaymentSchedules - (i - 1),
                )
                lastPayment = schedule - timezone.timedelta(days=cycle)

                dayTillCutOff = cycle - int(lastPayment.strftime("%d"))

                accruedInterest = (int(pmt.principal)) * (loan.interestRate.interestRate / 100) * dayTillCutOff / 360

                amortizationItem = AmortizationItem(
                    schedule=schedule,
                    amortization=amortization,
                    days=cycle,
                    principal=pmt.principal,
                    deductAccruedInterest=pmt.interest - accruedInterest,
                    accruedInterest=accruedInterest,
                    interest=pmt.interest,
                    additionalInterest=0,
                    penalty=0,
                    vat=0,
                    total=pmt.payment,
                    principalBalance=pmt.nextStartingValue,
                    amortizationStatus=AmortizationStatus.objects.get(pk=1),
                )
                amortizationItem.save()
                loanAmount = pmt.nextStartingValue
            else:
                amortizationItem = AmortizationItem(
                    schedule=schedule,
                    amortization=amortization,
                    days=cycle,
                    principal=0,
                    accruedInterest=0,
                    deductAccruedInterest=0,
                    interest=0,
                    vat=0,
                    total=0,
                    principalBalance=0,
                    amortizationStatus=AmortizationStatus.objects.get(pk=1),
                )

                amortizationItem.save()
        schedule = schedule + timezone.timedelta(days=cycle)
        i = i + 1


# def generateAmortizationSchedule(loan,request):


#     noOfPrincipalPaymentSchedules = loan.term.days / loan.term.principalPaymentPeriod.paymentCycle
#     # noOfPaymentSchedules = loan.term.days / loan.term.paymentPeriod.paymentCycle
#     noOfInterestPaymentSchedules = loan.term.days / loan.term.interestPaymentPeriod.paymentCycle

#     if noOfPrincipalPaymentSchedules > noOfInterestPaymentSchedules:

#         noOfPaymentSchedules = noOfPrincipalPaymentSchedules

#     else:
#         noOfPaymentSchedules = noOfInterestPaymentSchedules

#     cycle = loan.term.interestPaymentPeriod.paymentCycle

#     schedule = loan.dateReleased  + timezone.timedelta(days=cycle)

#     pmt = PMT()
#     pmtInterest = PMT()
#     print(pmt.payment)
#     print(pmt.nextStartingValue)
#     print(pmt.interest)
#     print(pmt.principal)

#     loanAmount = loan.amount

#     amortization = Amortization(
#             loan = loan,
#             dateReleased = loan.dateReleased  ,
#             # dateReleased = loan.dateReleased  + timezone.timedelta(days=1),
#             amortizationStatus = AmortizationStatus.objects.get(pk=1),
#             createdBy = request.user,
#             schedules = noOfPaymentSchedules,
#             cycle = cycle,
#             termDays = loan.term.days
#         )
#     amortization.save()
#     currentCycle = 1
#     interestLoan = loan.amount
#     for i in range(int(noOfPaymentSchedules)):

#         pmt = pmt.getPayment(loanAmount,loan.interestRate.interestRate,loan.term.days,noOfPaymentSchedules,noOfPaymentSchedules - i)
#         principaEntry = 0
#         pmtInterest = pmtInterest.getPayment(interestLoan,loan.interestRate.interestRate,loan.term.days,noOfPaymentSchedules,noOfPaymentSchedules - i)
#         if (cycle  *  (i+1)) == (loan.term.principalPaymentPeriod.paymentCycle * currentCycle) :
#         # if i+1 == int(noOfPaymentSchedules)/ int(noOfPrincipalPaymentSchedules):

#             # pmtPrincipal = pmt.getPayment(loanAmount,loan.interestRate.interestRate,loan.term.days,noOfPrincipalPaymentSchedules,noOfPrincipalPaymentSchedules - i)

#             principaEntry = int(loan.amount) / noOfPrincipalPaymentSchedules
#         print(i)
#         amortizationItem = AmortizationItem(
#             schedule = schedule,
#             amortization = amortization,
#             days= cycle,
#             principal = principaEntry,
#             interest = pmtInterest.interest,
#             additionalInterest = 0,
#             penalty = 0,
#             vat = 0,
#             total = int(principaEntry) + pmtInterest.interest,
#             principalBalance = pmt.nextStartingValue,
#             amortizationStatus = AmortizationStatus.objects.get(pk=1),
#         )
#         amortizationItem.save()

#         schedule = schedule + timezone.timedelta(days=cycle)
#         loanAmount = pmt.nextStartingValue

#         if (cycle  *  (i+1)) == (loan.term.principalPaymentPeriod.paymentCycle * currentCycle) :
#         # if i+1 == int(noOfPaymentSchedules)/ int(noOfPrincipalPaymentSchedules):
#             # loanAmount = pmt.nextStartingValue

#             currentCycle  = currentCycle + 1
#             interestLoan = int(principaEntry)
# excludeWeekends(amortization.amortizationItems)
def generateUnevenAmortizationSchedule(loan, lastPayment, currentAmortization):
    paidItems = loan.amortizations.filter(amortizationStatus__name="PAID").count()

    # cycle = currentAmortization.cycle
    # termDays = currentAmortization.termDays

    # schedule = loan.dateReleased  + timezone.timedelta(days=loan.term.principalPaymentPeriod.paymentCycle)
    # noOfPaymentSchedules = termDays/cycle
    # pmt = PMT()

    # print(pmt.payment)
    # print(pmt.nextStartingValue)
    # print(pmt.interest)
    # print(pmt.principal)

    # loanAmount = loan.amount

    # amortization = Amortization(
    #         loan = loan,
    #         # dateReleased = loan.dateReleased  + timezone.timedelta(days=1),
    #         dateReleased = loan.dateReleased ,
    #         amortizationStatus = AmortizationStatus.objects.get(pk=1),
    #         createdBy = CustomUser.objects.get(pk=1),
    #         schedules = noOfPaymentSchedules,
    #         cycle = cycle,
    #         termDays = termDays
    #     )
    # amortization.save()

    currentAmortization.amortizationItems.all()

    # for i in range(int(noOfPaymentSchedules)):
    i = 1

    noOfPrincipalPaymentSchedules = loan.term.days / loan.term.principalPaymentPeriod.paymentCycle
    # noOfPaymentSchedules = loan.term.days / loan.term.paymentPeriod.paymentCycle
    noOfInterestPaymentSchedules = loan.term.days / loan.term.interestPaymentPeriod.paymentCycle

    if noOfPrincipalPaymentSchedules > noOfInterestPaymentSchedules:

        noOfPaymentSchedules = noOfPrincipalPaymentSchedules

    else:
        noOfPaymentSchedules = noOfInterestPaymentSchedules

    cycle = loan.term.interestPaymentPeriod.paymentCycle

    schedule = loan.dateReleased + timezone.timedelta(days=cycle)

    pmt = PMT()
    pmtInterest = PMT()
    print(pmt.payment)
    print(pmt.nextStartingValue)
    print(pmt.interest)
    print(pmt.principal)

    loanAmount = loan.amount

    amortization = Amortization(
        loan=loan,
        dateReleased=loan.dateReleased,
        # dateReleased = loan.dateReleased  + timezone.timedelta(days=1),
        amortizationStatus=AmortizationStatus.objects.get(pk=1),
        createdBy=CustomUser.objects.get(pk=1),
        schedules=noOfPaymentSchedules,
        cycle=cycle,
        termDays=loan.term.days,
    )
    amortization.save()
    currentCycle = 1
    interestLoan = loan.amount
    loanAmount = lastPayment.outStandingBalance
    for amortizationItem in currentAmortization.amortizationItems.order_by("id").all():
        print(currentAmortization.amortizationItems.all().count())
        print("count")
        print(amortizationItem.total)

        print(paidItems)
        print(i)
        print("heres")
        if i <= (paidItems):

            print(loanAmount)
            print("pasok")
            amortizationItem.amortization = amortization
            payments = amortizationItem.payments.all()

            amortizationItem.pk = None
            if i == (paidItems):
                amortizationItem.principalBalance = loanAmount
                # amortizationItem.total =  lastPayment.total - ( lastPayment.additionalInterest + lastPayment.penalty )
                # amortizationItem.days =  lastPayment.days
                amortizationItem.days = cycle

                amortizationItem.schedule = schedule
                # amortizationItem.principal = lastPayment.principal
                # amortizationItem.interest = lastPayment.interest
                amortizationItem.daysExceed = lastPayment.daysExceed
                amortizationItem.daysAdvanced = lastPayment.daysAdvanced
                amortizationItem.additionalInterest = lastPayment.additionalInterest
                amortizationItem.penalty = lastPayment.penalty

                lastCheck = amortizationItem.getPDC()
                print(lastCheck)
                if lastCheck:
                    lastCheck.amortizationItem = amortizationItem
                    lastCheck.save()

                # print(lastPayment.balance)
                # if lastPayment.balance > 0:
                #     print(lastPayment.balance)
                #     print("balance2")
                #     amortizationItem.amortizationStatus = AmortizationStatus.objects.get(pk=3) #partial
                #     amortizationItem.principal = lastPayment.balance
                #     amortizationItem.interest = principalBalance * (loan.interestRate.interestRate/100) * loan.term.paymentPeriod.paymentCycle/360

            amortizationItem.save()
            lastPayment.amortizationItem = amortizationItem
            lastPayment.save()

            for payment in payments:
                payment.amortizationItem = amortizationItem
                payment.save()

            # schedule = lastPayment.datePayment
        else:
            if loanAmount > 0:
                pmt = pmt.getPayment(
                    loanAmount,
                    loan.interestRate.interestRate,
                    loan.term.days,
                    noOfPaymentSchedules,
                    noOfPaymentSchedules - (i - 1),
                )
                principaEntry = 0
                pmtInterest = pmtInterest.getPayment(
                    interestLoan,
                    loan.interestRate.interestRate,
                    loan.term.days,
                    noOfPaymentSchedules,
                    noOfPaymentSchedules - (i - 1),
                )
                if (cycle * (i)) == (loan.term.principalPaymentPeriod.paymentCycle * currentCycle):
                    # if i+1 == int(noOfPaymentSchedules)/ int(noOfPrincipalPaymentSchedules):

                    # pmtPrincipal = pmt.getPayment(loanAmount,loan.interestRate.interestRate,loan.term.days,noOfPrincipalPaymentSchedules,noOfPrincipalPaymentSchedules - i)

                    principaEntry = int(loan.amount) / noOfPrincipalPaymentSchedules
                print(i)
                lastPayment = schedule - timezone.timedelta(days=cycle)

                dayTillCutOff = cycle - int(lastPayment.strftime("%d"))

                accruedInterest = (int(pmt.principal)) * (loan.interestRate.interestRate / 100) * dayTillCutOff / 360

                amortizationItem = AmortizationItem(
                    schedule=schedule,
                    amortization=amortization,
                    days=cycle,
                    principal=principaEntry,
                    deductAccruedInterest=pmtInterest.interest - accruedInterest,
                    accruedInterest=accruedInterest,
                    interest=pmtInterest.interest,
                    additionalInterest=0,
                    penalty=0,
                    vat=0,
                    total=int(principaEntry) + pmtInterest.interest,
                    principalBalance=pmt.nextStartingValue,
                    amortizationStatus=AmortizationStatus.objects.get(pk=1),
                )
                amortizationItem.save()

                schedule = schedule + timezone.timedelta(days=cycle)
                loanAmount = pmt.nextStartingValue

                if (cycle * (i)) == (loan.term.principalPaymentPeriod.paymentCycle * currentCycle):
                    # if i+1 == int(noOfPaymentSchedules)/ int(noOfPrincipalPaymentSchedules):
                    # loanAmount = pmt.nextStartingValue

                    currentCycle = currentCycle + 1
                    interestLoan = int(principaEntry)
            else:
                amortizationItem = AmortizationItem(
                    schedule=schedule,
                    amortization=amortization,
                    days=cycle,
                    principal=0,
                    interest=0,
                    accruedInterest=0,
                    deductAccruedInterest=0,
                    vat=0,
                    total=0,
                    principalBalance=0,
                    amortizationStatus=AmortizationStatus.objects.get(pk=1),
                )

                amortizationItem.save()
        schedule = schedule + timezone.timedelta(days=cycle)
        i = i + 1
    # excludeWeekends(amortization.amortizationItems)


class CheckSerializer(ModelSerializer):
    borrowerName = serializers.CharField(read_only=True)
    checkStatusText = serializers.CharField(read_only=True)

    def create(self, validated_data):
        check = Check.objects.create(**validated_data)

        return check

    def update(self, instance, validated_data):

        return instance

    class Meta:
        model = Check
        fields = "__all__"


class CheckStatusSerializer(ModelSerializer):
    def create(self, validated_data):
        checkStatus = CheckStatus.objects.create(**validated_data)

        return checkStatus

    def update(self, instance, validated_data):

        return instance

    class Meta:
        model = CheckStatus
        fields = "__all__"


class PaymentStatusSerializer(ModelSerializer):
    def create(self, validated_data):
        paymentStatus = PaymentStatus.objects.create(**validated_data)

        return paymentStatus

    def update(self, instance, validated_data):

        return instance

    class Meta:
        model = PaymentStatus
        fields = "__all__"


class PaymentTypeSerializer(ModelSerializer):
    def create(self, validated_data):
        paymentType = PaymentType.objects.create(**validated_data)

        return paymentType

    def update(self, instance, validated_data):

        return instance

    class Meta:
        model = PaymentType
        fields = "__all__"


class FilteredPaymentSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by("id")
        return super(FilteredPaymentSerializer, self).to_representation(data)


class PaymentSerializer(ModelSerializer):
    paymentType_name = serializers.ReadOnlyField(source="paymentType.name")
    paymentStatus_name = serializers.ReadOnlyField(source="paymentStatus.name")
    amortizationItem_schedule = serializers.ReadOnlyField(source="amortizationItem.schedule")
    amortizationItem_principal = serializers.ReadOnlyField(source="amortizationItem.principal")
    amortizationItem_interest = serializers.ReadOnlyField(source="amortizationItem.interest")
    paidInterest = serializers.ReadOnlyField(source="amortizationItem.interest")
    # amortizationItem_additional_interest = serializers.ReadOnlyField(source='amortizationItem.additionalInterest')
    # amortizationItem_penalty = serializers.ReadOnlyField(source='amortizationItem.penalty')
    # amortizationItem_total_with_penalty = serializers.ReadOnlyField(source='amortizationItem.totalToPayWithPenalty')

    amortizationItem_total = serializers.ReadOnlyField(source="amortizationItem.totalToPay")
    borrowerName = serializers.CharField(read_only=True)
    pnNo = serializers.CharField(read_only=True)

    borrower_id = serializers.ReadOnlyField(source="loan.borrower.borrowerId")
    # loan_no  = serializers.ReadOnlyField(source='amortizationItem.total')

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)

        if payment.balance <= 0:

            # payment.amortization.amortizationStatus = AmortizationStatus.objects.get(pk=2) #paid
            amortizationItemCurrent = payment.loan.getCurrentAmortizationItem()
            amortizationItem = AmortizationItem.objects.get(pk=amortizationItemCurrent.pk)
            amortizationItem.amortizationStatus = AmortizationStatus.objects.get(pk=2)  # paid
            # amortizationItem.principal = payment.principal
            # amortizationItem.daysAdvanced = payment.daysAdvanced
            # amortizationItem.additionalInterest = payment.additionalInterest
            # amortizationItem.penalty = payment.penalty
            amortizationItem.save()
        payment.amortization.save()

        # payment.loan.getCurrentAmortizationItem.amortizationStatus  = AmortizationStatus.objects.get(pk=2)
        # payment.loan.getCurrentAmortizationItem.save()

        # payment.amortization.amortizationItems.update(amortizationStatus=AmortizationStatus.objects.get(pk=2))
        if payment.balance >= 1:
            print("payment new")
            amortizationItemCurrent = payment.loan.getCurrentAmortizationItem()
            amortizationItem = AmortizationItem.objects.get(pk=amortizationItemCurrent.pk)
            amortizationItem.amortizationStatus = AmortizationStatus.objects.get(pk=3)  # partial
            # amortizationItem.principal = amortizationItem.principal
            # amortizationItem.interest = payment.interestPayment
            # amortizationItem.accruedInterest = payment.accruedInterestPayment
            # amortizationItem.total = amortizationItem.interest + amortizationItem.principal
            print(amortizationItem.principal)
            print("amortizationItem.principal")
            amortizationItem.save()
        # else:
        #     payment.amortization.amortizationItems.update(amortizationStatus=AmortizationStatus.objects.get(pk=2))
        #     if payment.loan.term.principalPaymentPeriod == payment.loan.term.interestPaymentPeriod:

        #         generateAmortizationSchedule(payment.loan,payment,payment.amortization)
        #     else:
        #         generateUnevenAmortizationSchedule(payment.loan,payment,payment.amortization)
        # else:
        #
        # if payment.overPayment >= 1:
        #     print("payment over")
        #     amortizationItemCurrent = payment.loan.getCurrentAmortizationItem()

        #     amortizationItems = AmortizationItem.objects.filter(amortization=amortizationItemCurrent.amortization,principal__gt=0,amortizationStatus=1).order_by('id').first()
        #     print(amortizationItems)
        #     if amortizationItems:
        #         amortizationItems.principal = principal - payment.overPayment
        #         amortizationItems.save()

        return payment

    def update(self, instance, validated_data):
        instance.paymentType = validated_data.get("paymentType", instance.paymentType)
        instance.paymentStatus = validated_data.get("paymentStatus", instance.paymentStatus)

        instance.save()
        return instance

    class Meta:
        list_serializer_class = FilteredPaymentSerializer
        model = Payment
        fields = "__all__"
