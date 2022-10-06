from django.views.generic import View
from django.shortcuts import redirect,render

class homeView(View):

  def get(self,request,*args,**kwargs):
    context={

        }
    return render(request,'home_view.html',context)
