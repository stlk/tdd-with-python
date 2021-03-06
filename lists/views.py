from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
User = get_user_model()

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_, data=request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        if not isinstance(request.user, AnonymousUser):
            list_.owner = request.user
            list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})

def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    list_.shared_with.add(request.POST['email'])
    return redirect(list_)