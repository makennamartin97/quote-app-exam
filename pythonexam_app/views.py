from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'login.html')

def register(request):
    print(request.POST)
    responsefromValidator = User.objects.registerValidator(request.POST)
    print(responsefromValidator)
    if len(responsefromValidator) > 0:
        for key, value in responsefromValidator.items():
            messages.error(request, value)
        return redirect('/')
    else:
        securepassword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(securepassword)
        newuser = User.objects.create(firstname = request.POST['firstname'], email = request.POST['email'], password = securepassword)
        request.session['loggedinID'] = newuser.id
        return redirect('/quotes')

def success(request):
    if 'loggedinID' not in request.session:
        return redirect('/')
    loggedinuser = User.objects.get(id= request.session['loggedinID'])
    #allitems = Item.objects.get(id=request.session['item'])
    context = {
        'loggedinuser': loggedinuser,
        'allquotes': Quote.objects.all(),
        'allusers': User.objects.all(),
        #'getuser': User.objects.get(id=user_id),
        'myquotes': Quote.objects.filter(Q(uploader=User.objects.get(id=request.session['loggedinID'])) | Q(favoriters = User.objects.get(id=request.session['loggedinID']))),
        #'getquote': Quote.objects.get(id=request.session['quote_id']),
    
        #'newquote': Quote.objects.create(quotemessage= request.POST['message'], uploader=User.objects.get(id=request.session['loggedinID']), quotedby = request.session['quoter']),
        'otherquotes' : Quote.objects.exclude(Q(uploader=User.objects.get(id=request.session['loggedinID'])) | Q(favoriters = User.objects.get(id=request.session['loggedinID']))),
        }
    return render(request, 'quotes.html', context)

def login(request):
    print(request.POST)
    loginerrors = User.objects.loginValidator(request.POST)
    if len(loginerrors) >0:
        for key, value in loginerrors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        loggedUser = User.objects.filter(email = request.POST['email'])[0]
        print(loggedUser)
        request.session['loggedinID'] = loggedUser.id
        return redirect('/quotes')
    
def logout(request):
    request.session.clear()
    return redirect('/')

def uploadquote(request):
    errors = Quote.objects.quoteValidator(request.POST)
    Quote.objects.quoteValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    newquote = Quote.objects.create(quotemessage= request.POST['message'],quotedby=request.POST['quoter'], uploader=User.objects.get(id=request.session['loggedinID']))
    allquotes = Quote.objects.all()
    #print('newquote')
    return redirect('/quotes')

def addtofavorites(request, quote_id):
    quoteobj = Quote.objects.get(id=quote_id)
    userobj = User.objects.get(id=request.session['loggedinID'])
    quoteobj.favoriters.add(userobj)

    return redirect('/quotes')
def removefromfavorites(request, quote_id):
    quoteobj = Quote.objects.get(id=quote_id)
    userobj = User.objects.get(id=request.session['loggedinID'])
    quoteobj.favoriters.remove(userobj)
    return redirect('/quotes')

def delete(request, quote_id):
    quoteobj = Quote.objects.get(id=quote_id)
    quoteobj.delete()
    return redirect('/quotes')

def editpage(request, quote_id):
    context = {
        'getquote': Quote.objects.get(id=quote_id)
        }
    return render(request, 'editquote.html', context)

def edit(request, quote_id):
    errors = Quote.objects.quoteValidator(request.POST)
    #getquote = Quote.objects.get(id= quote_id)
    print (errors)
    print(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/quotes/{quote_id}')
    else:
        c = Quote.objects.get(id= quote_id)
        #c.uploader = User.objects.get(id=request.session['loggedinID'])
        #getquote.message = Quote.objects.get(quotemessage = request.POST['message'])
        c.quotemessage = request.POST['message']
        c.quotedby = request.POST['quoter']
        #c.uploader = request.POST['uploader']
        c.save()
        print(c)
        print('********')
        print(request.POST)
        messages.success(request, "Quote successfully updated")
    return redirect(f'/quotes/{quote_id}')

def posts(request, user_id):
    getuser = User.objects.get(id=user_id)
    context = {
        'allquotes': Quote.objects.filter(uploader=getuser),
        'getuser' : User.objects.get(id=user_id),
        }
    return render(request, 'postsbyuser.html', context)

##def success(request):
    #return render(request, 'quotes.html')


# Create your views here.
