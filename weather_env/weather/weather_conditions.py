import weather.views
from django.shortcuts import redirect
from django.shortcuts import render

#helper view to pass filter parameter
def cloud(request):
    context = weather.views.sheetPandas('Clouds')
    return render(request, 'weather/index.html', context)
    # return redirect(weather.views.sheetSync(request,'Clouds'))

def thunderstorm(request):
    context = weather.views.sheetPandas('Thunderstorm')
    return render(request, 'weather/index.html', context)
    # return redirect(weather.views.sheetSync(request,'Thunderstorm'))

def drizzle(request):
    context = weather.views.sheetPandas('Drizzle')
    return render(request, 'weather/index.html', context)
    # return redirect(weather.views.sheetSync(request,'Drizzle'))

def rain(request):
    context = weather.views.sheetPandas('Rain')
    return render(request, 'weather/index.html', context)
    # return redirect(weather.views.sheetSync(request,'Rain'))

def snow(request):
    context = weather.views.sheetPandas('Snow')
    return render(request, 'weather/index.html', context)
    # return redirect(weather.views.sheetSync(request,'Snow'))

def clear(request):
    context = weather.views.sheetPandas('Clear')
    return render(request, 'weather/index.html', context)
    # return redirect(weather.views.sheetSync(request,'Clear'))

def atmosphere(request):
    context = weather.views.sheetPandas('Atmosphere')
    return render(request, 'weather/index.html', context)
    # return redirect(weather.views.sheetSync(request,'Atmosphere'))