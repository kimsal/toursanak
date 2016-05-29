from django.http import HttpResponse
from django.shortcuts import *
from toursanak.models import *
from django.core import serializers
from .forms import *
from django.contrib import messages
from itertools import chain
import re
from django.core.mail import EmailMessage
from django.db.models import Q
#db.execute('CREATE FULLTEXT INDEX toursanak_title ON toursanak_tour (title, body)')
def index(request):
  tours = Tour.objects.raw('select * from toursanak_tour ORDER BY toursanak_tour.id DESC limit 15')
  return render(request,'index.html',{'tours':tours})
def contact(request):
  frm =ContactForm(request.POST or None)
  context={
    "frm":frm,
  }
  return render(request,'contact.html',context)
def single(request, slug):
  tours=Tour.objects.raw("select toursanak_tour.id,toursanak_tour.title,toursanak_tour.short_description,toursanak_tour.banner,toursanak_tour.description,toursanak_tour.keywords,toursanak_tour.feature_image,toursanak_tour.map, array_to_string(array_agg(toursanak_image.imagename), ',')  as imagename from toursanak_tour, toursanak_image where toursanak_tour.id=toursanak_image.tour_id AND toursanak_tour.slug='{}' group by toursanak_tour.id".format(slug))
  tab=0
  related=''
  for tour in tours:
    tab=tour.id
    related=tour.category_id
  related_posts=Tour.objects.raw("select * from toursanak_tour where category_id={} ORDER BY toursanak_tour.id DESC limit 4".format(related))
  related_footer=Tour.objects.raw("select * from toursanak_tour ORDER BY id DESC LIMIT 4");
  if tab!=0:
    tabs=''
    #tabs=Tab.objects.raw("Select * from toursanak_tab where tour_id={}".format(tab))
    #tabs=Tab.objects.raw("select id,title,(select STRING_AGG((select toursanak_tabdetail.title from toursanak_tabdetail where tb_td.id=toursanak_tabdetail.id limit 1), ';') as tabdescription  from toursanak_tabdetail as tb_td INNER JOIN toursanak_tab ON toursanak_tab.id=tb_td.tab_id where toursanak_tab.id=t1.id) as descript from toursanak_tab as t1 where tour_id={}".format(tab))
    #tabs=Tab.objects.raw("Select tb1.id,tb1.title,(Select array_to_string(ARRAY[array_agg(tb2.title),array_agg(tb2.description)],'$$$' ) as  descript from toursanak_tabdetail as tb2 where tb1.id=tb2.tab_id ) from toursanak_tab as tb1 where tb1.tour_id={}".format(tab))
    #tabs=Tab.objects.raw("select id,title,(select GROUP_CONCAT(';;;',toursanak_tabdetail.title,'$$$',toursanak_tabdetail.description) as tabdescription  from toursanak_tabdetail INNER JOIN toursanak_tab ON toursanak_tab.id=toursanak_tabdetail.tab_id where toursanak_tab.id=t1.id) as descript from toursanak_tab as t1 where tour_id={}".format(tab))
    tabs=Tab.objects.raw("Select toursanak_tab.id,toursanak_tab.title,toursanak_tabdetail.title as ttitle,toursanak_tabdetail.description from toursanak_tab inner join toursanak_tabdetail on toursanak_tab.id=toursanak_tabdetail.tab_id where toursanak_tab.tour_id={}".format(tab))
    tabhead=Tab.objects.raw("Select * from toursanak_tab where toursanak_tab.tour_id={}".format(tab))
    schedules=Schedule.objects.raw("select * from toursanak_schedule where tour_id={}".format(tab))
    #return HttpResponse(tabs.query)
    #data = serializers.serialize('json', tabs)
    #return HttpResponse(tabs.query)
    return render(request,'single.html',{'tabhead':tabhead,'tours':tours,'schedules':schedules,'tabs':tabs,'related_posts':related_posts,'related_footer':related_footer,'tour_id':tab})
  else:
    return render(request,'404.html')
def category(request,slug):
  tours = Tour.objects.raw("select * from toursanak_tour INNER JOIN toursanak_category ON toursanak_tour.category_id=toursanak_category.id where toursanak_category.slug='{}' limit 15".format(slug))
  return render(request,'category.html',{'tours':tours,'slug':slug})
def getCategory(request):
  context={}
  context['categories']=Category.objects.all()
  return context
