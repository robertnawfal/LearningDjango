from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer
import json
from datetime import datetime, timedelta

def index(request):
    now = datetime.now()

    return render(
        request,
        "HelloDjangoApp/index.html",  # Relative path from the 'templates' folder to the template file
        # "index.html", # Use this code for VS 2017 15.7 and earlier
        {
            'title' : "Hello Django",
            'message' : "Hello Django!",
            'content' : " on " + now.strftime("%A, %d %B, %Y at %X")
        }
    )

def about(request):
   return render(
      request,
      "HelloDjangoApp/about.html",
      {
         'title' : "About HelloDjangoApp",
         'content' : "Example app page for Django."
      }
   )

def rest(request):
   
    import json

    def merge_json_files(file_paths):
        result = []
        for f in file_paths:
            try:
                with open(f, "r", encoding="utf-8") as infile:
                    file_content = json.load(infile)
                    result.extend(file_content)
            except FileNotFoundError:
                print(f"File {f} not found.")

        # Sort the combined data by timestamp
        result.sort(key=lambda x: x.get("timestamp", 0))

        with open("result.json", "w") as output_file:
            json.dump(result, output_file)

    files = ["data/events.json", "data/latitudes.json", "data/longitudes.json"]
    # files = ["latitudes.json", "longitudes.json"]
    merge_json_files(files)
    
    return render(
      request,
      "HelloDjangoApp/rest.html",
      {
         'title' : "REST interface for flight coordinates.",
         'content' : "REST interface for flight coordinates."
      }
   
   )

class EventListView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

class EventDetailView(APIView):
    def get(self, request, event_id):
        event = get_object_or_404(Event, event_id=event_id)
        occurrence_time = event.occurrence_time

        with open('data/latitudes.json') as f:
            latitudes = json.load(f)

        with open('data/longitudes.json') as f:
            longitudes = json.load(f)

        closest_lat = min(latitudes, key=lambda x: abs(datetime.fromisoformat(x["timestamp"][:-1]) - occurrence_time))
        closest_lon = min(longitudes, key=lambda x: abs(datetime.fromisoformat(x["timestamp"][:-1]) - occurrence_time))

        response_data = {
            "event": EventSerializer(event).data,
            "latitude": closest_lat["latitude"],
            "longitude": closest_lon["longitude"],
            "lat_error": abs((datetime.fromisoformat(closest_lat["timestamp"][:-1]) - occurrence_time).total_seconds()),
            "lon_error": abs((datetime.fromisoformat(closest_lon["timestamp"][:-1]) - occurrence_time).total_seconds())
        }

        return Response(response_data)
