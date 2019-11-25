from django.http import HttpResponse, JsonResponse
from django.template import loader
from . import signal

def index(request):
    template = loader.get_template('CurveToSignalApp/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def get_points(request):
    asx = request.POST.getlist('x[]')
    asy = request.POST.getlist('y[]')
    dX,dY,adYCalc = prepare_signal([asx, asy])
    data = {'X'    : dX.tolist(),
            'Y'    : dY.tolist(),
            #'YCalc': adYCalc
            }    
    return JsonResponse(data)

def prepare_signal(points):
    asx = points[0]
    asy = points[1]
    if isinstance(asx[0], str):
        adx = [float(x) for x in asx]
        ady = [float(y) for y in asy]
    oSignal = signal.Signal([adx,ady])
    #acFourierCoeff = oSignal.get_Fourier_coefficients()
    adYCalc = oSignal.calculate_signal_from_Fourier_coeff()
    dX,dY = oSignal.dX, oSignal.dY
    return dX,dY,adYCalc  