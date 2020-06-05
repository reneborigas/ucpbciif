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


    def __str__(self):
        return "%s" % (self.name)


class Statuses(models.Model):  

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


    def __str__(self):
        return "%s" % (self.name)

class Requirements(models.Model):  

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
 
    subProcess = models.ForeignKey(
        SubProcess,
        on_delete=models.CASCADE,
        related_name="requirements",
   
    )

    optional = models.BooleanField(
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
        return "%s" % (self.name)



class Step(models.Model):  

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
    position = models.ManyToManyField('committees.Position')

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
        # limit_choices_to={'subProcess': document_.subProcess},
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
    nextStep = models.ForeignKey(
        Step,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="nextStepOutputs",
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