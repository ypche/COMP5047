from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView,TemplateView
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
import serial
from django.shortcuts import render, get_object_or_404
from myhome.models import Seneor
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
import json
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from .forms import  RegisterForm, UserInfoForm



# Create your views here.
class MyHomeListView(ListView):
    template_name = 'myhome.html'
    context_object_name = 'notifications'
    # login_url = '/auth/login/'

    def get_queryset(self):
        daydata = Seneor.objects.all().order_by('-time')[:240]
        mark_data = Seneor.objects.all().order_by('-time')[:5]
        data = []
        category = []
        tdata = []
        hdata = []
        # for _ in alldata:
        #     json_data = {
        #         "id": _.id,
        #         "Tvalue":_.Tvalue
        #     }
        #
        #     data.insert(0,json_data)
        #
        # print(data)
        count = 1
        average_tvalue = 0
        average_hvalue = 0
        total_tvalue = 0
        total_tval = 0
        total_hvalue = 0
        total_hval = 0
        time_hour = 1
        for _ in daydata:
            compare_data = Seneor.objects.all().order_by('-time')[:5]
            if compare_data == mark_data:
                break
            else:
                total_tval = total_tval + _.Tvalue
                total_hval = total_hval + _.Hvalue
                if count % 10!=0:
                    total_tvalue = total_tvalue + _.Tvalue
                    total_hvalue = total_hvalue + _.Hvalue
                    count = count + 1

                else:
                    count = 1
                    average_tvalue = total_tvalue/10
                    average_hvalue = total_hvalue/10
                    json_category = {
                        "label": str(time_hour)
                    }
                    json_tdata = {
                        "value": str(round(average_tvalue, 3))
                    }
                    json_hdata = {
                        "value": str(round(average_hvalue, 3))
                    }
                    json_data = {
                        "label": str(time_hour),
                        "value": str(round(average_tvalue, 3)),
                    }

                    # data.insert(0, json_data)
                    category.insert(0, json_category)
                    tdata.insert(0, json_tdata)
                    hdata.insert(0, json_hdata)
                    time_hour = time_hour + 1
                    total_tvalue = 0
                    total_hvalue = 0

        json_data = {
            "label": category,
            "tdata": tdata,
            "hdata": hdata
        }
        data.insert(0, json_data)

        with open('static/json/data.json', 'w') as outfile:
            json.dump(data, outfile)
        with open('static/json/category.json', 'w') as outfile:
            json.dump(category, outfile)
        with open('static/json/tdata.json', 'w') as outfile:
            json.dump(tdata, outfile)
        with open('static/json/hdata.json', 'w') as outfile:
            json.dump(hdata, outfile)

        if total_tval / 60 > 30:
            Notification = "Warning: Today's temperature in your environment was too high."
            return Notification
        else:
            Notification = "Cool, the temperature in past 24 hours was perfect! ."
            return Notification
    

class IndexView(TemplateView):
    template_name = 'home.html'




