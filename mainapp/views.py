from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, mixins, generics, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from mainapp.forms import UploadFileForm
from mainapp.models import Menu, CookQuantity, FoodMaterial, MyUser, MenuClassification, Occupation, Physique, Illness, \
    Element
from mainapp.serializers import MenuSerializer, CookQuantitySerializer, MyUserSerializer, MenuClassificationSerializer, \
    OccupationSerializer, PhysiqueSerializer, FoodMaterialSerializer, IllnessSerializer


#
# class MenuList(APIView)
#     def get(self,request,format=None):
#         menu = Menu.objects.all()
#         serializer = MenuSerializer(menu, many=True)
#         return Response(serializer.data)
#
#     def post(self,request,format=None):
#         print('log',request.data)
#         return Response(request.data)
#
#
# class MenuList(generics.ListAPIView):
#     queryset = Menu.objects.all()
#     serializer_class = MenuSerializer
#
#     def get(self, request, *args, **kwargs):
#         """
#         list函数自动返回字段queryset的serializer对象
#         """
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         print('log', request.data)
#         return Response(request.data)
#
#
# class MenuDetail(generics.RetrieveAPIView):
#     queryset = Menu.objects.all()
#     serializer_class = MenuSerializer
#     lookup_field = 'name'
#
#     def get(self, request, *args, **kwargs):
#         # menu = Menu.objects.get(name=self.kwargs['name'])
#         serializer = MenuSerializer(context={'request': request})
#         return Response(serializer.data)


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    """
    传入的pk值为菜名,查询菜的信息和做菜方法
    ReadOnlyViewSet提供list和detail
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @action(detail=False, methods=['get'])
    def get_random_menus(self, request):
        import random
        import numpy as np
        size = self.queryset.count()
        count = request.GET['count']
        count = int(count)
        # sample : 从一个list中随机挑选n个数组成list
        random_index = random.sample(range(size), count)
        random_menus = np.array(self.queryset)[random_index]
        serializer = MenuSerializer(random_menus, many=True)
        return Response(serializer.data)


# class CookQuantityDetail(APIView):
#     def get(self, request, name):
#         menu = Menu.objects.get(name=name)
#         cook_quantities = CookQuantity.objects.filter(menu=menu)
#         serializer = CookQuantitySerializer(cook_quantities, many=True)
#         return Response(serializer.data)

# class CookQuantityDetail(generics.ListAPIView):
#     serializer_class = CookQuantitySerializer
#     lookup_field = 'name'  # 在url中寻找的参数,可以通过self.kwargs['name']获取
#
#     def get_queryset(self):
#         name = self.kwargs['name']
#         menu = Menu.objects.get(name=name)
#         return CookQuantity.objects.filter(menu=menu)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


class CookQuantityViewSet(viewsets.ReadOnlyModelViewSet):
    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        查询菜谱具体需要的食材和数量(暂时不需要了,直接集成到了MenuViewSet里面,让MenuSerializer本身就包含食材信息)
        :param pk:
        """
        print('log', pk)
        menu = Menu.objects.get(name=pk)
        cook_quantities = CookQuantity.objects.filter(menu=menu)
        serializer = CookQuantitySerializer(cook_quantities, many=True)
        return Response(serializer.data)


class FoodMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FoodMaterial.objects.all()
    serializer_class = FoodMaterialSerializer

    # def retrieve(self, request, pk=None, *args, **kwargs):
    #     """
    #     查询食材可以做的菜
    #     :param pk: 食材名
    #     """
    #     food_material = FoodMaterial.objects.get(material_name=pk)
    #     cook_quantities = CookQuantity.objects.filter(material=food_material)
    #     serializer = CookQuantitySerializer(cook_quantities, many=True)
    #     return Response(serializer.data)


class MyUserViewSet(viewsets.ModelViewSet):
    """
    update PUT http://127.0.0.1:8000/myuser/test/  body传入更新后的数据
    retrieve GET http://127.0.0.1:8000/myuser/test1/
    create POST http://127.0.0.1:8000/myuser/  body传入创建的数据
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    lookup_field = 'username'

    @action(detail=False, methods=['post'])
    def eaten_menu(self, request):
        """
        吃了一个菜,就传过来这个菜名,然后动态改变用户已吃的营养元素的量
        :param request: 带有一个menu_name参数,一个username参数
        """
        menu_name = request.POST['menu_name']

        menu_list = Menu.objects.filter(name=menu_name)
        if (menu_list.count() > 0):
            # 首先获取到menu存在的elements信息
            menu = menu_list[0]
            menu_elements = menu.elements
            # 然后获取user的elements
            username = request.POST['username']
            user = MyUser.objects.get(username=username)
            user_element = user.eaten_elements if user.eaten_elements != None else Element()

            print('log','userelement',user_element.calorie)
            print('log','menuelement',menu_elements.calorie)


            # 加值,保存
            user_element += menu_elements
            # 把由material计算得到的卡路里换成直接爬到的卡路里
            user_element.calorie = user_element.calorie - menu_elements.calorie + menu.calorie

            print('log','after add ',user_element.calorie)

            user_element.save()
            user.eaten_elements = user_element
            user.save()
            return Response(MyUserSerializer(user).data)
        else:
            return Http404('not found this menu : ' + menu_name)
        # return HttpResponse('test')


class MenuClassificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MenuClassification.objects.all()
    serializer_class = MenuClassificationSerializer
    lookup_field = 'classification'


class OccupationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer
    lookup_field = 'occupation_name'


class PhysiqueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Physique.objects.all()
    serializer_class = PhysiqueSerializer
    lookup_field = 'physical_name'


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        # form = UploadFileForm(data=request.POST, files=request.FILES)
        # if form.is_valid():
        #     form.save()
        #     return HttpResponse('save file ')
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        return HttpResponse(uploaded_file_url)

    return HttpResponse('test')


class IllnessViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Illness.objects.all()
    serializer_class = IllnessSerializer
    lookup_field = 'menu_classification'
