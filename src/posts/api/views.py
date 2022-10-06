from rest_framework.response import Response
from posts.models import Propertys , Business , Comment
from .serializers import PropertysSerializer , BusinessSerializer , CommentSerializer
#from rest_framework.decorators import api_view
from django.views.generic import View
from django.shortcuts import render , get_object_or_404
from rest_framework import status , generics , mixins , viewsets

from rest_framework.views import APIView

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly , IsCommentUserOrReadOnly

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle

from .throttling import CommentCreateThrottle, CommentListThrottle

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .pagination import PropertysPagination,PropertysLOPagination



class UserComment(generics.ListAPIView):

  serializer_class = CommentSerializer

  #def get_queryset(self):
    #username = self.kwargs['username']
    #return Comment.objects.filter(comment_user__username=username)

  def get_queryset(self):
    username = self.request.query_params.get('username',None)
    return Comment.objects.filter(comment_user__username=username)


class CommentCreate(generics.CreateAPIView):

  serializer_class = CommentSerializer
  permission_classes = [IsAuthenticated]
  throttle_classes = [CommentCreateThrottle]

  def get_queryset(self):
    return Comment.objects.all()

  def perform_create(self,serializer):
    pk = self.kwargs.get('pk')
    property = Propertys.objects.get(pk=pk)

    user = self.request.user
    comment_queryset = Comment.objects.filter(propertys=property,comment_user=user)

    if comment_queryset.exists():
      raise ValidationError('El usuario ya escribio un comentario para este inmueble')

    if property.number_calification == 0:
      property.avg_calification = serializer.validated_data['calification']
    else:
      property.avg_calification = (serializer.validated_data['calification'] +
                                    property.avg_calification)/2

    property.number_calification = property.number_calification +1
    property.save()

    serializer.save(propertys=property , comment_user=user)


class CommentList(generics.ListCreateAPIView):

  #queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  #permission_classes = [IsAuthenticated]
  #permission_classes = [AdminOrReadOnly]
  throttle_classes = [CommentListThrottle, AnonRateThrottle]
  filter_backends = [DjangoFilterBackend]
  #indicar las columnas que deseo filtrar
  filterset_fields = ['comment_user__username','active']
  
  def get_queryset(self):
    pk = self.kwargs['pk']
    return Comment.objects.filter(propertys=pk)
    

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):

  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  permission_classes = [IsCommentUserOrReadOnly]

  #throttle_classes = [UserRateThrottle, AnonRateThrottle]
  throttle_scope = 'comment-detail'




# class CommentList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):

# queryset = Comment.objects.all()
# serializer_class = CommentSerializer

# def get(self,request,*args,**kwargs):
#   return self.list(request,*args,**kwargs)

# def post(self,request,*args,**kwargs):
#   return self.create(request,*args,**kwargs)

# class CommentDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):

# queryset = Comment.objects.all()
# serializer_class = CommentSerializer

# def get(self,request,*args,**kwargs):
#   return self.retrieve(request,*args,**kwargs)



# class BusinessVS(viewsets.ModelViewSet):

#   permission_classes = [AdminOrReadOnly]
#   queryset = Business.objects.all()
#   serializer_class = BusinessSerializer

class BusinessVS(viewsets.ViewSet):

  permission_classes = [IsAdminOrReadOnly]
  #permission_classes = [IsAuthenticated] 

  def list(self,request):
    queryset = Business.objects.all()
    serializer = BusinessSerializer(queryset,many=True)
    return Response(serializer.data)

  def retrieve(self,request,pk=None):
    queryset = Business.objects.all()
    edificationslist = get_object_or_404(queryset , pk=pk)
    serializer = BusinessSerializer(edificationslist)
    return Response(serializer.data)

  def create(self,request):
    serializer = BusinessSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)

    else:
      Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

  def update(self,request,pk):
    try:
      business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
      return Response({'Error':'Business not found'},status=status.HTTP_404_NOT_FOUND)

    serializer = BusinessSerializer(business,data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)

    else:
      return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)

  def destroy(self,request,pk):
    try:
      business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
      return Response({'Error':'Business not found'},status=status.HTTP_404_NOT_FOUND)

    business.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


