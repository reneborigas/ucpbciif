from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *

from documents.models import * 
from committees.models import Committee
from processes.models import Statuses,Step,Output,SubProcess
from processes.serializers import OutputSerializer,StatusSerializer,SubProcessSerializer
from committees.serializers import NoteSerializer
from loans.serializers import LoanSerializer,CreditLineSerializer
from loans.models import Loan ,CreditLine


class DocumentMovementSerializer(ModelSerializer): 
    committeeName = serializers.CharField(read_only=True)
    statusName = serializers.CharField(read_only=True) 
    documentId = serializers.CharField(read_only=True)
    stepId = serializers.CharField(read_only=True)
    outputName= serializers.CharField(read_only=True)
    output= OutputSerializer(read_only=True)
    outputId= serializers.CharField()
    
    # status = serializers.StatusSerializer(read_only=True)
    status = StatusSerializer(read_only=True)


    def create(self, validated_data): 
 

         
        document = Document.objects.get(pk=validated_data.get("document").id)
        outputId =  validated_data.get("outputId")
        print(outputId)
        output = Output.objects.get(id=outputId) 
        
        committee = Committee.objects.get(pk=validated_data.get("committee", "1").id)
        remarks = validated_data.get("remarks", "")
        documentMovement = DocumentMovement(
        document = document ,name = output.step.name,output=output, committee= committee , status=output.step.status,step=output.step,remarks=remarks)

        documentMovement.save()

        
        return documentMovement
 
    

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = DocumentMovement          
        fields = '__all__'

class DocumentSerializer(ModelSerializer):



    subProcessName = serializers.CharField(read_only=True)
    documentTypeName = serializers.CharField(read_only=True)
    borrowerName = serializers.CharField(read_only=True)
    documentCode = serializers.CharField(read_only=True)
    notes = NoteSerializer(many=True,read_only=True)
    loan = LoanSerializer(read_only=True)
    creditLine = CreditLineSerializer(read_only=True)

    loanid= serializers.CharField(required=False)
    creditlineid= serializers.CharField(required=False)

    currentStatus = StatusSerializer(read_only=True)
    
    documentMovements = DocumentMovementSerializer(many=True,read_only=True)
    lastDocumentMovementId = serializers.CharField(read_only=True)
    subProcess = SubProcessSerializer(read_only=True)
    subProcessId = serializers.CharField()
    committeeId = serializers.CharField()
    
    def create(self, validated_data): 
        
        committee = Committee.objects.get(pk=validated_data.get("committeeId", "1"))
        print(validated_data)
        status = Statuses.objects.get(pk=1)
        # subProcess = SubProcess.objects.get(pk=validated_data.get("subProcess")[''] )
        # validated_data.set("subProcess",)
        # print(validated_data)

        subProcess = SubProcess.objects.get(pk=validated_data.get("subProcessId","1" ))
        description = validated_data.get("description", "1")
        remarks = validated_data.get("remarks", "1")
        
        parentDocument = None
        if(subProcess.relatedProcesses.last()):
            lastDocument = Document.objects.filter(
                borrower_id=validated_data.get("borrower" ),
                subProcess = subProcess.relatedProcesses.last(),

                ).order_by('id').last()
            
          
            if(lastDocument.documentMovements.last().status.isFinalStatus and not lastDocument.documentMovements.last().status.isNegativeResult):
                parentDocument = lastDocument

        document=Document(
            subProcess=subProcess,
            name=validated_data.get("name" ),
            code=subProcess.code, 
            documentType=validated_data.get("documentType" ), 
            borrower=validated_data.get("borrower" ),
            parentDocument=parentDocument,
            description=description,
            remarks=remarks
            )

        creditlineid = validated_data.get("creditlineid" )
        if creditlineid is not None:  
            creditLine = CreditLine.objects.get(pk=validated_data.get("creditlineid" )) 
            if creditLine:
                document.creditLine = creditLine

        loanid = validated_data.get("loanid" )
        if loanid is not None: 
            loan = Loan.objects.get(pk=loanid)
            if loan:
               document.loan = loan

       
         
       

       

           
        
        document.save()

        # document = Document.objects.create(**validated_data) 
        # document.code = document.subProcess.code + ("%03d" % document.id)
        # document.save()
        
        steps = Step.objects.filter(subProcess=document.subProcess) 
        step = steps.order_by('order').first()
        
        
        if not step:
            name = '%s Created'  % document.subProcess 
            user = validated_data.get("createdBy", "1")
            step = Step(subProcess=document.subProcess,committee=committee,name=name,order=0,createdBy=user,status=status)
            step.save()

           


        documentMovement = DocumentMovement(
        document = document ,name = step.name, committee= committee , status=status,step=step)
        documentMovement.save()

        return document
 
    

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = Document          
        fields = '__all__'
 