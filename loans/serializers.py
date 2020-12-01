from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    ListSerializer,
)
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from payments.serializers import PaymentSerializer, CheckSerializer
from borrowers.models import Branch

# from documents.serializers import DocumentSerializer
# from borrowers.serializers import BorrowerSerializer
# class LoanAmortizationSerializer(ModelSerializer):
#     # termName = serializers.CharField(read_only=True)
#     loanStatus_name = serializers.ReadOnlyField(source='loanStatus.name')
#     payments = PaymentSerializer(many=True,read_only=True)
#     creditLine_amount= serializers.ReadOnlyField(source='creditLine.amount')
#     creditLine_dateApproved = serializers.ReadOnlyField(source='creditLine.dateApproved')
#     creditLine_dateExpired = serializers.ReadOnlyField(source='creditLine.dateExpired')
#     borrower_name = serializers.ReadOnlyField(source='borrower.cooperative.name')
#     borrower_id = serializers.ReadOnlyField(source='borrower.borrowerId')
#     term_name = serializers.ReadOnlyField(source='term.name')
#     interestRate_amount = serializers.ReadOnlyField(source='interestRate.interestRate')
#     loanProgram_name = serializers.ReadOnlyField(source='loanProgram.name')
#     totalAmortizationInterest = serializers.CharField(read_only=True)
#     totalObligations = serializers.CharField(read_only=True)

#     latestPayment =  PaymentSerializer(read_only=True)

#     outStandingBalance = serializers.CharField(read_only=True)
#     interestBalance= serializers.CharField(read_only=True)

#     totalPayment = serializers.CharField(read_only=True)
#     # loanDocuments = DocumentSerializer(read_only=True,nany=True)

#     # borrower = BorrowerSerializer(read_only=True)
#     def create(self, validated_data):

#         loan = Loan.objects.create(**validated_data)
#         loan.term = loan.creditLine.term
#         loan.save()
#         return loan

#     def update(self, instance, validated_data):
#         # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
#         # instance.loanName = validated_data.get("loanName", instance.loanName)
#         # instance.borrower =  validated_data.get("borrower", instance.borrower)
#         instance.save()

#         return instance

#     class Meta:
#         model = Loan
#         fields = '__all__'


class AmortizationStatusSerializer(ModelSerializer):
    class Meta:
        model = AmortizationStatus
        fields = "__all__"


class LoanStatusSerializer(ModelSerializer):
    class Meta:
        model = LoanStatus
        fields = "__all__"


class CalendarAmortizationItemSerializer(ModelSerializer):
    title = serializers.CharField(read_only=True)
    start = serializers.CharField(read_only=True)
    className = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    url = serializers.CharField(read_only=True)
    backgroundColor = serializers.CharField(read_only=True)

    class Meta:
        model = AmortizationItem
        fields = [
            "title",
            "start",
            "className",
            "description",
            "url",
            "backgroundColor",
        ]

    # class DashboardDataSerialiazer(ModelSerializer):
    #     borrowerCount   = serializers.CharField(read_only=True)
    #     totalPayments = serializers.CharField(read_only=True)
    #     totalLoans = serializers.CharField(read_only=True)
    #     totalBalance = serializers.CharField(read_only=True)

    #     class Meta:
    #         model = Loan
    #         fields =  ['borrowerCount','totalPayments','totalLoans','totalBalance']


class PaymentPeriodSerializer(ModelSerializer):
    def create(self, validated_data):
        paymentPeriod = PaymentPeriod.objects.create(**validated_data)
        return paymentPeriod

    def update(self, instance, validated_data):

        return instance

    class Meta:
        model = PaymentPeriod
        fields = "__all__"


class TermSerializer(ModelSerializer):
    principalPaymentPeriod = PaymentPeriodSerializer(read_only=True)
    interestPaymentPeriod = PaymentPeriodSerializer(read_only=True)
    principalPaymentPeriodName = serializers.CharField(read_only=True)
    interestPaymentPeriodName = serializers.CharField(read_only=True)
    termName = serializers.CharField(read_only=True)

    def create(self, validated_data):
        term = Term.objects.create(**validated_data)

        return term

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.days = validated_data.get("days", instance.days)
        instance.principalPaymentPeriod = validated_data.get("principalPaymentPeriod", instance.principalPaymentPeriod)
        instance.interestPaymentPeriod = validated_data.get("interestPaymentPeriod", instance.interestPaymentPeriod)
        instance.remarks = validated_data.get("remarks", instance.remarks)
        instance.dateUpdated = validated_data.get("dateUpdated", instance.dateUpdated)
        instance.save()

        return instance

    class Meta:
        model = Term
        fields = "__all__"


