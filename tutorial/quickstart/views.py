from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from tutorial.quickstart.serializers import GroupSerializer, UserSerializer
from .models import Product
from .serializers import ProductSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset?
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    """
    Viewset specify cho admin 
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny] #set tạm allow any
    # permission_classes = [IsAdminUser]



# decorator tạo endpoint cho function views based hoặc không phải class-based viewset
@api_view()
def hello_world(request):
    return Response({"message": "hello, world"})

# @api_view(['GET'])
# @renderer_classes([TemplateHTMLRenderer])
# def testing_templaterenderer(request):
#     template = loader.get_template('test/testing.html')
#     return HttpResponse(template.render())
#     # return render(request, 'test/testing.html')

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]