#ESTA PARTE YA NO SE USA
class BusinessAV(APIView):

  def get(self,request):
    business = Business.objects.all()
    #ESTA PARTE LA PONEMOS PARA PODER PONER EL LINK EN SERIALIZER 
    serializer = BusinessSerializer(business,many=True,context={'request':request})
    return Response(serializer.data)

  def post(self,request):
    serializer = BusinessSerializer(data=data.request)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BusinessDetailAV(APIView):

  def get(self,request,pk):
    try:
      business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
      return Response({'Error':'Business not found'},status=status.HTTP_404_NOT_FOUND)

    serializer = BusinessSerializer(business,context={'request':request})
    return Response(serializer.data)

  def put(self,request,pk):
    try:
      business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
      return Response({'Error':'Business not found'},status=status.HTTP_404_NOT_FOUND)

    serializer = BusinessSerializer(business,context={request:request})

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

  def delete(self,request,pk):
    try:
      business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
      return Response({'Error':'Business not found'},status=status.HTTP_404_NOT_FOUND)

    business.delete()
    return Response({'Exito':'Business delete'},status=status.HTTP_204_NO_CONTENT)



class PropertysList(generics.ListAPIView):

  queryset = Propertys.objects.all()
  serializer_class = PropertysSerializer
  #filter_backends = [DjangoFilterBackend]
  #filterset_fields = ['direction','business__name']
  filter_backends = [filters.SearchFilter, filters.OrderingFilter]
  search_fields = ['direction','business__name']
  pagination_class = PropertysLOPagination #PropertysPagination


class PropertysListAV(APIView):

  permissions_classes = [IsAdminOrReadOnly]

  def get(self,request):
    propertys = Propertys.objects.all()
    serializer = PropertysSerializer(propertys,many=True)
    return Response(serializer.data)

  def post(self,request):
    serializer = PropertysSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PropertysDetailAV(APIView):

  permissions_classes = [IsAdminOrReadOnly]

  def get(self,request,pk):
    try:
      propertys = Propertys.objects.get(pk=pk)
    except Propertys.DoesNotExist:
      return Response({'error':'Property not found'},status=status.HTTP_404_NOT_FOUND)

    serializer = PropertysSerializer(propertys)
    return Response(serializer.data)

  def put(self,request,pk):
    try:
      propertys = Propertys.objects.get(pk=pk)
    except Propertys.DoesNotExist:
      return Response({'error':'Property not found'},status=status.HTTP_404_NOT_FOUND)

    serializer = PropertysSerializer(propertys,data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

  def delete(self,request,pk):
    try:
      propertys = Propertys.objects.get(pk=pk)
    except Propertys.DoesNotExist:
      return Response({'error':'Property not found'},status=status.HTTP_404_NOT_FOUND)
    
    propertys.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

       
    







# @api_view(['GET','POST'])
# def property_list(request):

# if request.method == 'GET':
#   propertys = Propertys.objects.all()
#   serializer = PropertysSerializer(propertys,many=True)
#   return Response(serializer.data)

# if request.method == 'POST':
#   de_serializer = PropertysSerializer(data=request.data)

#   if de_serializer.is_valid():
#     de_serializer.save()
#     return Response(de_serializer.data)

#   else:
#     return Response(de_serializer.errors)

# @api_view(['GET','PUT','DELETE'])
# def property_detail(request,pk):

# if request.method == 'GET':
#   try:
#     propertys = Propertys.objects.get(pk=pk)
#     serializer = PropertysSerializer(propertys)

#     return Response(serializer.data)
#   except Propertys.DoesNotExist:
#     return Response({'Error':'El inmueble no existe'},status=status.HTTP_404_NOT_FOUND)

# if request.method == 'PUT':
#   propertys =Propertys.objects.get(pk=pk)
#   de_serializer = PropertysSerializer(propertys,data=request.data)

#   if de_serializer.is_valid():
#     de_serializer.save()
#     return Response(de_serializer.data)

#   else:
#     return Response(de_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# if request.method == 'DELETE':
#   try:
#     propertys = Propertys.objects.get(pk=pk)
#     propertys.delete()
#   except Propertys.DoesNotExist:
#     return Response({'Erorr':'El inmueble no existe'},status=status.HTTP_404_NOT_FOUND)

#   return Response(status=status.HTTP_204_NO_CONTENT)
