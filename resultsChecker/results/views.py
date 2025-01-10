from django.shortcuts import render
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re

def index(request):
    return render(request, 'results/index.html')

@csrf_exempt
def check_results(request):
    if request.method == "POST":
        # Extract the POST data from the form
        index_number = request.POST.get('indexNumber')
        name = request.POST.get('name')

        # Payload to send to the external server
        payload = {
            "indexNumber": index_number,
            "name": name
        }

        try:
            # Make the POST request to the external server
            response = requests.post(
                "https://results.knec.ac.ke/Home/CheckResults",
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            # Remove the form element and the image with alt="Banner" from the response
            cleaned_response = re.sub(r'<form.*?</form>', '', response.text, flags=re.DOTALL)
            cleaned_response = re.sub(r'<img[^>]*alt="Banner"[^>]*>', '', cleaned_response, flags=re.DOTALL)
            return HttpResponse(cleaned_response)  # Return the cleaned HTML response
        except requests.RequestException as e:
            return HttpResponse('<p class="text-red-700">Check your index number or name</p>', status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
