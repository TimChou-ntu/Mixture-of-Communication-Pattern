from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import FibResItem
from .serializers import FibReqItemSerializer, FibResItemSerializer

# MQTT
import paho.mqtt.client as mqtt

# rgpc
import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
import fib_pb2
import fib_pb2_grpc

import log_pb2
import log_pb2_grpc


# Create your views here.
class EchoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(data={ 'echo': 'hello world' }, status=200)

class FiboView(APIView):
    permission_classes = (permissions.AllowAny,)

    def __init__(self):

        mqttIP = "127.0.0.1"
        mqttPORT = 1883
        self.client = mqtt.Client()
        self.client.connect(host=mqttIP, port=mqttPORT)
        # self.client.loop_start()
    
    def post(self, request):
        serializer = FibReqItemSerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer.data)
            # process
            
            fibIP = "127.0.0.1"
            fibPORT = "8080"
            host = f"{fibIP}:{fibPORT}"
            fiborder = serializer.data['order']
            print(fiborder)
            with grpc.insecure_channel(host) as channel:
                stub = fib_pb2_grpc.FibCalculatorStub(channel)

                request = fib_pb2.FibRequest()
                request.order = fiborder
                try:
                    response = stub.Compute(request)
                    # resdict = {}
                    # resdict.update(serializer.data)
                    # resdict['value'] = response.value
                    # res = FibResItemSerializer(data=resdict)
                    self.client.publish(topic='log', payload=response.value)
                    return Response({"status": "success", "data": response.value}, status=status.HTTP_200_OK)
                    # if res.is_valid():
                    #     return Response({"status": "success", "data": res.data}, status=status.HTTP_200_OK)
                    # else:
                    #     raise Exception
                except Exception as e:
                    return Response({"status": "error", "data": "error"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, _, id=None):

        # if id:
        #     item = FibResItem.objects.get(id=id)
        #     serializer = FibResItemSerializer(item)
        #     return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        # items = FibResItem.objects.all()
        # serializer = FibResItemSerializer(items, many=True)
        # return Response({"status": "success", "history": serializer.data}, status=status.HTTP_200_OK)

        # pass # TODO using grpc
        logIP = "127.0.0.1"
        logPORT = "8888"
        host = f"{logIP}:{logPORT}"
        
        with grpc.insecure_channel(host) as channel:
            stub = log_pb2_grpc.LogHistoryStub(channel)

            request = log_pb2.LogRequest()
            try:
                response = stub.getHistory(request)
                # self.client.publish(topic='log', payload=response.value)
                return Response({"status": "success", "data": response.value[:]}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"status": "error", "data": "error"}, status=status.HTTP_400_BAD_REQUEST)
