from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SoilDataSerializer
import json
from traceback import print_exc
from django.db.models import Max
import csv

def current_value(request):
    csv_filename = 'soil_data.csv'
    data = []

    try:
        with open(csv_filename, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        data = None

    return render(request, 'welcome.html', {'data': data})





'''def current_value(request):
    # Get the latest data across all grid_sections
    data = SoilData.objects.all().order_by('-id').first()
    
    return render(request,'welcome.html',{'data':data})'''



# Create your views here.
# myapp/views.py

def welcome(request):
    data = SoilData.objects.all().order_by('-id').first()
    return render(request, 'welcome.html',{'data':data})

from .models import SoilData

def grid_section_detail(request):
    data = SoilData.objects.all()
    return render(request, 'npk.html', {'data': data})

def moisture(request):
    data = SoilData.objects.all()
    return render(request, 'water.html', {'data': data})

'''def current_value(request, grid_section):
    data = SoilData.objects
    return render(request, 'welcome.html', {'data': data})'''
    
'''@csrf_exempt
def receive_data_from_rover(request):
    if request.method == 'POST':
        try:

            # Get JSON data from the request
            data_json = json.loads(request.body)

            
            # Extract relevant information from the JSON data
            grid_section = data_json.get('grid_section')
            nitrogen = data_json.get('nitrogen')
            phosphorus = data_json.get('phosphorus')
            potassium = data_json.get('potassium')
            moisture_level = data_json.get('moisture_level')

            # Create a new SoilData instance and save it to the database
            soil_data = SoilData.objects.create(
                grid_section=grid_section,
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                moisture_level=moisture_level
            )

            return JsonResponse({'message': 'Data received and stored successfully'})
        except Exception as e:
            print_exc()
            return JsonResponse({'error': f'Error: {str(e)}'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)'''

class ReceiveDataFromRoverAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SoilDataSerializer(data=request.data)

        if serializer.is_valid():
            csv_filename = 'soil_data.csv'
            with open(csv_filename, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                # Write a header if the file is empty
                if csvfile.tell() == 0:
                    csv_writer.writerow(serializer.validated_data.keys())
                csv_writer.writerow(serializer.validated_data.values())
            # Save the data to the database
            soil_data = SoilData.objects.create(**serializer.validated_data)
           

            return JsonResponse({'message': 'Data received and stored successfully'})
            
           
        else:
            print_exc
            return JsonResponse({'error': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)
