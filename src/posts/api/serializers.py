from rest_framework import serializers
from posts.models import Propertys , Business , Comment


class CommentSerializer(serializers.ModelSerializer):

  comment_user = serializers.StringRelatedField(read_only=True)
  class Meta:
    model = Comment
    exclude = ['propertys',]
    #fields = '__all__'

class PropertysSerializer(serializers.ModelSerializer):

  #len_direction = serializers.SerializerMethodField()
  comments = CommentSerializer(many=True,read_only=True)
  property_name = serializers.CharField(source='business.name')

  class Meta:
    model = Propertys
    fields = '__all__'
    #fields = ['id','country','active','thumbnail']
    #exclude = ['id']


class BusinessSerializer(serializers.ModelSerializer): #serializers.HyperlinkedModelSerializer
  
  edificationslist = PropertysSerializer(many=True,read_only=True)
  #edificationslist = serializers.StringRelatedField(many=True)
  #edificationslist = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
 # edificationslist = serializers.HyperlinkedRelatedField(
 #     many=True,
 #     read_only=True,
 #     view_name='property-detail',
 #     )

  class Meta:
    model = Business
    fields = '__all__'


# def get_len_direction(self,object):
#   number_characters = len(object.direction)
#   return number_characters

# def validate(self,data):
#   if data['direction'] == data['country']:
#     raise serializers.ValidationError('The direction and country are the same')
#   else:
#     return data

# def validate_thumbnail(self,data):
#   if len(data) < 2:
#     raise serializers.ValidationError('The thumbnail is small slouch')
#   else:
#     return data

# def column_longitud(value):
#   if len(value)<2:
#     raise serializers.ValidationError("Tu pene es demasiado corta")

# class PropertysSerializer(serializers.Serializer):

#   id = serializers.IntegerField(read_only=True)
#   direction = serializers.CharField(validators=[column_longitud])
#   country = serializers.CharField(validators=[column_longitud])
#   description = serializers.CharField()
#   thumbnail =serializers.CharField()
#   active = serializers.BooleanField()

#   def create(self,validate_data):
#     return Propertys.objects.create(**validate_data)

#   def update(self,instance,validate_data):
#     instance.direction = validate_data.get('direction',instance.direction)
#     instance.country = validate_data.get('country',instance.country)
#     instance.description = validate_data.get('description',instance.description)
#     instance.thumbnail = validate_data.get('thumbnail',instance.thumbnail)
#     instance.active = validate_data.get('active',instance.active)
#     instance.save()
#     return instance

#   def validate(self,data):
#     if data['direction']==data['country']:
#       raise serializers.ValidationError('La direccion y el pais deben ser diferentes')
#     else:
#       return data

#   def validate_thumbnail(self,data):
#     if len(data) < 2:
#       raise serializers.ValidationError('La URL de la imagen es muy corta')
#     else:
#       return data