# def ArdunioConnection(request):
#
#      ser = serial.Serial("/dev/cu.usbmodem1421", baudrate=9600)
#
#      while 1:
#          arduinoData = ser.readline().decode('ascii')
#          print(arduinoData)
#          data_display = arduinoData.replace(',', '').strip('\n').strip('\r')
#          print(data_display)
#          Tvalue = float(data_display[:5])
#          Hvalue = float(data_display[5:10])
#          Uvalue = int(data_display[10:])
#          print(Tvalue)
#          print(Hvalue)
#          print(Uvalue)
#
#          data = Seneor.objects.create(Tvalue=Tvalue, Uvalue=Uvalue, Hvalue=Hvalue)
#          data.save()
#
#          if(Uvalue <= 2):
#
#              if(Hvalue <=40):
#                  context = {'UVNote': 'UV value is low. You can go out and have fun!',
#                             'HNote': 'Humidity value is too low for your skin',
#                             'data': data}
#              elif(Hvalue >40 and Hvalue<=60):
#                  context = {'UVNote': 'UV value is low. You can go out and have fun!',
#                             'HNote': 'This is moderate humidity level for your skin. Enjoy your environment!',
#                             'data': data}
#              elif (Hvalue > 60):
#                  context = {'UVNote': 'UV value is low. You can go out and have fun!',
#                            'HNote': 'The humidity level is too high. Higher levels to allow dust mites to grow on skin and trigger for skin allergy.',
#                            'data': data}
#
#          elif(Uvalue > 2 and Uvalue <= 5):
#
#              if (Hvalue <= 40):
#                  context = {'UVNote': 'UV value is moderate. You can go out and fun! But you’d better to use sunscreen(SPF30) or sunglasses to protect your skin from aging causing by UV.',
#                             'HNote': 'Humidity value is too low for your skin',
#                             'data': data}
#              elif (Hvalue > 40 and Hvalue <= 60):
#                  context = {'UVNote': 'UV value is moderate. You can go out and fun! But you’d better to use sunscreen(SPF30) or sunglasses to protect your skin from aging causing by UV.',
#                             'HNote': 'This is moderate humidity level for your skin. Enjoy your environment!',
#                             'data': data}
#              elif (Hvalue > 60):
#                  context = {'UVNote': 'UV value is moderate. You can go out and fun! But you’d better to use sunscreen(SPF30) or sunglasses to protect your skin from aging causing by UV.',
#                             'HNote': 'The humidity level is too high. Higher levels to allow dust mites to grow on skin and trigger for skin allergy.',
#                             'data': data}
#          elif(Uvalue > 5 and Uvalue <= 7):
#
#              if (Hvalue <= 40):
#                  context = {
#                      'UVNote': 'UV value is high. Please use appropriate protection like sunscreen (SPF 50++), sunglasses, sun-protective clothing or slap.',
#                      'HNote': 'Humidity value is too low for your skin',
#                      'data': data}
#              elif (Hvalue > 40 and Hvalue <= 60):
#                  context = {
#                      'UVNote': 'UV value is high. Please use appropriate protection like sunscreen (SPF 50++), sunglasses, sun-protective clothing or slap.',
#                      'HNote': 'This is moderate humidity level for your skin. Enjoy your environment!',
#                      'data': data}
#              elif (Hvalue > 60):
#                  context = {
#                      'UVNote': 'UV value is high. Please use appropriate protection like sunscreen (SPF 50++), sunglasses, sun-protective clothing or slap.',
#                      'HNote': 'The humidity level is too high. Higher levels to allow dust mites to grow on skin and trigger for skin allergy.',
#                      'data': data}
#          elif(Uvalue > 8 and Uvalue <= 10):
#
#              if (Hvalue <= 40):
#                  context = {'UVNote': 'UV value is very high. You’d better stay indoors or use appropriate protection like sunscreen (SPF 50+++), sunglasses, sun-protective clothing or slap.',
#                             'HNote': 'Humidity value is too low for your skin',
#                             'data': data}
#              elif (Hvalue > 40 and Hvalue <= 60):
#                  context = {'UVNote': 'UV value is very high. You’d better stay indoors or use appropriate protection like sunscreen (SPF 50+++), sunglasses, sun-protective clothing or slap.',
#                             'HNote': 'This is moderate humidity level for your skin. Enjoy your environment!',
#                             'data': data}
#              elif (Hvalue > 60):
#                  context = {'UVNote': 'UV value is very high. You’d better stay indoors or use appropriate protection like sunscreen (SPF 50+++), sunglasses, sun-protective clothing or slap.',
#                             'HNote': 'The humidity level is too high. Higher levels to allow dust mites to grow on skin and trigger for skin allergy.',
#                             'data': data}
#          else:
#
#              if (Hvalue <= 40):
#                  context = {'UVNote': 'UV value is extremely strong. You should better stay indoors. The sun ultraviolet (UV) radiation is the major cause of skin cancer and cause of skin aging',
#                             'HNote': 'Humidity value is too low for your skin',
#                             'data': data}
#              elif (Hvalue > 40 and Hvalue <= 60):
#                  context = {'UVNote': 'UV value is extremely strong. You should better stay indoors. The sun ultraviolet (UV) radiation is the major cause of skin cancer and cause of skin aging',
#                             'HNote': 'This is moderate humidity level for your skin. Enjoy your environment!',
#                             'data': data}
#              elif (Hvalue > 60):
#                  context = {'UVNote': 'UV value is extremely strong. You should better stay indoors. The sun ultraviolet (UV) radiation is the major cause of skin cancer and cause of skin aging',
#                             'HNote': 'The humidity level is too high. Higher levels to allow dust mites to grow on skin and trigger for skin allergy.',
#                             'data': data}
#
#          break
#
#      ser.close()
#
#      return render(request, 'myhome.html', context)
import requests

