from django.http.response import JsonResponse
from pandas.core.frame import DataFrame
from historia.forms import UploadFileForm
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .serializers import ContractSearializer, RatesSearializer
from .models import Contract, Rate
import pandas as pd
import json
import uuid
import os

def handle_uploaded_file(f):
    uuidForFile = uuid.uuid4()
    pathToFile = f'{uuidForFile}.xlsx'
    with open(f'{uuidForFile}.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return pathToFile

def deleteFile(path):
    os.remove(path)

def insertRates(data: dict, contract: Contract):
    rates = []
    for row in data:
        origin = row["POL"]
        destination = row["POD"]
        currency = row["Curr."]
        twenty = row["20'GP"]
        forty = row["40'GP"]
        fortyhc = row["40'HC"]
        rate = Rate(origin=origin, destination=destination, currency=currency, twenty=twenty, forty=forty, fortyhc=fortyhc, contract=contract)
        rate.save()
        rates.append({
            "origin": origin,
            "destination": destination,
            "currency": currency,
            "twenty": twenty,
            "forty": forty,
            "fortyhc": fortyhc
        })
    return rates

def validateFile(excel: DataFrame):
    if not'POL' in excel.all():
        return False
    if not'POD' in excel.all():
        return False
    if not'Curr.' in excel.all():
        return False
    if not "20'GP" in excel.all():
        return False
    if not "40'GP" in excel.all():
        return False
    if not "40'HC" in excel.all():
        return False
    return True

@api_view(["GET", "POST"])
def contractController(request: Request):
    if(request.method == "POST"):
        uploadForm = UploadFileForm(request.POST, request.FILES)
        print(request.FILES)
        if not uploadForm.is_valid():
            return Response({ "msg": "Falta algun campo" })
        pathToFile = handle_uploaded_file(request.FILES["file"])
        print(pathToFile)
        excel = pd.read_excel(pathToFile, engine="openpyxl")
        excel = excel.dropna()
        if(not validateFile(excel)):
            deleteFile(pathToFile)
            return Response({ "msg": "Excel invalido" })
        nombre = request.data["nombre"]
        fecha = request.data["fecha"]
        contract = Contract(nombre=nombre, fecha=fecha)
        contract.save()
        excel = json.loads(excel.to_json(orient="records"))
        deleteFile(pathToFile)
        rates = insertRates(excel, contract)        
        return render(request, "result.html", { "contract": contract, "rates": rates })
    else:
         contract = Contract.objects.all()
         contractSearializer = ContractSearializer(contract, many=True)
         return JsonResponse(contractSearializer.data, safe=False)
    
@api_view(["GET"])
def ratesController(request: Request):
    rate = Rate.objects.all()
    ratesSearializer = RatesSearializer(rate, many=True)
    return JsonResponse(ratesSearializer.data, safe=False)

@api_view(["GET"])
def formController(request: Request):
    return render(request, "index.html")