def createContact(request):
  if request.method == 'POST':
    form=ContactForm(request.POST)
    if form.is_valid():
      try:
        name=form.cleaned_data['contactName']
        email=form.cleaned_data['contactEmail']
        description=form.cleaned_data['contactDescription']
        r=Contact(name=name,email=email,description=description)
        r.save()
        body="Please keep in touch with the customer. Customer request is:\n{}\n----------------------\nFrom: {}".format(description,email)
        #return HttpResponse(r)
        e = EmailMessage('New Contact request From {}. '.format(name), body, to=['toursanak@gmail.com'])
        e.send()
        messages.add_message(request, messages.SUCCESS, "Your request sent succesfully. We'll contact you soon!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
      except:
        return redirect('/contact',{'name':name,'email':email,'description':description})
    else:
      messages.add_message(request, messages.ERROR, "Your information is not valid!")
      return redirect('/contact',{})
  else:
    messages.add_message(request, messages.ERROR, "Sorry we can't write your contact!")
    return redirect('/contact',{})
def PostScroll(request,id):
  ScrollTours = Tour.objects.raw("select * from toursanak_tour ORDER BY id DESC limit 6 OFFSET {}".format(id))
  data = serializers.serialize('json', ScrollTours)
  return HttpResponse(data)
def scrollCategory(request,slug,id):
  ScrollTours = Tour.objects.raw("select * from toursanak_tour INNER JOIN toursanak_category on toursanak_tour.category_id=toursanak_category.id where toursanak_category.slug='{}' ORDER BY toursanak_tour.id DESC limit 6 OFFSET {}".format(slug,id))
  data = serializers.serialize('json', ScrollTours)
  return HttpResponse(data)
def booking(request,tour_id,schedule_id):
  frm =BookingForm(request.POST or None)
  schedule = Schedule.objects.raw("select * from toursanak_schedule where id={} limit 1".format(schedule_id))
  return render(request,'booking.html',{'schedule':schedule,'tour_id':tour_id,'frm':frm})
def createBooking(request,tour_id,schedule_id):
  if request.method == 'POST':
    form=BookingForm(request.POST)
    if form.is_valid():
      try:
        name=form.cleaned_data['bookingName']
        email=form.cleaned_data['bookingEmail']
        description=form.cleaned_data['bookingDescription']
        #r=Booking(name=name,email=email,description=description,tour_id=tour_id,schedule_id=schedule_id)
        #r.save()

        tour=Tour.objects.raw("select * from toursanak_tour inner join toursanak_schedule on toursanak_tour.id=toursanak_schedule.tour_id where toursanak_tour.id={} AND toursanak_schedule.id={}".format(tour_id,schedule_id))
        
        t_title=''
        tour_url=''
        tour_startdate=''
        tour_enddate=''
        tour_price=''
        for t in tour:
          t_title=t.title
          tour_url="http://{}/{}".format(request.META['HTTP_HOST'],t.slug)
          tour_startdate=t.start_date
          tour_enddate=t.end_date
          tour_price=t.price
          body="Hello"
          #body="{}\n\nMore info:\nTour:{}\nStart date: {}\nEnd date: {}\nPrice: ${} \nTour url: {}\n\n From: {}".format(description,t.title,tour_startdate,tour_enddate,tour_price,tour_url,email)
          body="{}\n\nMore info:\nTour:{}\nStart date: {}\nEnd date: {}\nPrice: ${} \nTour url: {}\n\n From: {}".format(description,t.title,tour_startdate,tour_enddate,tour_price,tour_url,email)
          #body="hello"
          e = EmailMessage('New booking request From {}'.format(name), body, to=['kimsalsan007@gmail.com'])
          e.send()
        messages.add_message(request, messages.SUCCESS, "Your booking sent succesfully. We'll contact you soon!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
      except:
        raise
        messages.add_message(request, messages.ERROR, 'Sorry, Internal error!')
        return redirect('/{}/{}/booking'.format(tour_id,schedule_id),{'name':name,'email':email,'description':description})
    else:
      messages.add_message(request, messages.ERROR, "Your information is not valid!")
      return redirect('/{}/{}/booking'.format(tour_id,schedule_id),{})
  else:
    messages.add_message(request, messages.ERROR, "Sorry we can't write your contact!")
    return redirect('/{}/{}/booking'.format(tour_id,schedule_id),{})
def search(request):
  #search_data=Tour.objects.raw("SELECT * FROM toursanak_tour where  to_tsvector('simple', concat_ws(' ', title)) @@ to_tsquery('{}') ORDER BY id DESC limit 15".format(request.GET['q']))
  search_data=Tour.objects.raw("select * from toursanak_tour where  title like 'title'")
  return render(request,'search.html',{'tours':search_data})
def getTabDetail(request,tab_id):
  #return HttpResponse(tab_id)
  result=TabDetail.objects.raw("Select * from toursanak_tabdetail as t1 where t1.tab_id={} ORDER BY t1.id ".format(tab_id))
  data = serializers.serialize('json', result)
  return HttpResponse(data)


