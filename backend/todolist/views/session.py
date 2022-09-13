from django.contrib.auth import(
    authenticate,
    login,
    logout
)
from django.http import JsonResponse


def login_view(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'authentication': 'success'})
    else:
        return JsonResponse({'authentication': 'fail'}, status=401)


def logout_view(request):
    logout(request)
    return JsonResponse({'authentication': 'logout'})
