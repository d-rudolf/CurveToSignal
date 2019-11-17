from django.http import HttpResponse
from django.template import loader
from . import signal

def index(request):
    template = loader.get_template('CurveToSignalApp/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def get_points(request):
    template = loader.get_template('CurveToSignalApp/index.html')
    context = {}
    asx = request.POST.getlist('x[]')
    asy = request.POST.getlist('y[]')
    prepare_signal([asx, asy])
    return HttpResponse(template.render(context, request))

def prepare_signal(points):
    asx = points[0]
    asy = points[1]
    if isinstance(asx[0], str):
        adx = [float(x) for x in asx]
        ady = [float(y) for y in asy]
    oSignal = signal.Signal([adx,ady])
    #acFourierCoeff = oSignal.get_Fourier_coefficients()
    oSignal.calculate_signal_from_Fourier_coeff()
    dX,dY = oSignal.dX, oSignal.dY