class CRUDTermSerializer(ModelSerializer):
    def create(self, validated_data):
        term = Term.objects.create(**validated_data)

        return term

    class Meta:
        model = Term
        fields = "__all__"


class InterestRateSerializer(ModelSerializer):
    def create(self, validated_data):
        interestRate = InterestRate.objects.create(**validated_data)
        return interestRate

    def update(self, instance, validated_data):

        return instance

    class Meta:
        model = InterestRate
        fields = "__all__"


class AmortizationItemSerializer(ModelSerializer):
    pnNo = serializers.CharField(read_only=True)
    amortizationStatus_name = serializers.ReadOnlyField(source="amortizationStatus.name")
    loan_id = serializers.ReadOnlyField(source="amortization.loan.id")
    payments = PaymentSerializer(many=True, read_only=True)
    checks = CheckSerializer(many=True, read_only=True)

    totalPayment = serializers.CharField(read_only=True)
    latestCheck = CheckSerializer(read_only=True)

    def create(self, validated_data):
        amortizationitem = AmortizationItem.objects.create(**validated_data)
        return amortizationitem

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance

    class Meta:
        model = AmortizationItem
        fields = "__all__"


class AmortizationSerializer(ModelSerializer):
    pnNo = serializers.CharField(read_only=True)
    amortizationItems = AmortizationItemSerializer(many=True, read_only=True)
    totalAmortizationInterest = serializers.CharField(read_only=True)
    totalAmortizationAccruedInterest = serializers.CharField(read_only=True)

    totalObligations = serializers.CharField(read_only=True)

    totalAmortizationPrincipal = serializers.CharField(read_only=True)

    def create(self, validated_data):
        amortization = Amortization.objects.create(**validated_data)
        return amortization

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance

    class Meta:
        model = Amortization
        fields = "__all__"


class StatusSerializer(ModelSerializer):
    def create(self, validated_data):
        status = Status.objects.create(**validated_data)
        return status

    def update(self, instance, validated_data):
        instance.save()

        return instance

    class Meta:
        model = Status
        fields = "__all__"


class CreditLineSerializer(ModelSerializer):
    term_name = serializers.ReadOnlyField(source="term.name")
    interestRate_amount = serializers.ReadOnlyField(source="interestRate.interestRate")
    status_name = serializers.ReadOnlyField(source="status.name")
    loanProgram_name = serializers.ReadOnlyField(source="loanProgram.name")
    borrower_name = serializers.ReadOnlyField(source="borrower.business.tradeName")
    remainingCreditLine = serializers.CharField(read_only=True)
    totalAvailment = serializers.CharField(read_only=True)

    def create(self, validated_data):
        creditLine = CreditLine.objects.create(**validated_data)
        return creditLine

    def update(self, instance, validated_data):
        instance.save()

        return instance

    class Meta:
        model = CreditLine
        fields = "__all__"


class CreditLineListSerializer(ModelSerializer):
    borrowerName = serializers.CharField(read_only=True)
    statusName = serializers.ReadOnlyField(source="status.name")
    totalAvailment = serializers.CharField(read_only=True)
    totalCreditLineBalance = serializers.CharField(read_only=True)

    class Meta:
        model = CreditLine
        fields = [
            "id",
            "borrowerName",
            "dateCreated",
            "dateApproved",
            "dateExpired",
            "amount",
            "totalAvailment",
            "totalCreditLineBalance",
            "statusName",
        ]


