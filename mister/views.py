import csv

from rest_framework import viewsets

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from .serializers import CollectorSerializer, UserSerializer
from .forms import UserForm, UserProfileForm
from .models import Collector, UserProfile


def index(request):
    return render(request, 'index.html')


def collection(request):
    data = Collector.objects.filter(
            user=request.user).order_by('-time_collected')
    return render(request, 'plantinfo.html', {'data': data})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class CollectionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mister collections to be viewed or edited.
    """
    queryset = Collector.objects.all().order_by('-pH_level')
    serializer_class = CollectorSerializer

    def get_queryset(self):
        return Collector.objects.filter(
                user=self.request.user).order_by('-pH_level')


def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        payload = {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered}
    return render_to_response('register.html', payload, context)


@login_required
def restricted(request):
    return HttpResponse("You're Logged In!")


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('plantinfo')
            else:
                return HttpResponse("Your Bona Petite account is disabled.")
        else:
            print('Invalid login details: {}, {}'.format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('login.html', {}, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('index')


@login_required
def profile(request):
    context = RequestContext(request)
    cat_list = get_category_list()  # DOES THIS WORK?
    context_dict = {'cat_list': cat_list}
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('profile.html', context_dict, context)


def data_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_csv.csv"'
    # Create the HttpResponse object with the appropriate CSV header.
    writer = csv.writer(response)
    for collector in Collector.objects.all():
        writer.writerow([collector.pH_level, collector.temperature])
    return response
