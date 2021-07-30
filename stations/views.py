from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    class BusStation:
        def __init__(self, Name, Street, District):
            self.Name = Name
            self.Street = Street
            self.District = District

    stations_info = []
    with open(settings.BUS_STATION_CSV, encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stations_info.append(
                BusStation(
                    Name=row.get('Name'),
                    Street=row.get('Street'),
                    District=row.get('District'))
            )

    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(stations_info, settings.ELEMENT_PER_PAGE)
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
