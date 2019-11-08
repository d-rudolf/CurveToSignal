from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('CurveToSignalApp/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def get_points(request):
    template = loader.get_template('CurveToSignalApp/index.html')
    context = {}
    x = request.POST.getlist('x[]')
    y = request.POST.getlist('y[]')
    return HttpResponse(template.render(context, request))