class LoanSerializer(ModelSerializer):
    # termName = serializers.CharField(read_only=True)
    loanStatus_name = serializers.ReadOnlyField(source="loanStatus.name")
    payments = PaymentSerializer(many=True, read_only=True)
    creditLine_amount = serializers.ReadOnlyField(source="creditLine.amount")
    creditLine_dateApproved = serializers.ReadOnlyField(source="creditLine.dateApproved")
    creditLine_dateExpired = serializers.ReadOnlyField(source="creditLine.dateExpired")
    borrower_name = serializers.ReadOnlyField(source="borrower.business.tradeName")
    borrower_id = serializers.ReadOnlyField(source="borrower.borrowerId")
    amortizations = AmortizationSerializer(many=True, read_only=True)
    term_name = serializers.ReadOnlyField(source="term.name")
    interestRate_amount = serializers.ReadOnlyField(source="interestRate.interestRate")
    loanProgram_name = serializers.ReadOnlyField(source="loanProgram.name")
    branch = serializers.CharField(read_only=True)
    totalAmortizationInterest = serializers.CharField(read_only=True)
    totalAmortizationAccruedInterest = serializers.CharField(read_only=True)
    loanTotalAmortizationPrincipal = serializers.CharField(read_only=True)
    totalDraftAmortizationInterest = serializers.CharField(read_only=True)
    totalObligations = serializers.CharField(read_only=True)
    latestAmortization = AmortizationSerializer(read_only=True)
    latestPayment = PaymentSerializer(read_only=True)
    outStandingBalance = serializers.CharField(read_only=True)
    interestBalance = serializers.CharField(read_only=True)
    totalPayment = serializers.CharField(read_only=True)
    totalPrincipalPayment = serializers.CharField(read_only=True)
    totalInterestPayment = serializers.CharField(read_only=True)
    totalAccruedInterestPayment = serializers.CharField(read_only=True)
    totalPenaltyPayment = serializers.CharField(read_only=True)
    totalAdditionalInterestPayment = serializers.CharField(read_only=True)
    totalTotalInterestPayment = serializers.CharField(read_only=True)
    totalPrincipalBalance = serializers.CharField(read_only=True)
    currentAmortizationItem = AmortizationItemSerializer(read_only=True)
    lastAmortizationItem = AmortizationItemSerializer(read_only=True)
    latestDraftAmortization = AmortizationSerializer(read_only=True)
    # loanDocuments = DocumentSerializer(read_only=True,nany=True)
    # status=StatusSerializer(read_only=True)
    term = TermSerializer(read_only=True)
    parentLastDocumentCreditLine = CreditLineSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    # borrower = BorrowerSerializer(read_only=True)
    def create(self, validated_data):

        loan = Loan.objects.create(**validated_data)
        loan.term = loan.creditLine.term
        loan.save()
        return loan

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance

    class Meta:
        model = Loan
        fields = "__all__"


class LoanProgramDistributionSerializer(ModelSerializer):
    values = serializers.ListField(read_only=True)
    text = serializers.CharField(read_only=True)

    def create(self, validated_data):
        loanProgram = LoanProgram.objects.create(**validated_data)
        return loanProgram

    def update(self, instance, validated_data):
        return instance

    class Meta:
        model = LoanProgram
        fields = ["text", "values"]


class LoanProgramSerializer(ModelSerializer):
    activeLoan = LoanSerializer(read_only=True)
    activeCreditLine = CreditLineSerializer(read_only=True)
    totalAvailments = serializers.CharField(read_only=True)
    overallLoan = serializers.CharField(read_only=True)
    overallLoanPercentage = serializers.CharField(read_only=True)
    dateApproved = serializers.DateTimeField(read_only=True)
    dateExpired = serializers.DateTimeField(read_only=True)
    creditLineAmount = serializers.CharField(read_only=True)
    availableBalance = serializers.CharField(read_only=True)

    def create(self, validated_data):
        loanProgram = LoanProgram.objects.create(**validated_data)
        return loanProgram

    def update(self, instance, validated_data):
        return instance

    class Meta:
        model = LoanProgram
        fields = "__all__"


class LoanReportSerializer(ModelSerializer):
    pnNo = serializers.CharField(read_only=True)
    releaseDate = serializers.CharField(read_only=True)
    maturityDate = serializers.CharField(read_only=True)
    borrowerName = serializers.ReadOnlyField(source="borrower.business.tradeName")
    address = serializers.CharField(read_only=True)
    branch = serializers.ReadOnlyField(source="borrower.branch.branchCode")
    loanTerm = serializers.ReadOnlyField(source="term.name")
    loanInterestRate = serializers.CharField(read_only=True)
    window = serializers.ReadOnlyField(source="loanProgram.name")
    status = serializers.ReadOnlyField(source="loanStatus.name")
    loanAmount = serializers.CharField(read_only=True)
    docStamps = serializers.CharField(read_only=True)
    tsNo = serializers.CharField(read_only=True)
    doa = serializers.CharField(read_only=True)
    notFee = serializers.CharField(read_only=True)
    netPreceed = serializers.CharField(read_only=True)
    exemption = serializers.CharField(read_only=True)
    edstSale = serializers.CharField(read_only=True)
    edstTransaction = serializers.CharField(read_only=True)
    releaseMonth = serializers.CharField(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "releaseMonth",
            "pnNo",
            "releaseDate",
            "borrowerName",
            "address",
            "maturityDate",
            "branch",
            "loanAmount",
            "loanTerm",
            "loanInterestRate",
            "window",
            "tsNo",
            "docStamps",
            "doa",
            "notFee",
            "netPreceed",
            "exemption",
            "edstSale",
            "edstTransaction",
            "status",
        ]


