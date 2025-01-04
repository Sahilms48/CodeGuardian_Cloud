# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from .main import main

# # Create your views here.
# def index(request):
#     return render(request, 'url/index.html')

# @csrf_exempt
# def generate_report(request, path):
#     if request.method == 'POST':
#         ##Some function here##
#         # TODO 
#         print("b")
#         main()
#         print("a")
#         return HttpResponse(f"Report generated for: {path}", status=200)

#     return HttpResponse("Invalid Request", status=400)


from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .main import main
import json

def index(request):
    return render(request, 'url/index.html')

@csrf_exempt
def generate_report(request):
    if request.method == 'GET':  # Changed to GET for EventSource
        repo_path = request.GET.get('path')  # Get path from query params
        email = request.GET.get('email', '')
        print(email)
        if not repo_path:
            return HttpResponse("No path provided", status=400)

        def stream_response():
            try:
                for progress in main(repo_path, email):
                    yield f"data: {json.dumps(progress)}\n\n"
                yield f"data: {json.dumps({'completed': True, 'message': 'Report generation completed successfully'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        response = StreamingHttpResponse(
            streaming_content=stream_response(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

    return HttpResponse("Invalid Request", status=400)
