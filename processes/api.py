from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat

from committees.models import Position

class SubProcessViewSet(ModelViewSet):
    queryset = SubProcess.objects.all()
    serializer_class = SubProcessSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = SubProcess.objects.order_by('id')
        subProcessId = self.request.query_params.get('subProcessId', None)

        if subProcessId is not None:
            queryset = queryset.filter(id=subProcessId)

        return queryset


class StepViewSet(ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Step.objects.exclude(isDeleted=True).order_by('id')
        stepId = self.request.query_params.get('stepId', None)

        if stepId is not None:
            process = self.request.query_params.get('process', None)


            if process is not None:
                 
                if process == 'last':

                    step = Step.objects.get(id=stepId)


                    queryset = queryset.filter(order__gte=step.order).order_by('-order')[:1]

                elif process == 'current':

                    step = Step.objects.get(id=stepId)


                    queryset = queryset.filter(order__gt=step.order).order_by('order')[:1]

                elif process == 'next':
                    
                    step = Step.objects.get(id=stepId)

                    
                     
                    current = Step.objects.filter(order__gt=step.order).order_by('order').first()
                     
                    queryset = queryset.filter(order__gt=step.order).exclude(pk=current.pk).order_by('order')[:1]
                     
            else: 
                queryset = queryset.filter(id=stepId)


        return queryset.prefetch_related('outputs','position')

class OutputViewSet(ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Output.objects.annotate(
            stepName=F('step__name'), 
            stepStatus=F('step__status'), 
        ).order_by('id')
        outputID = self.request.query_params.get('outputID', None)

        if outputID is not None:
            queryset = queryset.filter(id=outputID)

        return queryset