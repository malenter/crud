from django.shortcuts import render ,redirect ,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth import login ,logout,authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .froms import Taskfrom
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, "home.html")


def singnup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('task')
            except IntegrityError:
                return render(request, 'singup.html', {'form': UserCreationForm, 'error': 'Username already exits'})

        return render(request, 'singup.html', {'form': UserCreationForm, 'error': 'contraseñas no coninciden'})
@login_required
def task(request):
    tasks=Task.objects.filter(user=request.user,datecompleted__isnull=True)

    return render(request,'task.html',{'Tasks':tasks})
@login_required
def task_complete(request):
    tasks=Task.objects.filter(user=request.user,datecompleted__isnull=False).order_by('datecompleted')
    return render(request,'task.html',{'Tasks':tasks})
@login_required
def task_detail(request,task_id):
    if request .method =='GET':
        task=get_object_or_404(Task,pk=task_id,user=request.user)
        form=Taskfrom(instance=task)
        return render(request,'task_deatelle.html',{'task':task,'form': form})
    else:
         try:
             task= get_object_or_404(Task,pk=task_id)
             form=Taskfrom(request.POST,instance=task,user=request.user)
             form.save()
             return redirect('task')
        
         except ValueError:
              return render(request,'task_deatelle.html',{'task':task,'form': form,'error':'error al cargar la task'})
@login_required
def complete_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request .method =='POST':
        task.datecompleted=timezone.now()
        task.save()
        return redirect('task') 
@login_required
def delete_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request .method =='POST':
        task.delete()
        return redirect('task') 
@login_required        
def signaout(request):
    logout(request)
    return redirect('home')

def siging(request):
    if request.method =='GET':
         return render(request,'login.html',{'form':AuthenticationForm})
    else:
         user=authenticate(request,username=request.POST['username'], password=request.POST['password'])
         if user is None:
              return render(request,'login.html',{'form':AuthenticationForm,'error':'username or passwors is incorrect'})
         else:
             login(request,user)
             return redirect('task')
         
@login_required
def create_task(request):
    if request.method =='GET':
       return render(request,'create_task.html',{'form':Taskfrom})
    else:
          try:
              form=Taskfrom(request.POST)
              new_task= form.save(commit=False)
              new_task.user=request.user
              new_task.save()
              return redirect(task)
          except ValueError:
                   return render(request,'create_task.html',{'form':Taskfrom,'ERROR':'DA UNOS DATOS QUE SEAN LEGIBLES'})
              
              
 
             
      
   