from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from .models import Counter
from .serializers import CounterSerializer
from prometheus_client import Counter as PCounter, generate_latest, CONTENT_TYPE_LATEST

# Define a Prometheus Counter to track the number of API calls
API_CALL_COUNT = PCounter('counter_api_calls_total', 'Total number of times the counter API was called')


class CounterView(APIView):
    def get(self, request):
        try:
            # Get the counter object, or create it if it doesn't exist
            DBCounter, created = Counter.objects.get_or_create(id=1)
            # Increment the counter
            DBCounter.value += 1
            DBCounter.save()
            # Serialize the response
            serializer = CounterSerializer(DBCounter)

            # Update Prometheus metric
            API_CALL_COUNT.inc()

            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# Prometheus Metrics View
def metrics_view(request):
    """Expose Prometheus metrics"""
    try:
        return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