def email_alert(first, second, third):
    report = {}
    report["value1"] = first
    report["value2"] = second
    report["value3"] = third
    requests.post("https://maker.ifttt.com/trigger/test_email/with/key/dSdWZmpGBUOhqoBu3uZ9KR", data=report)


from SkinHealth.tasks import test

def ArdunioConnection(request):
    ser = serial.Serial("/dev/cu.usbmodem1411", baudrate=9600)
    count = 0;
    while 1:
        arduinoData = ser.readline().decode('ascii')
        print(arduinoData)
        data_display = arduinoData.replace(',', '').strip('\n').strip('\r')
        print(data_display)
        Tvalue = float(data_display[:5])
        Hvalue = float(data_display[5:10])
        Uvalue = int(data_display[10:])
        print(Tvalue)
        print(Hvalue)
        print(Uvalue)
        # if (count==0):
        #     count = count + 1
        #     email_alert("hello \n","Handsome ","Chao")

        data = Seneor.objects.create(Tvalue=Tvalue, Uvalue=Uvalue, Hvalue=Hvalue)
        data.save()

        if (Tvalue <= 15):

            if (Hvalue <= 50):
                context = {'Note': ' The indoor temperature and humidity is low, please open the humidifier!',
                           'data': data}
                # email_alert("Dear client", " wanring", " the indoor temperature and humidity is low, please open the humidifier!")
            elif (Hvalue > 50):
                context = {'Note': 'The indoor temperature is low, and the Humidity value is high, please open the heater!',
                           'data': data}
            # email_alert("Dear client", " wanring", " the indoor temperature is low, and the Humidity value is high, please open the heater!")

        elif (Tvalue >15  and Tvalue <= 25):

            if (Hvalue <= 40):
                context = {
                    'Note': ' The indoor humidity is low, please open the humidifier!',
                    'data': data}
                # email_alert("Dear client", " wanring", " the indoor humidity is low, please open the humidifier!")
            elif (Hvalue > 40 and Hvalue <= 60):
                context = {
                    'Note': 'The indoor air quality is quite good now',
                    'data': data}
            elif (Hvalue > 60):
                context = {
                    'Note': 'The indoor temperature is proper, and the Humidity value is high, please open the heater!',
                    'data': data}
                # email_alert("Dear client", " wanring", "the indoor temperature is proper, and the Humidity value is high, please open the heater!")

        else :

            if (Hvalue <= 40):
                context = {
                    'Note': ' The indoor humidity is low,and temperature is quite high, please open the humidifier!',
                    'data': data}
                # email_alert("Dear client", " wanring", " the indoor humidity is low,and temperature is quite high, please open the humidifier!")

            elif (Hvalue > 40 and Hvalue <= 60):
                context = {
                    'Note': '',
                    'data': data}
            elif (Hvalue > 60):
                context = {
                    'HNote': 'The humidity level is too high. ',
                    'data': data}
                # email_alert("Dear client", " wanring", " the humidity level is too high. ")


        break

    ser.close()
    # test()

    return render(request, 'myhome.html', context)


def ArdunioReadLong(request):

     ser = serial.Serial("/dev/cu.usbmodem1411", baudrate=9600)

     count = 0

     while 1:
         arduinoData = ser.readline().decode('ascii')
         print(arduinoData)
         data_display = arduinoData.replace(',', '').strip('\n').strip('\r')
         print(data_display)
         Tvalue = float(data_display[:5])
         Hvalue = float(data_display[5:10])
         Uvalue = int(data_display[10:])
         print(Tvalue)
         print(Hvalue)
         print(Uvalue)

         data = Seneor.objects.create(Tvalue=Tvalue, Uvalue=Uvalue, Hvalue=Hvalue)
         data.save()

         count = count + 1

         if (count >= 2000):
            context = {'Loding': 'You have read 10 groups of value'}
            break
     ser.close()

     return render(request, 'myhome.html', context)




class UV_valueView(generic.ListView):
    template_name = "UV.html"
    def get_queryset(self):
        alldata = Seneor.objects.all().order_by('-time')[:100]
        return alldata




