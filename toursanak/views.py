from django.http import HttpResponse
from django.shortcuts import *
from toursanak.models import *
from django.core import serializers
from .forms import *
from django.contrib import messages
from itertools import chain
import re
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
		schedules=Schedule.objects.raw("select * from toursanak_schedule where tour_id={}".format(tab))
		return render(request,'single.html',{'tours':tours,'schedules':schedules,'tabs':tabs,'related_posts':related_posts,'related_footer':related_footer,'tour_id':tab})
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
	ScrollTours = Tour.objects.raw("select * from toursanak_tour ORDER BY id DESC limit {},3".format(id))
	data = serializers.serialize('json', ScrollTours)
	return HttpResponse(data)
def scrollCategory(request,slug,id):
	ScrollTours = Tour.objects.raw("select * from toursanak_tour INNER JOIN toursanak_category on toursanak_tour.category_id=toursanak_category.id where toursanak_category.slug='{}' ORDER BY toursanak_tour.id DESC limit {},3".format(slug,id))
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
				r=Booking(name=name,email=email,description=description,tour_id=tour_id,schedule_id=schedule_id)
				r.save()
				messages.add_message(request, messages.SUCCESS, "Your booking sent succesfully. We'll contact you soon!")
				return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
			except:
				messages.add_message(request, messages.ERROR, 'Sorry, Internal error!')
				return redirect('/{}/{}/booking'.format(tour_id,schedule_id),{'name':name,'email':email,'description':description})
		else:
			messages.add_message(request, messages.ERROR, "Your information is not valid!")
			return redirect('/{}/{}/booking'.format(tour_id,schedule_id),{})
	else:
		messages.add_message(request, messages.ERROR, "Sorry we can't write your contact!")
		return redirect('/{}/{}/booking'.format(tour_id,schedule_id),{})
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 
def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
def search(request):
  #return HttpResponse("HELLO")
	#search_data=Tour.objects.raw("SELECT * FROM toursanak_tour WHERE to_tsvector('simple', concat_ws(' ', title, description)) @@ 'kimsal' ORDER BY toursanak_tour.id DESC LIMIT 15;".format(request.GET['q']))
	search_data=Tour.objects.raw("SELECT * FROM toursanak_tour where  to_tsvector('simple', concat_ws(' ', title, description,short_description)) @@ to_tsquery('{}') ORDER BY id DESC limit 15".format(request.GET['q'].replace(' ','&')))
	return render(request,'search.html',{'tours':search_data})
