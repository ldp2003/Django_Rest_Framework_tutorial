from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, renderer_classes, action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination

from tutorial.quickstart.serializers import GroupSerializer, UserSerializer
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

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

class CategoryViewSet(viewsets.ViewSet):
    """
    Category viewset
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        if category is not None:
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        if category is not None:
            serializer = self.serializer_class(category, data=request.data) # self.serializer_class == CategorySerializer
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

class ProductPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'size' #custom params truyền vào để request số lượng trên 1 trang
    max_page_size = 10 #giới hạn số lượng trên 1 trang 

class ProductViewSet(viewsets.ModelViewSet):
    """
    Viewset specify cho admin 
    """
    queryset = Product.objects.all().order_by('-created_at') #Có paging thì nên ordering 
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.AllowAny] #set tạm allow any
    # permission_classes = [IsAdminUser]

    #demo extra action
    @action(detail=True, methods=['put'], permission_classes=[permissions.AllowAny]) # để tạm allow any do chưa biết test với login trong postman
    def update_price(self, request, pk=None):
        product = self.get_object()

        #update bằng serializer tự động validate
        serializer = ProductSerializer(
            product,
            data={'price' : request.data.get('price')},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Price updated successfully',
                'product': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        #Không dùng serializer tự động validate
        # new_price = request.data.get('price')
        # product.price = new_price
        # product.save()
        # # return Response({product}) #Sai
        # # return Response({'message': 'Price updated successfully','new_price': product.price,'product_id': product.id}) 
        # #Cách 2
        # serializer = ProductSerializer(product)
        # return Response({'message': 'Price updated successfully','product': serializer.data})

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