def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username","")
        pass_word = request.POST.get("password","")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            my_login(request, user)
            return render(request, "myhome.html")
        else:
            context = {'login_err': 'Username or Password is wrong!'}
            return render(request, "login.html", context)
    elif request.method == "GET":
        return render(request, "login.html",{})


def my_login(request, user):
    login(request, user)
    request.session['user_id'] = user.id


def user_logout(request):
    my_logout(request)
    return HttpResponseRedirect("/myhome/index")


def my_logout(request):
    logout(request)
    request.session['user_id'] = ''


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            my_register(request, username, password)
            return HttpResponseRedirect("/myhome")
    else:
        form = RegisterForm()
    return render(request, 'register.html', context={'form': form})


def my_register(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        my_login(request, user)

def Userinfo(request):
    return  render(request, 'user_profile.html',{})

def editprofile(request):
    user_info_form = UserInfoForm(request.POST, instance=request.user)
    if user_info_form.is_valid():
        user_info_form.save()
        return HttpResponseRedirect("/myhome/info")
    else:
        user_info_form = UserInfoForm()
    return render(request, 'edit_profile.html', context={'user_info_form': user_info_form})



class History_TvalueView(generic.ListView):
    template_name = "historyofTvalue.html"
    context_object_name = "Notification"

    def get_queryset(self):
        daydata = Seneor.objects.all().order_by('-time')[:240]
        mark_data = Seneor.objects.all().order_by('-time')[:5]
        data = []
        # for _ in alldata:
        #     json_data = {
        #         "id": _.id,
        #         "Tvalue":_.Tvalue
        #     }
        #
        #     data.insert(0,json_data)
        #
        # print(data)
        count = 1
        average_value = 0
        total_value = 0
        total_val = 0
        time_hour = 1
        for _ in daydata:
            compare_data = Seneor.objects.all().order_by('-time')[:5]
            if compare_data == mark_data:
                break
            else:
                total_val = total_val + _.Tvalue
                if count % 10!=0:
                    total_value = total_value + _.Tvalue
                    count = count + 1

                else:
                    count = 1
                    average_value = total_value/10
                    print(total_value)
                    print("average:", average_value)
                    json_data = {
                        "label": str(time_hour),
                        "value": str(round(average_value, 3)),
                    }
                    print(average_value)
                    data.insert(0, json_data)
                    time_hour = time_hour + 1
                    total_value = 0
        with open('static/json/data.json', 'w') as outfile:
            json.dump(data, outfile)

        if total_val / 60 > 30:
            Notification = "Warning: Today's temperature in your environment was too high."
            return Notification
        else:
            Notification = "Cool, the temperature in past 24 hours was perfect! ."
            return Notification


class History_UvalueView(generic.ListView):
    template_name = "historyofUvalue.html"
    context_object_name = "Notification"
    def get_queryset(self):
        daydata = Seneor.objects.all().order_by('-time')[:240]
        mark_data = Seneor.objects.all().order_by('-time')[:5]
        data = []
        total_val = 0
        count = 1
        average_value = 0
        total_value = 0
        time_hour = 1
        for _ in daydata:
            compare_data = Seneor.objects.all().order_by('-time')[:5]
            if compare_data == mark_data:
                break
            else:
                total_val = total_val + _.Hvalue
                if count % 10!=0:
                    total_value = total_value + _.Uvalue
                    count = count + 1

                else:
                    count = 1
                    average_value = total_value/10
                    print(total_value)
                    print("average:", average_value)
                    json_data = {
                        "id": time_hour,
                        "Uvalue": average_value
                    }
                    print(average_value)
                    data.insert(0, json_data)
                    time_hour = time_hour + 1
                    total_value = 0
        with open('static/json/data.json', 'w') as outfile:
            json.dump(data, outfile)

        if total_val / 60 > 30:
            Notification = "Warning: Today's UV value in your environment were too high."
            return Notification
        else:
            Notification = "Great! You did not expose to any intensity ultraviolet rays ."
            return Notification


class History_HvalueView(generic.ListView):
    template_name = "historyofHvalue.html"
    context_object_name = "Notification"

    def get_queryset(self):
        daydata = Seneor.objects.all().order_by('-time')[:240]
        mark_data = Seneor.objects.all().order_by('-time')[:5]

        data = []
        count = 1
        average_value = 0
        total_value = 0
        hour = 1
        total_val = 0

        for _ in daydata:
            compare_data = Seneor.objects.all().order_by('-time')[:5]
            if compare_data == mark_data:
                break
            else:
               # print("HAAAAAAAA")
               total_val = total_val + _.Hvalue
               if count % 10 != 0:
                   total_value = total_value + _.Hvalue
                   count = count + 1

               else:
                  count = 1
                  average_value = total_value / 10
                  json_data = {
                    "label": str(hour),
                    "value": str(round(average_value, 3)),
                  }
                  data.insert(0, json_data)
                  hour = hour + 1
                  total_value = 0


        with open('static/json/data.json', 'w') as outfile:
            json.dump(data, outfile)

        if total_val / 60 < 56:
            Notification = "The humidity level today was good for your skin. Enjoy your environment!"
            return Notification
        if total_val / 60 > 56:
            Notification = "warning: The humidity level today was too high. Higher levels to allow dust mites to grow on skin and trigger for skin allergy."
            return Notification


# history data of week
class week_HvalueView(generic.ListView):
    template_name = "week_Hvalue.html"
    context_object_name = "Notification"
    print("I am here0")

    def get_queryset(self):
        weekdata = Seneor.objects.all().order_by('-time')[:420]
        data = []
        count = 1
        average_value = 0
        total_value = 0
        day = 1
        total_val = 0

        for _ in weekdata:
            print("I am here2")
            total_val = total_val + _.Hvalue
            if count % 60 != 0:
                total_value = total_value + _.Hvalue
                count = count + 1
            else:
                count = 1
                average_value = total_value / 60
                json_data = {
                    "label": str(day),
                    "value": str(round(average_value, 3)),
                }
                data.insert(0, json_data)
                day = day + 1
                total_value = 0

        with open('static/json/data.json', 'w') as outfile:
            json.dump(data, outfile)

        if total_val / 60 > 38 and total_val / 60 < 56:
            Notification = "The humidity level in past 7 days was good for your skin. Enjoy your environment!"
            return Notification
        if total_val / 60 > 56 and total_val / 60 < 80:
            Notification = "warning: The humidity level in past 7 days was too high. Higher levels to allow dust mites to grow on skin and trigger for skin allergy."
            return Notification



class week_TvalueView(generic.ListView):
    template_name = "week_Tvalue.html"
    context_object_name = "Notification"

    def get_queryset(self):
        weekdata = Seneor.objects.all().order_by('-time')[:420]
        data = []
        count = 1
        average_value = 0
        total_value = 0
        day = 1
        total_val = 0
        for _ in weekdata:
            total_val = total_val + _.Tvalue
            if count % 60 != 0:
                total_value = total_value + _.Tvalue
                count = count + 1
            else:
                count = 1
                average_value = total_value / 60
                json_data = {
                    "label": str(day),
                    "value": str(round(average_value, 3)),
                }
                data.insert(0, json_data)
                day = day + 1
                total_value = 0

        with open('static/json/data.json', 'w') as outfile:
            json.dump(data, outfile)

        if total_val / 60 > 30:
            Notification = "Warning: The past 7 days's temperature in your environment was too high."
            return Notification
        else:
            Notification = "Cool, the temperature in past 7 days is perfect! ."
            return Notification

class week_UvalueView(generic.ListView):
    template_name = "week_Uvalue.html"
    context_object_name = "Notification"

    def get_queryset(self):
        weekdata = Seneor.objects.all().order_by('-time')[:420]
        data = []
        count = 1
        average_value = 0
        total_value = 0
        day = 1
        total_val = 0
        for _ in weekdata:
            total_val = total_val + _.Uvalue
            if count % 60 != 0:
                total_value = total_value + _.Uvalue
                count = count + 1
            else:
                count = 1
                average_value = total_value / 60
                json_data = {
                    "id": day,
                    "Uvalue": average_value
                }
                data.insert(0, json_data)
                day = day + 1
                total_value = 0

        with open('static/json/data.json', 'w') as outfile:
            json.dump(data, outfile)

        if total_val / 60 > 30:
            Notification = "Warning: The past 7 days's UV value in your environment were too high."
            return Notification
        else:
            Notification = "Great! You did not expose to any intensity ultraviolet rays ."
            return Notification
