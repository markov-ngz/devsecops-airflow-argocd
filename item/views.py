from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views import generic

from .models import *
from .forms import NewItemForm, EditItemForm

# Create your views here.
def index(request):
        items = Item.objects.order_by("created_at")
        context = {"items":items} # response must be a dict, not a QuerySet
        return render(request,"item/index.html", context)

def detail (request, pk):
        # try:
        #         item = Item.objects.get(pk=pk)
        # except Item.DoesNotExist : 
        #         raise Http404("Item do not exist or unauthorized access")
        item = get_object_or_404(Item, pk = pk)
        return render(request,"item/detail.html", {"item":item} )

def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST)
        if form.is_valid : 
            item = form.save(commit=False)
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html',{
                  'form':form,
                  'title':'Adding Items'
    })


def edit(request, pk ):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = EditItemForm(request.POST, instance=item)
        if form.is_valid : 
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html',{
                  'form':form,
                  'title':'Edit Items'
    })

def delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()

    return redirect('item:index')



