# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis
import math
import dateutil.parser
import json
# Create your views here.
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt

redis_con = redis.StrictRedis(host="localhost", port="6379", db="0")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
@permission_classes((AllowAny,))
# @login_required(login_url='/login/')
def EMITemplate(request):
    return Response({'template':'emicalc'},template_name='emi_page.html')

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
# @login_required(login_url='/login/')
def emiCalculate(request):
    try:
        json_data = {}
        totalEmi = 0
        otherEmi = request.POST.get('otherEmi')
        income = request.POST.get('income')
        principal = request.POST.get('principal')
        rate = request.POST.get('interest')
        duration = request.POST.get('duration')
        fromemi = request.POST.get('fromemi')
        durationType = request.POST.get('durationType')
        monthNames = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"]
        monthDict = {}
        loanDict = {}
        if principal and rate and duration and fromemi and durationType:
            fromemidate = dateutil.parser.parse(fromemi, ignoretz=True).strftime("%m-%Y")
            startMonth = fromemidate.split('-')[0]
            startYear =  fromemidate.split('-')[1] 
            principal = float(principal)
            rate = float(rate)
            duration = float(duration)
            if durationType=="Y" :
                duration = duration * 12;
            rate = float((rate/12)/100)
            ratePower = float(math.pow((1+rate),duration))
            emi = float(principal*rate*(ratePower/(ratePower -1)))
            InterestPay =  float((emi*duration)-principal)
            totalPay = float(principal + InterestPay)
            for i in range(1,int(duration)+1):
                interestRateMonth = float(rate) * float(principal)
                principalMonth = float(emi) - float(interestRateMonth)
                loanRepaid = (principalMonth *100)/float(principal)
                principal = float(principal) - principalMonth;   
                totalVal = {'Principal':round(principalMonth) ,'Interest':round(interestRateMonth) ,'Total Payment':round(emi),'Balance':round(principal),'Loan Paid':round(loanRepaid)}
                monthName = monthNames[int(startMonth) - 1]
                monthDict[monthName] = totalVal
                loanDict[startYear] = monthDict
                if int(startMonth) == 12:
                    monthDict = {}
                    startMonth = 0;
                    startYear  = int(startYear)  + 1;
                startMonth = int(startMonth) + 1;
            json_data['loandata'] = loanDict
            json_data['totalPay'] = round(totalPay)
            json_data['status'] = "Success"

        elif income and rate and duration and durationType and otherEmi:
            emi = (float(income)*(50/100))
            rate = float(rate)
            duration = float(duration)
            if durationType=="Y" :
                duration = duration * 12;
            rate = float((rate/12)/100)
            ratePower = float(math.pow((1+rate),duration))
            for i in json.loads(otherEmi):
                totalEmi = float(totalEmi) + float(i)
            if totalEmi!=0 :
                remainIncome = float(income) - float(totalEmi)
                decreasePercent =50-(100 - (float(remainIncome)/(float(income)))*100)
            else:
                decreasePercent = 50
            finalEmi = float(income) * (float(decreasePercent)/100)
            principal = float(finalEmi)/float(rate*(ratePower/(ratePower -1)))
            json_data['emi'] = round(finalEmi)
            json_data['loanEligible'] = round(principal)
            json_data['status'] = "Success"
        else:
            json_data['status'] = "Failed"
    except Exception as e:
        print "eeeeeeeeeeeee",e
        json_data['status'] = "exception"
        json_data['exception'] = e
    return Response(json_data)