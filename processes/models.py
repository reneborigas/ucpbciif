from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator 

class Process(models.Model):     
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    code = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="processCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.name)


class SubProcess(models.Model):     
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    code = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    relatedProcesses = models.ManyToManyField('processes.SubProcess',blank=True)

    process = models.ForeignKey(
        Process,
        on_delete=models.CASCADE,
        related_name="subProcesses",
    ) 
    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="subProcessCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )
    def isCanCreateNewFile(self,borrower):
        isAllowed = False
        isAllowedByParent = False
        from documents.models import Document

        parentDocument = None
        if(self.relatedProcesses.last()):


            lastDocument = Document.objects.filter(
                borrower=borrower,
                subProcess = self.relatedProcesses.last(),

                ).order_by('id').last()


            if(lastDocument):
                if(lastDocument.documentMovements.last().status.isFinalStatus and not lastDocument.documentMovements.last().status.isNegativeResult):
                    isAllowedByParent = True
                else:
                    print("here")
                    isAllowedByParent = False
            
        lastDocument = Document.objects.filter(
            borrower=borrower,
            subProcess = self,

            ).order_by('id').last()

        if(lastDocument):
            if(lastDocument.documentMovements.last().status.isFinalStatus ): 

                isAllowed = True
            else:
                print("here") 
                isAllowed = False
        else:
            isAllowed=True

        if( (not lastDocument) and (not self.relatedProcesses.last() )):
            isAllowed=True
            isAllowedByParent=True

        if( (lastDocument) and (not self.relatedProcesses.last() )):
            
            isAllowedByParent=True

          

        print(self)
        print(isAllowed)
        print(isAllowedByParent)
        if isAllowed and isAllowedByParent:
            return True

        return False


    def getParentLastDocument(self,borrower):
        from documents.models import Document


        if(self.relatedProcesses.last()):


            lastDocument = Document.objects.filter(
                borrower=borrower,
                subProcess = self.relatedProcesses.last(),

                ).order_by('id').last()


            if(lastDocument):
                if(lastDocument.documentMovements.last().status.isFinalStatus and not lastDocument.documentMovements.last().status.isNegativeResult):
                    isAllowedByParent = True

                return lastDocument    
        return None

    def __str__(self):
        return "%s" % (self.name)


class Statuses(models.Model):  
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
   
    subProcess = models.ForeignKey(
        SubProcess,
        on_delete=models.CASCADE,
        related_name="statuses",
    )
    isDefault = models.BooleanField(
        default=False
    )    
    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="statusesCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    isFinalStatus = models.BooleanField(
        default=False,
    )

    isNegativeResult = models.BooleanField(
        default=False,
    )
    
    def __str__(self):
        return "%s %s" % (self.name, self.subProcess    )

class ProcessRequirement(models.Model):  
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
     
    subProcess = models.ForeignKey(
        SubProcess,
        on_delete=models.CASCADE,
        related_name="processRequirements",
    )
    isRequired = models.BooleanField(
        default=True
    )
    isAttachementRequired = models.BooleanField(
        default=True
    )    
    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="requirementsCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    
    def __str__(self):
        return "%s - %s" % (self.subProcess,self.name)

class Step(models.Model):  
    # def _get_self_subProcess(self):
    #     return self.subProcess
    order= models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), 
        MaxValueValidator(100)]
    )
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    committee = models.ForeignKey(
        'committees.Committee',
        on_delete=models.CASCADE,
        related_name="committeeSteps",
    )
    position = models.ManyToManyField('committees.Position',blank=True)
    subProcess = models.ForeignKey(
        SubProcess,
        on_delete=models.CASCADE,
        related_name="steps", 
    )    
    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )    
    status = models.ForeignKey(
        Statuses,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': _get_self_subProcess},
        related_name="stepStatuses",
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="stepCreatedBy",
        null = True,
    )    
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s: %s (%s)" % (self.order ,self.name, self.subProcess)

        
class Output(models.Model):  
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    ) 
    step = models.ForeignKey(
        Step,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="outputs",
    )
    callBackLink= models.TextField(
        blank = True,
        null = True,
    )
    nextStep = models.ForeignKey(
        Step,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="nextStepOutputs",
        blank=True,null=True
    )
    isDefault = models.BooleanField(
        default=False
    )    
    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="outputCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s - %s" % (self.step,self.name)
        
class StepRequirement(models.Model):  
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    step = models.ForeignKey(
        Step,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="requirements",
    )
    isRequired =models.BooleanField(
        default=True
    )  
    isAttachementRequired = models.BooleanField(
        default=True
    )
    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="stepRequirementCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField( 
        default=False,
    )

    def __str__(self):
        return "%s - %s" % (self.step,self.name)

def attachment_directory_path(instance, filename):
    # ext = filename.split('.')[-1]
    # filename = "%s_%s.%s" % (instance.user.id, instance.questid.id, ext)
    return 'attachments_{0}/{1}'.format(instance.stepRequirement.id, filename)

class StepRequirementAttachment(models.Model):  
    fileName = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    fileAttachment = models.FileField(
        null = True,
        blank=True,
        upload_to=attachment_directory_path
    )
    stepRequirement = models.ForeignKey(
        StepRequirement,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="stepRequirementAttachments",
    )    
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.CASCADE,
        related_name="documentStepRequirementAttachments",
    )
    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="stepAttachmentCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s - %s" % (self.stepRequirement,self.fileName)


def process_attachment_directory_path(instance, filename):
    # ext = filename.split('.')[-1]
    # filename = "%s_%s.%s" % (instance.user.id, instance.questid.id, ext)
    return 'attachments_{0}/{1}'.format(instance.processRequirement.id, filename)

class ProcessRequirementAttachment(models.Model):  
    fileName = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    fileAttachment = models.FileField(
        null = True,
        blank=True,
        upload_to=process_attachment_directory_path
    )
    processRequirement = models.ForeignKey(
        ProcessRequirement,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="processRequirementAttachments",
    )    
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.CASCADE,
        related_name="documentProcessRequirementAttachments",
    )
    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="processAttachmentCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s - %s" % (self.processRequirement,self.fileName)
# class PositionStep(models.Model):  

#     position = models.CharField(
#         'committees.Position',
#         on_delete=models.CASCADE,
          
#     )

#     step = models.ForeignKey(
#         Step,
#         on_delete=models.CASCADE,
         
#     )

#     createdBy = models.ForeignKey(
#         'users.CustomUser',
#         on_delete=models.SET_NULL,
#         related_name="positionStepCreatedBy",
#         null = True,
#     )

#     dateCreated = models.DateTimeField(
#         auto_now_add=True,
#     )
#     dateUpdated = models.DateTimeField(
#         auto_now_add=True,
#     )
#     isDeleted = models.BooleanField(
#         default=False,
#     )


#     def __str__(self):
#         return "%s - %s" % (self.step,self.name)