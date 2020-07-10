


def generateAmortizationSchedule(loan):

        numberOfItems = loan.term/loan.term.paymentPeriod
        schedule = loan.dateReleased  + timezone.timedelta(days=loan.term.paymentPeriod)
        for i in range(numberOfItems):
            amortization = Amortization(
                schedule = schedule,
                loan=loan,
                days=loan.term.paymentPeriod,
                principal = 0,
                interest = 0,
                vat = 0,
                total = 0, 
                principalBalance = 0,
                status=1 
            ) 
            amortization.save()
            schedule = schedule + timezone.timedelta(days=loan.term.paymentPeriod)