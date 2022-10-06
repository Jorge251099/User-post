# from django.shortcuts import render
# from django.views.generic import View

# from .models import Property
# from  django.http import JsonResponse


# class PostView(View):
#   
#   def get(self,request,*args,**kwargs):
#     context={

#         }
#     return render(request,'posts/post_home.html',context)

# def property_list(request):

#   property = Property.objects.all()

#   data = {
#     'property':list(property.values())
#   }

#   return JsonResponse(data) 

# def property_detail(request,pk):

#   property = Property.objects.get(pk=pk)
#   data = {
#     'direction':property.direction,
#     'country':property.country,
#     'description':property.description,
#     'thumbnail':property.thumbnail,
#     'active':property.active,
#   }

#   return JsonResponse(data)
