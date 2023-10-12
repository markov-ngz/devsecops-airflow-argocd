from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import DeleteUser
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def index(request):
        return render(request, 'core/index.html')

def settings(request):
        return render(request, 'core/settings.html')

def delete_user_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DeleteUser(request.POST)

            if form.is_valid():
                if request.POST["delete_checkbox"]:
                    rem = User.objects.get(username=request.user)
                    if rem is not None:
                        rem.delete()
                        logout(request)
                        messages.info(request, "Your account has been deleted.")
                        return redirect(reverse("core:index"))
                    else:
                        messages.info(request, "There was an error.")
        else:
            form = DeleteUser()
        context = {'form': form}
        return render(request, 'core/delete_account.html', context)
        # if request.user.is_anonymous:
        #     return HttpResponse(render(request, "401.html"), status=401)