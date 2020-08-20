from django.urls import include, path
from django.conf.urls import url
from django.http import JsonResponse
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response
import logging
import pandas as pd
import json
import os

from . import views
from .models import TranDetail
from .serializers import TranSerializer
from .utils import utils

month_util = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', \
    'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

@api_view(['GET'])
def about(request):
    return Response({"message": "About"})
    
@api_view(['POST'])
def uploadFile(request):
    try:
        input_file = request.FILES['file']
        df = pd.read_csv(input_file, index_col = 0)
        str_data = df.reset_index().to_json(orient='records')

        json_data = json.loads(str_data)
        logging.info(json_data)
        for rec in json_data:
            reward, status = utils.get_reward(rec)
            rec['reward']= reward
            rec['status']= status
            tran_serializer = utils.create_new_rec(rec)

        data = {"message":"Records added succesfully"}
        return JsonResponse(data)

    except Exception as err:
        logging.error(f'err : {err}')
        data = {"message":"Failed to upload record"}
        return JsonResponse(data)

@api_view(['GET'])
def tran_list(request):
    try:
        tran = TranDetail.objects.all()
        title = request.GET.get('cardType', None)
        if title is not None:
            tran = tran.filter(title__icontains=title)
        
        tran_serializer = TranSerializer(tran, many=True)
        data = {"data" : tran_serializer.data, "size": len(tran_serializer.data) }
        return JsonResponse(data=data, safe=False)

    except Exception as err:
        logging.error(f'err : {err}')
        return JsonResponse("Failed to upload record")

@api_view(['GET'])
def tran_detail_status(request, param, value):
    # find tran by status
    try: 
        logging.info(f'param : {param}, value : {value}')
        if param == 'status':
            tran = TranDetail.objects.filter(status=value)
        elif param == 'category':
            tran = TranDetail.objects.filter(category=value)
        elif param == 'reward' or param == 'month':
            tran = TranDetail.objects.filter()
        else:
            data = {"data" : "Invalid filter selected"}
            return JsonResponse(data=data, safe=False)
        
        print(param, value)
        tran_serializer = TranSerializer(tran, many=True)
        records = tran_serializer.data
        if param == 'reward':
            rewards = []
            total = 0
            for rec in records:
                rewards.append(rec['reward'])
                total = total + int(rec['reward'])
            data = {"data" : rewards, "rewards":total, "size": len(records) }
        elif param == 'month':
            month_arr = []
            total = 0
            for rec in records:
                tran_date = rec['tran_date']
                rec_month = tran_date[5:7]
                if '/' in rec_month:
                    rec_month = tran_date[3:5]
                print(tran_date)
                print(rec_month)
                month = month_util[value]
                if month == rec_month:
                    month_arr.append(rec)
                    total = total+1
            data = {"data" : month_arr, "size":total }

        else:
            data = {"data" : records, "size": len(records) }

        return JsonResponse(data=data, safe=False)
    except Exception as err: 
        logging.error(f'err : {err}')
        return JsonResponse({'message': 'The Tran does not exist'}, status=404) 

router = routers.DefaultRouter()
router.register(r'trans', views.TranViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('about', about),
    path('upload/file', uploadFile),
    path('fetch/all', tran_list),
    path('fetch/<str:param>/<str:value>/', tran_detail_status),

]