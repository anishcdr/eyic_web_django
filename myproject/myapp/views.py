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

def current_value(request):
    # Get the latest data across all grid_sections
    data = SoilData.objects.values('grid_section').annotate(latest_timestamp=Max('timestamp')).order_by('-latest_timestamp').first()

    if data:
        # Retrieve the data for the grid_section with the latest timestamp
        data_instance = SoilData.objects.get(grid_section=data['grid_section'], timestamp=data['latest_timestamp'])
        return render(request, 'welcome.html', {'data': data_instance})
    else:
        # No data available
        return render(request, 'welcome.html', {'data': None})



# Create your views here.
# myapp/views.py

def welcome(request):
    return render(request, 'welcome.html')

from .models import SoilData

def grid_section_detail(request, grid_section):
    data = SoilData.objects
    return render(request, 'npk.html', {'data': data})

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
            # Save the data to the database
            soil_data = SoilData.objects.create(**serializer.validated_data)
            return JsonResponse({'message': 'Data received and stored successfully'})
           
        else:
            print_exc
            return JsonResponse({'error': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)
