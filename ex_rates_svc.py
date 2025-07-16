import os
import struct
import sys
import time
import datetime
import array
import enum
import urllib
import json
import requests

from concurrent import futures
import logging

import grpc

sys.path.append('gen');
from gen import ex_rates_pb2
from gen import ex_rates_pb2_grpc

REMOTE_REQUEST_REF_TEMPLATE = 'https://open.er-api.com/v6/latest/{}'

class CurrRatesSvc(ex_rates_pb2_grpc.ExRatesSvc):

        rates = {}

        def __init__(self):
            pass

        def GetRates(self, request, context) -> ex_rates_pb2.Rates:
            # TODO: Refresh cache periodically (e.g. limit keeping some rates by time)
            specificRates = self.getFromCache(request.currency_code)
            if (specificRates == None):
                print("Requesting from remote service for", request.currency_code, "...")
                jsData = self.requestFromRemote(request.currency_code)
                if jsData.get("result") == "success":
                    specificRates = self.fillRatesFromJs(jsData, request.currency_code)
                    print("Received successfully!")
                else:
                    specificRates = ex_rates_pb2.Rates()
                    print("Something went wrong :(")
            else:
                print("Obtained from cache for", request.currency_code)
            return specificRates;

        def fillRatesFromJs(self, jsData, currency):
            specificRates = None
            jsRates = jsData.get("rates", None) 
            if jsRates:
                    specificRates = ex_rates_pb2.Rates()
                    self.rates[currency] = specificRates
                    for element in jsRates.items():
                        specificRates.entries.append(ex_rates_pb2.Rates.Rate(currency=element[0], value=element[1]))
            else:
                print("Rates not found in js data")
            return specificRates

        def checkIfExist(self, currency) -> bool:
            val = self.rates.get(currency, None)
            return (val != None)
        
        def getFromCache(self, currency) -> ex_rates_pb2.Rates:
            return self.rates.get(currency, None)

        def printData(self, jsData):
             for element in jsData["rates"].items():
                print(element[0], " : ", element[1])

        def requestFromRemote(self, key):
            fullRef = REMOTE_REQUEST_REF_TEMPLATE.format(key);
            result = requests.get(fullRef)
            jsData = json.loads(result.content.decode('utf-8')) 
            return jsData
        

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ex_rates_pb2_grpc.add_ExRatesSvcServicer_to_server(CurrRatesSvc(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()


