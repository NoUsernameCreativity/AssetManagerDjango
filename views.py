from msilib.schema import Media
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .models import teacher, asset
from .forms import AssetForm

# for last updated updation
from datetime import datetime

selectedAssetsIndices = []
sortByKey = "id"
filters={'Subject': None}

def index(request):
    return render(
        request, 
        "DjangoApp1/index.html",  # Relative path from the templates folder to the template file we want
        {
            'header': "Home page",
            'title' : "Home page",
            'description': "This is the home page"
        }
    )


def UsersPage(request):
    users = teacher.objects.values()

    # deal with add assets button to let us do something
    if request.method == 'POST' and 'add_user' in request.POST:
        inputs ={
            'Name': request.POST.get('Name', None),
            'Area': request.POST.get('Area', None)
        }
        if all(inputs.values()): # no 'none' values
            teacher.objects.create(**inputs)

    return render(
        request, 
        "DjangoApp1/index.html",  # Relative path from the templates folder to the template file we want
        {
            'header': "Users page",
            'title' : "Users page",
            'description': "Here you can see all the users of the website.",
            'tableHeaders': ["ID", "Name", "Teaching area"],
            'tableContent': users,
            'buttons': ['add_user'],
        }
    )

def GetSelectedItemIndex(selectedIndex, dictionary):
    for item in dictionary:
        if item.startswith('selectedassetid'):
            indexOut = int(''.join([char for char in item if char.isdigit()]))
            selectedIndex.append(indexOut)
            return True
    return False

def GetSortByKey(sortByList, dictionary):
    for item in dictionary:
        if item.startswith('sortby'):
            strOut = item.split('_')[1] # must be split around _
            sortByList.append(strOut)
            return True
    return False


def AssetsPage(request):
    # stuff to deal with forms


    if request.method == 'POST' and 'asset_form' in request.POST:
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        if len(request.FILES.getlist('AssetImage')) > 0:
             storedURL = asset.objects.all().latest('id').__dict__['AssetImage']
             imagefile = request.FILES.getlist('AssetImage')[0]
             print("creating file at" + settings.MEDIA_ROOT.replace('images', '')+storedURL)
             with open(settings.MEDIA_ROOT.replace('images', '')+storedURL, "wb+") as destination:
                for chunk in imagefile.chunks():
                    destination.write(chunk)
    else:
       form = AssetForm()

    global filters, sortByKey, selectedAssetsIndices

    # deal with add assets button to let us do something
    selectedAssetIndex = [] # use as mutable type 'out' parameter
    sortByKeytemp = []

    assetList = asset.objects.all().order_by(sortByKey).values()

    if request.method == 'POST':
        if 'add_asset' in request.POST:
            inputs ={
                'Name': request.POST.get('Name', None),
                'Location': request.POST.get('Location', None),
                'Value': request.POST.get('Value', None),
                'Subject': request.POST.get('Subject', None),
                'LastUpdated': datetime.now().strftime("%A, %d %B, %Y at %X")
            }
            if all(inputs.values()): # no 'none' values
                asset.objects.create(**inputs)
        elif 'select_all_assets' in request.POST:
            for item in asset.objects.all():
                selectedAssetsIndices.append(item.__dict__['id'])
        elif GetSelectedItemIndex(selectedAssetIndex, request.POST):
            selectedAssetsIndices.append(selectedAssetIndex[0])
        elif GetSortByKey(sortByKeytemp, request.POST):
            sortByKey = sortByKeytemp[0]
        elif 'filter_assets' in request.POST:
            filters = {
                'Subject': request.POST.get('SubjectFilter', None)
            }
            print(filters)
        if filters['Subject'] != None and filters['Subject']!='':
            assetList = asset.objects.filter(**filters).order_by(sortByKey).values()

    # return render
    return render(
        request, 
        "DjangoApp1/index.html",  # Relative path from the templates folder to the template file we want
        {
            'page': "Assets",
            'title' : "Assets",
            'content' : "Some Content",
            'tableHeaders': ["ID", "Name", "Location", "Subjects", "Value", "Last Updated", "Image"],
            'tableContent': assetList,
            'buttons': ['add_asset', 'select_assets'],
            'form': form
        }
    )

def SelectedAssetsPage(request):
    global selectedAssetsIndices

    # edit and deleting selected assets
    if request.method == 'POST':
        if 'edit_selected_assets' in request.POST:
            inputs ={
                'Name': request.POST.get('Name', None),
                'Location': request.POST.get('Location', None),
                'Subject': request.POST.get('Subject', None),
                'Value': request.POST.get('Value', None),
            }
            inputs = {k: v for k, v in inputs.items() if v is not None and v is not ''}
            for index in selectedAssetsIndices:
                asset.objects.filter(pk=index).update(**inputs)
        if 'delete_selected_assets' in request.POST:
            for index in selectedAssetsIndices:
                asset.objects.get(pk=index).delete()
                selectedAssetsIndices = []
        if 'clear_selected_assets' in request.POST:
            selectedAssetsIndices = []
    print(selectedAssetsIndices)

    assetList = []
    if len(selectedAssetsIndices)>0:
        for index in selectedAssetsIndices:
            dictionary = asset.objects.get(pk=index).__dict__
            del dictionary['_state']
            assetList.append(dictionary)

    # return render
    return render(
        request, 
        "DjangoApp1/index.html",  # Relative path from the templates folder to the template file we want
        {
            'page': "Selected Assets",
            'title' : "Selected Assets",
            'content' : "Edit the selected assets here by editing the parameters below and clicking 'edit'",
            'tableHeaders': ["ID", "Name", "Location", "Subject", "Value", "Last Updated", "Image"],
            'tableContent': assetList,
            'buttons': ['edit_selected_assets'],
        }
    )