class PMT:

    def __init__(self):
        self.nextStartingValue = 0
        self.payment = 0
        self.interest = 0 
        self.principal = 0


    def getPayment(self,loanAmount,interestRate,termDays,noOfPaymentSchedules,remainingperiod):
        
        noOfYears = termDays / 360
        frequencyPerYear = noOfPaymentSchedules / noOfYears
        # print(frequencyPerYear)
        # print("=====")
        #R
        periodicInterestRate = (interestRate/100) / int(frequencyPerYear)
        # print(periodicInterestRate)
        #PV
        presentValue = loanAmount
        # print(presentValue)
        # print("---------------")
        #n
        # totalNumberOfInterestPeriod = (frequencyPerYear * noOfYears) * -1
        totalNumberOfInterestPeriod = (remainingperiod) * -1
        
        #(PV*R)
        pvr = presentValue *  periodicInterestRate
        # print(pvr)

        self.payment =   pvr / (1 - (1 + periodicInterestRate) ** int(totalNumberOfInterestPeriod))
        self.interest = loanAmount * periodicInterestRate
        

        self.principal = self.payment - self.interest
        self.nextStartingValue = loanAmount -  self.principal

        return self

      