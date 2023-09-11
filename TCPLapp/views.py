import os
from django.conf import settings
from django.shortcuts import render,HttpResponse,redirect, get_object_or_404 ,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from .models import Customer2, DownloadFile, Location, UploadedFile, VillageBoundary, Revenue1,FinalPlu,Payment

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import LoginView
from .models import UploadedFile
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.serializers.geojson import Serializer as GeoJSONSerializer
from django.contrib.gis.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
import json
import geopandas as gpd
from pyproj import CRS
import requests
from django.contrib import messages
from .forms import CustomerProfileForms,CustomerRegiForm, LoginForm

#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas
from io import BytesIO
import io
from django.contrib.auth import authenticate
# from .forms import uploadFileForm
from collections import OrderedDict
 
import re
###################### new code ##########################



from django.contrib.auth.views import LoginView
# from django.shortcuts import redirect

class CustomerRegistrationForm(View):
    def get(self,request):
        form=CustomerRegiForm()
        
        return render(request,'TCPLapp/customerregistration.html',{"form":form})
    
    def post(self,request):
        form=CustomerRegiForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request,'TCPLapp/customerregistration.html',{"form":form})


class CustomLoginView(LoginView):
    template_name = "TCPLapp/login.html"
    authentication_form = LoginForm  # Use Django's built-in AuthenticationForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Authenticate the user using Django's built-in authentication
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)  # Log in the authenticated user
            if username == 'admin123':
                return redirect('admin123')
            else:
                try:
                    customer = Customer2.objects.get(user=user)
                    return redirect('basemap')
                except Customer2.DoesNotExist:
                    return redirect('profile')

        return super().form_valid(form)
    
def admin123(request):
    data1=User.objects.all()
   
    count=data1.count()                                                                               
    
    context={'data1':data1,'count':count}
    return render(request, 'TCPLapp/admin123.html',context)

