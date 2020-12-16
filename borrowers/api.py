from rest_framework.viewsets import ModelViewSet
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
from documents.models import Document, DocumentMovement
from loans.models import Loan
from payments.models import Payment


class CreateBorrowerViewSet(ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = CreateBorrowerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Borrower.objects.exclude(isDeleted=True).order_by("borrowerId")
        borrowerId = self.request.query_params.get("borrowerId", None)

        if borrowerId is not None:
            queryset = queryset.filter(borrowerId=borrowerId)

        return queryset


class FetchBorrowerViewSet(ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = FetchBorrowerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = (
            Borrower.objects.annotate(
                borrowerName=Case(
                    When(Q(recordType="BD"), then=F("business__tradeName")),
                    When(
                        Q(recordType="ID"),
                        then=Concat(
                            F("individual__firstname"),
                            V(" "),
                            F("individual__middlename"),
                            V(" "),
                            F("individual__lastname"),
                        ),
                    ),
                ),
                borrowerType=Case(
                    When(recordType="BD", then=V("Business")),
                    When(recordType="ID", then=V("Individual")),
                    output_field=models.CharField(),
                ),
                branch=F("area__branchCode"),
                tin=Case(
                    When(
                        Q(recordType="BD") & Q(business__businessIdentification__identificationType__value="10"),
                        then=F("business__businessIdentification__identificationNumber"),
                    ),
                    When(
                        Q(recordType="ID") & Q(individual__individualIdentification__identificationType__value="10"),
                        then=F("individual__individualIdentification__identificationNumber"),
                    ),
                ),
            )
            .exclude(isDeleted=True)
            .order_by("-borrowerId")
        )
        borrowerId = self.request.query_params.get("borrowerId", None)

        if borrowerId is not None:
            queryset = queryset.filter(borrowerId=borrowerId)

        return queryset


class UpdateBorrowerViewSet(ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = UpdateBorrowerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Borrower.objects.exclude(isDeleted=True).order_by("borrowerId")
        borrowerId = self.request.query_params.get("borrowerId", None)

        if borrowerId is not None:
            queryset = queryset.filter(borrowerId=borrowerId)

        return queryset


class BorrowerViewSet(ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = (
            Borrower.objects.prefetch_related(
                Prefetch(
                    "individual",
                    queryset=Individual.objects.annotate(
                        _titleName=F("title__description"),
                        _genderName=F("gender__description"),
                        _countryOfBirthName=F("countryOfBirth__description"),
                        _nationalityName=F("nationality__description"),
                        _maritalStatusName=F("maritalStatus__description"),
                        _religionName=F("religion__name"),
                    ).all(),
                ),
                Prefetch(
                    "business",
                    queryset=Business.objects.annotate(
                        _nationalityName=F("nationality__description"),
                        _legalFormName=F("legalForm__description"),
                        _psicName=F("psic__description"),
                        _firmSizeName=F("firmSize__description"),
                    ).all(),
                ),
                "borrowerAttachments",
                Prefetch("documents", queryset=Document.objects.order_by("dateCreated")),
                Prefetch(
                    "loans",
                    queryset=Loan.objects.order_by("dateReleased"),
                ),
                Prefetch("documents__documentMovements", queryset=DocumentMovement.objects.order_by("-dateCreated")),
            )
            .annotate(
                borrowerName=Case(
                    When(Q(recordType="BD"), then=F("business__tradeName")),
                    When(
                        Q(recordType="ID"),
                        then=Concat(
                            F("individual__firstname"),
                            V(" "),
                            F("individual__middlename"),
                            V(" "),
                            F("individual__lastname"),
                        ),
                    ),
                ),
                borrowerType=Case(
                    When(recordType="BD", then=V("Business")),
                    When(recordType="ID", then=V("Individual")),
                    output_field=models.CharField(),
                ),
                borrowerAddress=Case(
                    When(
                        Q(recordType="BD"),
                        then=Concat(
                            F("business__businessAddress__streetNo"),
                            V(" "),
                            F("business__businessAddress__barangay"),
                            V(" "),
                            F("business__businessAddress__city"),
                            V(" "),
                            F("business__businessAddress__province"),
                        ),
                    ),
                    When(
                        Q(recordType="ID"),
                        then=Concat(
                            F("individual__individualAddress__streetNo"),
                            V(" "),
                            F("individual__individualAddress__barangay"),
                            V(" "),
                            F("individual__individualAddress__city"),
                            V(" "),
                            F("individual__individualAddress__province"),
                        ),
                    ),
                ),
                contactPersonNumber=Case(
                    When(
                        Q(recordType="BD"),
                        then=F("business__businessContactPerson__phoneNo"),
                    ),
                ),
                areaCode=Case(
                    When(
                        Q(recordType="BD"),
                        then=F("area__branchCode"),
                    ),
                ),
                tin=Case(
                    When(
                        Q(recordType="BD") & Q(business__businessIdentification__identificationType__value="10"),
                        then=F("business__businessIdentification__identificationNumber"),
                    ),
                    When(
                        Q(recordType="ID") & Q(individual__individualIdentification__identificationType__value="10"),
                        then=F("individual__individualIdentification__identificationNumber"),
                    ),
                ),
            )
            .exclude(isDeleted=True)
            .order_by("-borrowerId")
        )

        borrowerId = self.request.query_params.get("borrowerId", None)
        branch = self.request.query_params.get("branch", None)
        loanProgramId = self.request.query_params.get("loanProgramId", None)
        totalAvailmentsFrom = self.request.query_params.get("totalAvailmentsFrom", None)
        totalAvailmentsTo = self.request.query_params.get("totalAvailmentsTo", None)
        totalOutstandingBalanceFrom = self.request.query_params.get("totalOutstandingBalanceFrom", None)
        totalOutstandingBalanceTo = self.request.query_params.get("totalOutstandingBalanceTo", None)
        totalPaymentsFrom = self.request.query_params.get("totalPaymentsFrom", None)
        totalPaymentsTo = self.request.query_params.get("totalPaymentsTo", None)

        clientSinceFrom = self.request.query_params.get("clientSinceFrom", None)
        clientSinceTo = self.request.query_params.get("clientSinceTo", None)

        if borrowerId is not None:
            queryset = queryset.filter(borrowerId=borrowerId)

        if branch is not None:
            queryset = queryset.filter(area=branch)

        if totalAvailmentsFrom is not None and totalAvailmentsTo is not None:
            borrowers = []
            for borrower in queryset:
                borrower.totalAvailments = borrower.getTotalAvailments()
                if (int(borrower.totalAvailments) >= int(totalAvailmentsFrom)) and (
                    int(borrower.totalAvailments) <= int(totalAvailmentsTo)
                ):
                    borrowers.append(borrower.pk)

            queryset = queryset.filter(borrowerId__in=borrowers)

        if totalOutstandingBalanceFrom is not None and totalOutstandingBalanceTo is not None:
            borrowers = []
            for borrower in queryset:
                borrower.totalOutstandingBalance = borrower.getTotalOutstandingBalance()
                if (int(borrower.totalOutstandingBalance) >= int(totalOutstandingBalanceFrom)) and (
                    int(borrower.totalOutstandingBalance) <= int(totalOutstandingBalanceTo)
                ):
                    borrowers.append(borrower.pk)

            queryset = queryset.filter(borrowerId__in=borrowers)

        if totalPaymentsFrom is not None and totalPaymentsTo is not None:
            borrowers = []
            for borrower in queryset:
                borrower.payments = borrower.getPayments()
                borrower.totalPayments = borrower.getTotalPayments()
                if (int(borrower.totalPayments) >= int(totalPaymentsFrom)) and (
                    int(borrower.totalPayments) <= int(totalPaymentsTo)
                ):
                    borrowers.append(borrower.pk)

            queryset = queryset.filter(borrowerId__in=borrowers)

        if clientSinceFrom is not None and clientSinceTo is not None:
            queryset = queryset.filter(accreditationDate__gte=clientSinceFrom).filter(
                accreditationDate__lte=clientSinceTo
            )

        for borrower in queryset:
            borrower.totalAvailments = borrower.getTotalAvailments()
            borrower.totalOutstandingBalance = borrower.getTotalOutstandingBalance()

            borrower.payments = borrower.getPayments()
            borrower.totalPayments = borrower.getTotalPayments()

            for loan in borrower.loans.all():
                loan.totalAmortizationInterest = loan.getTotalAmortizationInterest
                loan.totalPayment = loan.getTotalPayment
                loan.totalPrincipalPayment = loan.getTotalPrincipalPayment()
                loan.totalInterestPayment = loan.getTotaInterestPayment()
                loan.totalAccruedInterestPayment = loan.getTotalAccruedInterestPayment()
                loan.totalTotalInterestPayment = loan.getTotalTotalInterestPayment()
                loan.totalPenaltyPayment = loan.getTotalPenaltyPayment()
                loan.totalAdditionalInterestPayment = loan.getTotalAdditionalInterestPayment()
                loan.lastAmortizationItem = loan.getLastAmortizationItem()
                loan.latestAmortization = loan.getLatestAmortization()

                if loan.latestAmortization:
                    loan.latestAmortization.totalAmortizationPrincipal = (
                        loan.latestAmortization.getTotalAmortizationPrincipal()
                    )
                    print(loan.latestAmortization.totalAmortizationPrincipal)

            if loanProgramId is not None:
                borrower.totalAvailmentPerProgram = borrower.getTotalAvailmentsPerProgram(loanProgramId)

        return queryset


class BusinessViewSet(ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = (permissions.IsAuthenticated,)


class IndividualViewSet(ModelViewSet):
    queryset = Individual.objects.all()
    serializer_class = IndividualSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BorrowerAttachmentViewSet(ModelViewSet):
    queryset = BorrowerAttachment.objects.all()
    serializer_class = BorrowerAttachmentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = BorrowerAttachment.objects.order_by("id")

        borrowerAttachmentId = self.request.query_params.get("borrowerAttachmentId", None)
        borrowerId = self.request.query_params.get("borrowerId", None)

        if borrowerAttachmentId is not None:
            queryset = queryset.filter(borrowerAttachment__id=borrowerAttachmentId)

        if borrowerId is not None:
            queryset = queryset.filter(borrower=borrowerId)

        return queryset


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Branch.objects.order_by("id")

        return queryset


class BorrowerReportViewSet(ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerReportSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = (
            Borrower.objects.prefetch_related(
                "borrowerAttachments",
                Prefetch("documents", queryset=Document.objects.order_by("dateCreated")),
                Prefetch("loans", queryset=Loan.objects.order_by("dateReleased")),
                Prefetch("documents__documentMovements", queryset=DocumentMovement.objects.order_by("-dateCreated")),
            )
            .annotate(
                borrowerName=Case(
                    When(Q(recordType="BD"), then=F("business__tradeName")),
                    When(
                        Q(recordType="ID"),
                        then=Concat(
                            F("individual__firstname"),
                            V(" "),
                            F("individual__middlename"),
                            V(" "),
                            F("individual__lastname"),
                        ),
                    ),
                ),
                _area=Case(
                    When(Q(recordType="BD"), then=F("area__branchCode")),
                ),
            )
            .exclude(isDeleted=True)
            .order_by("borrowerId")
        )

        loanProgramId = self.request.query_params.get("loanProgramId", None)
        outstandingBalance = self.request.query_params.get("outstandingBalance", None)

        for borrower in queryset:
            borrower.totalAvailments = borrower.getTotalAvailments()
            borrower.totalOutstandingBalance = borrower.getTotalOutstandingBalance()
            borrower.payments = borrower.getPayments()
            borrower.totalPayments = borrower.getTotalPayments()

            for loan in borrower.loans.all():
                loan.totalPayment = loan.getTotalPayment
                loan.totalPrincipalPayment = loan.getTotalPrincipalPayment()
                loan.totalInterestPayment = loan.getTotaInterestPayment()
                loan.totalAccruedInterestPayment = loan.getTotalAccruedInterestPayment()
                loan.totalTotalInterestPayment = loan.getTotalTotalInterestPayment()
                loan.totalPenaltyPayment = loan.getTotalPenaltyPayment()
                loan.totalAdditionalInterestPayment = loan.getTotalAdditionalInterestPayment()

            if loanProgramId is not None:
                borrower.totalAvailmentPerProgram = borrower.getTotalAvailmentsPerProgram(loanProgramId)

            if outstandingBalance:
                borrower.totalOutstandingBalance = borrower.getTotalOutstandingBalance()
                exclude = []
                if borrower.totalOutstandingBalance == 0:
                    exclude.append(borrower.pk)

                queryset = queryset.exclude(pk__in=exclude)

        for borrower in queryset:
            borrower.totalAvailments = str(borrower.getTotalAvailments()) + " | number :'2'"
            borrower.totalOutstandingBalance = str(borrower.getTotalOutstandingBalance()) + " | number :'2'"
            borrower.payments = borrower.getPayments()
            borrower.totalPayments = str(borrower.getTotalPayments()) + " | number :'2'"

        return queryset