class LoanReportOutstandingBalanceSerializer(ModelSerializer):
    pnNo = serializers.CharField(read_only=True)
    releaseDate = serializers.CharField(read_only=True)
    borrowerName = serializers.ReadOnlyField(source="borrower.business.tradeName")
    branch = serializers.ReadOnlyField(source="borrower.branch.branchCode")
    loanTerm = serializers.ReadOnlyField(source="term.name")
    loanInterestRate = serializers.CharField(read_only=True)
    window = serializers.ReadOnlyField(source="loanProgram.name")
    releaseMonth = serializers.CharField(read_only=True)

    outstandingBalance = serializers.CharField(read_only=True)
    interestBalance = serializers.CharField(read_only=True)
    totalPrincipalBalance = serializers.CharField(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "releaseMonth",
            "pnNo",
            "releaseDate",
            "borrowerName",
            "branch",
            "loanTerm",
            "loanInterestRate",
            "window",
            "outstandingBalance",
            "interestBalance",
            "totalPrincipalBalance",
        ]


class AmortizationItemReportSerializer(ModelSerializer):
    pnNo = serializers.CharField(read_only=True)
    window = serializers.ReadOnlyField(source="amortization.loan.loanProgram.name")
    loanTerm = serializers.ReadOnlyField(source="amortization.loan.term.name")
    amortizationStatus = serializers.ReadOnlyField(source="amortizationStatus.name")
    branch = serializers.ReadOnlyField(source="amortization.loan.borrower.branch.branchCode")
    amortizationSchedule = serializers.CharField(read_only=True)
    principal = serializers.CharField(read_only=True)
    interest = serializers.CharField(read_only=True)
    accruedInterest = serializers.CharField(read_only=True)
    total = serializers.CharField(read_only=True)
    principalBalance = serializers.CharField(read_only=True)
    # loan_id = serializers.ReadOnlyField(source='amortization.loan.id')
    # payments = PaymentSerializer(many=True,read_only=True)
    # checks = CheckSerializer(many=True,read_only=True)
    # totalPayment = serializers.CharField(read_only=True)
    # latestCheck = CheckSerializer(read_only=True)

    class Meta:
        model = AmortizationItem
        fields = [
            "pnNo",
            "branch",
            "schedule",
            "days",
            "principal",
            "interest",
            "accruedInterest",
            "total",
            "principalBalance",
            "amortizationStatus",
            "window",
            "loanTerm",
            "amortizationSchedule",
        ]


class CreditLineOutstandingReportSerializer(ModelSerializer):
    borrowerName = serializers.CharField(read_only=True)
    _status = serializers.CharField(read_only=True)
    window = serializers.ReadOnlyField(source="loanProgram.name")
    paymentTerm = serializers.ReadOnlyField(source="term.name")
    totalAmount = serializers.CharField(read_only=True)
    creditLineInterestRate = serializers.CharField(read_only=True)
    dateCreated = serializers.CharField(read_only=True)
    dateExpired = serializers.CharField(read_only=True)
    dateApproved = serializers.CharField(read_only=True)
    totalAvailment = serializers.CharField(read_only=True)
    totalCreditLineBalance = serializers.CharField(read_only=True)

    class Meta:
        model = CreditLine
        fields = [
            "dateCreated",
            "borrowerName",
            "window",
            "dateApproved",
            "dateExpired",
            "purpose",
            "creditLineInterestRate",
            "paymentTerm",
            "totalAmount",
            "_status",
            "totalAvailment",
            "totalCreditLineBalance",
        ]


class CreditLineProcessingReportSerializer(ModelSerializer):
    borrowerName = serializers.CharField(read_only=True)
    _status = serializers.CharField(read_only=True)
    window = serializers.ReadOnlyField(source="loanProgram.name")
    paymentTerm = serializers.ReadOnlyField(source="term.name")
    totalAmount = serializers.CharField(read_only=True)
    creditLineInterestRate = serializers.CharField(read_only=True)
    dateCreated = serializers.CharField(read_only=True)

    class Meta:
        model = CreditLine
        fields = [
            "dateCreated",
            "borrowerName",
            "window",
            "purpose",
            "creditLineInterestRate",
            "paymentTerm",
            "totalAmount",
            "_status",
        ]


class CreditLineApprovedReportSerializer(ModelSerializer):
    borrowerName = serializers.CharField(read_only=True)
    _status = serializers.ReadOnlyField(source="status.name")
    window = serializers.ReadOnlyField(source="loanProgram.name")
    paymentTerm = serializers.ReadOnlyField(source="term.name")
    totalAmount = serializers.CharField(read_only=True)
    creditLineInterestRate = serializers.CharField(read_only=True)
    dateCreated = serializers.CharField(read_only=True)
    dateExpired = serializers.CharField(read_only=True)

    class Meta:
        model = CreditLine
        fields = [
            "dateCreated",
            "borrowerName",
            "window",
            "purpose",
            "creditLineInterestRate",
            "paymentTerm",
            "totalAmount",
            "dateExpired",
            "_status",
        ]