def customer_details(request,id):
    data1= Customer2.objects.filter(user_id=id)
    print(data1,'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
    customer_details=[]
    
    for i in data1:
       
        user=i.user_id
        fullname=i.fullname
        mobileno=i.mobileno
        occupation=i.occupation
        industry=i.industry
                
        customer_data = {'user': user, 'fullname':fullname,'mobileno':mobileno,'occupation':occupation,'industry':industry}

        # print(customer_data,'anuppppp')
        customer_details.append(customer_data)
        
        # print(customer_details,'aaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            
   
  
    return render(request, 'TCPLapp/customer_details.html',{'customer_details':customer_details})




#_____________ profile _____________________________
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForms()
        return render(request,'TCPLapp/profile.html',{"form":form,"active":"btn-primary"})
    
    def post(self,request):
        form=CustomerProfileForms(request.POST)
        if form.is_valid():
            usr=request.user
            fullname=form.cleaned_data["fullname"]
            
            mobileno=form.cleaned_data["mobileno"]
            
            dob=form.cleaned_data["dob"]
            
            city=form.cleaned_data["city"]
            
            pin_code=form.cleaned_data["pin_code"]
            
            address=form.cleaned_data['address']
            
            occupation=form.cleaned_data["occupation"]

            industry = form.cleaned_data["industry"]
            
            reg=Customer2(user=usr,fullname=fullname,mobileno=mobileno,city=city,pin_code=pin_code,occupation=occupation,address=address,dob=dob,industry=industry)#
            
            reg.save()
            messages.success(request,"Congratulations !! Profile Updated Successfully")
       
            return render(request, 'TCPLapp/profile.html',{"form":form,"active":"btn-primary"})

#_______________user_details______________________
@login_required
def user_details(request):
    add=Customer2.objects.filter(user=request.user) 
    # print(add,'aaaaaa')#This is to get the current user,it solve the problem like to store user in login as a session.
    
    return render(request, 'TCPLapp/user_details.html',{"add":add,"active":"btn-primary"})
    

    

@login_required(login_url="login")
def changepassword(request):
    
    return render(request, 'TCPLapp/changepassword.html')



########################################################


def basemap(request):
    return render(request, 'TCPLapp/basemap.html')


def index(request):
    return render(request, 'TCPLapp/index.html')
@login_required(login_url="login")
def logout(request):
    # Do not use "return render" here
    # return render(request, 'TCPLapp/login.html')
    return redirect("login")
@login_required(login_url="login")
def zoneDetail(request):
      return render(request, 'TCPLapp/zoneDetail.html')
@login_required(login_url="login")
def planSurvey(request):
      return render(request, 'TCPLapp/planSurvey.html')
  
@login_required(login_url="login") 
def mapCalculator(request):
      return render(request, 'TCPLapp/mapCalculator.html')
  
  
def upload_file_page(request):
      return render(request, 'TCPLapp/upload_file.html')
    
@login_required(login_url="login")
def before_payment(request):
      add=Customer2.objects.filter(user=request.user)
      return render(request, 'TCPLapp/before_payment.html',{"add":add})
    
@login_required(login_url="login")
def payment_done(request):
    user=request.user  
    cust=Customer2.objects.filter(user=user)
    pay=Payment(user=user).save()
    
    return redirect("upload_file")


@login_required
def upload_file_page(request):
    return render(request, 'TCPLapp/upload_file.html')

@login_required
# @staticmethod   
def upload_file(request):
        if request.method == 'POST' and 'file' in request.FILES:
            # Check if the user is authenticated
            if request.user.is_authenticated:
                uploaded_file = request.FILES['file']
                allowed_extensions = ['.jpg', '.jpeg', '.pdf', '.tif', '.tiff']

                if any(uploaded_file.name.lower().endswith(ext) for ext in allowed_extensions):
                    # Save the uploaded file using the model
                    uploaded_file_instance = UploadedFile(files1=uploaded_file, user_id1=request.user)
                    uploaded_file_instance.save()

                    message = 'File uploaded successfully!'
                else:
                    message = 'Invalid file format. Allowed formats: JPG, PDF, TIFF.'
            else:
                message = 'User is not authenticated.'
        else:
            message = ''
        return render(request, 'TCPLapp/upload_file.html', {'message': message})
    
@login_required(login_url="login")
def download_file(request):
    files = DownloadFile.objects.filter(user_id1=request.user)
    print(request.user,"...............")
    return render(request, "TCPLapp/user_details.html", {"files": files})    

@login_required(login_url="login")
def user_details(request):
    add=Customer2.objects.filter(user=request.user) 
    #This is to get the current user,it solve the problem like to store user in login as a session.
    
    file=UploadedFile.objects.filter(user_id1=request.user)
    
    files = DownloadFile.objects.filter(user_id1=request.user)
    
    return render(request, 'TCPLapp/user_detailss.html',{"add":add,"file":file,"files":files,"active":"btn-primary"})



    
##############################search_button orginal#######################################################################

pattern =r'(^(?P<village_name>[\w\s\(\)\.-]+),(?P<taluka_name>[\D\\w\s\(\)\.-]+)(?:,(?P<gut_numbers>\d+(?:,\d+)*))?$)|(?P<xy>\b\d+\.\d+\s*,\s*\d+\.\d+\b)'


def getInfoValues(request):
    selected_layer = request.GET.get('selected_layer')
    print(selected_layer,"______________________________________")
    if request.method == 'POST':
        selected_value = request.POST.get('radio_field')


                
    return JsonResponse(products1, safe=False)           
            


def autocomplete(request):
    term = request.GET.get('term')
    if term is not None:
        products = VillageBoundary.objects.filter(village_name_revenue__istartswith=term).values_list('village_name_revenue','taluka')
        products_list1 = list(set(products))
        products_list = [','.join(t) for t in products_list1]
        
    return JsonResponse(products_list, safe=False)

def convert_To_Geojson(products1):
    coordinates_list = []
    for instance in  products1:   
        geom_geojson = GEOSGeometry(json.dumps({"type": "MultiPolygon", "coordinates": [instance.geom.coords[0]]}))
        feature = {
        "type": "Feature",
        "geometry": json.loads(geom_geojson.geojson),
        "properties": {
            "village_name_revenue": instance.village_name_revenue,
            "taluka": instance.taluka,
                        } }
        coordinates_list.append(feature)
        geojson_data = {
                    "type": "FeatureCollection",
                    "features": coordinates_list
                            }
    return geojson_data

def searchOnClick(request):
    response = request.GET.get("selected_value").split(",")
    respo = ','.join(response)
    sd_values = re.compile(pattern)
    sd = re.finditer(sd_values,respo)
    for s in sd:
        if bool(s.group('gut_numbers'))== True:
            tr123 = list(s.group('gut_numbers').split(","))
            products1 = Revenue1.objects.filter(taluka=s.group('taluka_name'), village_name_revenue=s.group('village_name'), gut_number__in= tr123)
            geojson_gut = convert_To_Geojson(products1)
        elif bool(s.group('village_name'))== True:           
            products1 = VillageBoundary.objects.filter(taluka=s.group('taluka_name'), village_name_revenue=s.group('village_name'))
            geojson_gut = convert_To_Geojson(products1)
            
        elif bool(s.group('xy'))== True:  
            coordinates_list =[]
            latitude, longitude = [float(coord) for coord in s.group('xy').split(',')]
            geom_geojson = GEOSGeometry(json.dumps({"type": "Point", "coordinates": [longitude, latitude]}))
            feature = {
            "type": "Feature",
            "geometry": json.loads(geom_geojson.geojson),
                            }
            coordinates_list.append(feature)
            geojson_data = {
                        "type": "FeatureCollection",
                        "features": coordinates_list
                                }
            geojson_gut = geojson_data
        
    return JsonResponse(geojson_gut, safe=False)



# ****************PDF TABLE***************************************

def Out_table(request):
    
    response = request.GET.get("selected_value").split(",")
    villageName, talukaName, gutNumber = response[0], response[1], response[2:]
    gutnumber2=response[2:]
    
    
    products1 = Revenue1.objects.filter(taluka=talukaName, village_name_revenue=villageName, gut_number=str(gutNumber[0]))
    intersection_query = Q(geom__intersects=products1[0].geom)
    
    
    for product in products1[1:]:
        intersection_query |= Q(geom__intersects=product.geom)
    plu = FinalPlu.objects.filter(intersection_query)
    data = []
    for Iplu in plu:
        intersection_area = Iplu.geom.intersection(products1[0].geom).area
      
        data.append(Iplu.broad_lu)
        data.append(intersection_area)
        
    data1 = {
        
        "Village_Name": villageName,
        "Taluka_Name": talukaName,
        "Gut_Number": gutNumber,
        "selected_values": data
    }

   
    
    return JsonResponse(data1,safe=False)



def Queryform(request):
    data = request.POST.get('data')
    
    
    return render (request,'TCPLapp/Queryform.html')



#############################################################changesearchdata##############################################################
# 

# Save BookMarks_____________________________

@csrf_exempt
@login_required
def save_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        name = request.POST.get('name')
        username = request.POST.get('username')

        location = Location(user=request.user, name=name,
                            latitude=latitude, longitude=longitude)
        location.save()

        return JsonResponse({'message': 'Location saved successfully.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'})


def get_locations(request):
    locations = Location.objects.filter(user=request.user)
    data = {
        'locations': list(locations.values('id','name', 'latitude', 'longitude'))
    }
    return JsonResponse(data)

#delete_location
@csrf_exempt
@login_required
def delete_location(request):
    if request.method == 'POST':
        location_id = request.POST.get('locationId')
        try:
            location = Location.objects.get(id=location_id)
            if location.user == request.user:
                location.delete()
                return JsonResponse({'message': 'Location deleted successfully.'})
            else:
                return JsonResponse({'message': 'Unauthorized access.'}, status=401)
        except Location.DoesNotExist:
            return JsonResponse({'message': 'Location not found.'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)
    
def locations(request):
    return render(request,"TCPLapp/search_location.html")    
 
 
###################################################searchby coordinates#################################################################################### 
 
# def Search_cordinates(request):
#     Term=request.GET.get('term')
#     if Term is not None:
#         coordinates_database=Revenue1.objects.filter(geom=geom)
#         coordinates=re.match('([\d.]+?)\s([\d.]+?)\s([\d.]+?)',coordinates_database)
#         print(coordinates)
#     return JsonResponse(coordinates, safe=False)    

#     # foo = "SRID=4326;MULTIPOLYGON(((352877.02163887 1233618.83923531 5,352872.32998848 1233609.44478035 5,352867.693426132 1233612.15611458 5,352861.67354393 1233602.76770592 5,352841.814386368 1233616.9818058 5,352848.495328903 1233625.69463921 5,352861.076768875 1233617.56668663 5,352866.429475784 1233626.28557014 5,352877.02163887 1233618.83923531 5)))"
#     # print (re.findall('([\d.]+?)\s([\d.]+?)\s([\d.]+?)', foo))
    
#1way
# def Search_coordinates(request):
#     term = request.GET.get('term')
#     if term is not None:
#         # Assuming 'geom' is a field in the Revenue1 model
#         coordinates_data = Revenue1.objects.filter(geom__icontains=term)

#         coordinates_list = []
#         for data in coordinates_data:
#             coordinates_match = re.match(r'([\d.]+)\s([\d.]+)\s([\d.]+)', data.geom)
#             if coordinates_match:
#                 coordinates_list.append({
#                     'latitude': coordinates_match.group(1),
#                     'longitude': coordinates_match.group(2),
#                     'altitude': coordinates_match.group(3)
#                 })

#         return JsonResponse(coordinates_list, safe=False)

#     return JsonResponse({'error': 'No search term provided'}, status=400)

# def selected_data(request):
#     response = request.GET.get("selected_value")
#     geom=response.geom[0]
#     products1 = Revenue1.objects.filter(geom=geom)
#     geojson_gut = convert_To_Geojson(products1)
    
   
#     return JsonResponse(geojson_gut, safe=False)

# def convert_To_Geojson(products1):
#     for instance in  products1:
#         coordinates_list = []
       
#         geom_geojson = GEOSGeometry(json.dumps({"type": "MultiPolygon", "coordinates": [instance.geom.coords[0]]}))
      
#         feature = {
#         "type": "Feature",
#         "geometry": json.loads(geom_geojson.geojson),
#         "properties": {
#             "geom":instance.geom
#             #"gut_number":instance.gut_number,
            
            
#                         } }
#         coordinates_list.append(feature)
#         geojson_data = {
#                     "type": "FeatureCollection",
#                     "features": coordinates_list
#                             }
  
#     return geojson_data
    

# #2ways

# def Search_coordinates(request):
#     term = request.GET.get('term')
#     coordinates = []

#     if term is not None:
#         # Assuming that 'geom' is a field in your Revenue1 model
#         coordinates_queryset = Revenue1.objects.filter(geom__contains=term)

#         for item in coordinates_queryset:
#             # Assuming that 'geom' is a string field containing coordinates like "x y z"
#             match = re.match(r'([\d.]+)\s([\d.]+)\s([\d.]+)', item.geom)
#             if match:
#                 x_coord, y_coord, z_coord = map(float, match.groups())
#                 coordinates.append({'x': x_coord, 'y': y_coord, 'z': z_coord})

#     return JsonResponse(coordinates, safe=False)

#3way
# def Search_coordinates(request):
#     Term = request.GET.get('term')
#     if Term is not None:
#         coordinates_queryset = Revenue1.objects.filter(geom__icontains=Term)
        
#         coordinates_list = []
#         for item in coordinates_queryset:
#             # Assuming geom contains a string like "x y z", split and convert to float
#             x, y, z = re.findall(r'([\d.]+)', item.geom)
#             coordinates_list.append({'x': float(x), 'y': float(y), 'z': float(z)})
        
#         return JsonResponse(coordinates_list, safe=False)
    
#     return JsonResponse([], safe=False)




