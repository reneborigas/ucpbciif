from rest_framework.routers import DefaultRouter
from .api import *
from django.urls import path

router = DefaultRouter()
router.register(r"amortizationitems", AmortizationItemViewSet)
router.register(r"amortizationitemsreports", AmortizationItemReportViewSet)
router.register(r"amortizationitemsagingreports", AmortizationItemAgingViewSet)


router.register(r"amortizations", AmortizationViewSet)
router.register(r"creditlines", CreditLineViewSet)
router.register(r"creditlineslist", CreditLineListViewSet)

router.register(r"loans", LoanViewSet)
router.register(r"loanreports", LoanReportViewSet)
router.register(r"loanreportssecurity", LoanReportSecurityViewSet)
router.register(r"loanreportsoutstandingbalance", LoanReportOutstandingBalanceViewSet)

router.register(r"terms", TermViewSet)
router.register(r"crud-terms", CRUDTermViewSet)
router.register(r"paymentperiods", PaymentPeriodViewSet)
router.register(r"loanprograms", LoanProgramViewSet)
router.register(r"interestrates", InterestRateViewSet)
router.register(r"status", StatusViewSet)
router.register(r"amortizationstatus", AmortizationStatusViewSet)
router.register(r"loanstatus", LoanStatusViewSet)

router.register(r"loanprogramdistribution", LoanProgramDistributionViewSet)
router.register(r"creditlineprocessingreport", CreditLineProcessingReportViewSet)
router.register(r"creditlineapprovedreport", CreditLineApprovedReportViewSet)
router.register(r"creditlineoutstandingreport", CreditLineOutstandingViewSet)

router.register(r"loanprogramagingcount", LoanProgramAgingCountViewSet)

urlpatterns = [
    path("updatecreditline/", UpdateCreditLineView.as_view()),
    path("updateamortizationitem/", UpdateAmortizationItemView.as_view()),
    path("updateloanview/", UpdateLoanView.as_view()),
    path("updatecreditlineview/", UpdateCreditLineView.as_view()),
    path("amortizationitemscalendar/", GetAmortizationItemsCalendarView.as_view()),
    path("getdashboarddata/", GetDashboardDataView.as_view()),
]


urlpatterns += router.urls