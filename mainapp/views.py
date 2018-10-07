from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mainapp.serializers import *


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

        # random  0-10的数，0-4病  5-7体质  8-10职业
        # username = request.GET['username']
        # user = MyUser.objects.get(username=username)




    @action(detail=False, methods=['post', 'get'])
    def get_menus_by_elements(self, request):
        """
        返回营养元素为0-elements 范围的菜谱
        暂时仅仅用到calorie,fat,protein,
        :param request:
        :return:
        """
        import time
        localtime = time.localtime()
        week = int(time.strftime("%w", localtime))
        # 返回每天的营养元素允许量(本周剩下的量 / 本周剩余的天数)
        week_denominator = (7 - week + 1) if week != 0 else 1  # week = 0是周日,周日就不用处理了,直接分母为1

        # 通过传入的参数构造sql查询字符串
        post = request.POST
        menus = None
        sql = 'SELECT "mainapp_menu"."name", "mainapp_menu"."calorie", "mainapp_menu"."minutes", "mainapp_menu"."flavor", "mainapp_menu"."technology", "mainapp_menu"."image_url", "mainapp_menu"."practice", "mainapp_menu"."elements_id" FROM "mainapp_menu" INNER JOIN "mainapp_element" ON ("mainapp_menu"."elements_id" = "mainapp_element"."id") WHERE '
        query_sql = ''
        for k, v in post.items():
            if (k == 'calorie'):
                query_sql += ' AND "mainapp_menu"."calorie" <= ' + str(
                    float(v) / week_denominator) + ' AND "mainapp_menu"."calorie" > 0'
            else:
                query_sql += ' AND "mainapp_element"."' + k + '" <= ' + str(
                    float(v) / week_denominator) + ' AND "mainapp_element"."' + k + '" > 0'
        query_sql = sql + '( ' + query_sql[5:] + ' )'
        menus = Menu.objects.raw(query_sql)
        print('log sql', query_sql)
        print('log count', len(list(menus)))
        serializer = MenuSerializerLighter(menus, many=True)  # MenuSerializer 耦合了CookQuantity,可能造成查询比较慢.上线后试一试效果
        return Response(serializer.data)
        # return HttpResponse(query_sql)

        # calorie = post.get('calorie')
        # carbohydrate = post.get('carbohydrate')
        # fat = post.get('fat')
        # protein = post.get('protein')
        # cellulose = post.get('cellulose')
        # vitaminA = post.get('vitaminA')
        # vitaminB1 = post.get('vitaminB1')
        # vitaminB2 = post.get('vitaminB2')
        # vitaminB6 = post.get('vitaminB6')
        # vitaminC = post.get('vitaminC')
        # vitaminE = post.get('vitaminE')
        # carotene = post.get('carotene')
        # cholesterol = post.get('cholesterol')
        # Mg = post.get('Mg')
        # Ca = post.get('Ca')
        # Fe = post.get('Fe')  # x
        # Zn = post.get('Zn')
        # Cu = post.get('Cu')  # x
        # Mn = post.get('Mn')  # x
        # K = post.get('K')
        # P = post.get('P')
        # Na = post.get('Na')
        # Se = post.get('Se')
        # niacin = post.get('niacin')  # B3
        # thiamine = post.get('thiamine')  # B1


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

        吃了一个菜,就传入摄入的elements,然后+= 存到user的elements里面
        :param request: 带有一个elements参数,一个username参数
        """
        username = request.POST['username']
        user = MyUser.objects.get(username=username)  # user对象
        # 根据user对象找到user对应的elements
        user_element = user.eaten_elements if user.eaten_elements != None else Element()

        # 根据POST传入的元素kv,创建一个Element对象
        eaten_elements = Element()
        for k, v in request.POST.items():
            if (k != 'username'):
                setattr(eaten_elements, k, float(v))
                print('log eaten_elements', getattr(eaten_elements, k))
        # print('log',user_element)
        # print('log',eaten_elements)

        user_element += eaten_elements
        user_element.save()
        user.eaten_elements = user_element
        user.save()

        return Response(MyUserSerializer(user).data)

        # menu_name = request.POST['menu_name']
        # menu_list = Menu.objects.filter(name=menu_name)
        # if (menu_list.count() > 0):
        #     # 首先获取到menu存在的elements信息
        #     menu = menu_list[0]
        #     menu_elements = menu.elements
        #     # 然后获取user的elements
        #     username = request.POST['username']
        #     user = MyUser.objects.get(username=username)
        #     user_element = user.eaten_elements if user.eaten_elements != None else Element()
        #
        #     # 加值,保存
        #     user_element += menu_elements
        #     # 把由material计算得到的卡路里换成直接爬到的卡路里
        #     user_element.calorie = user_element.calorie - menu_elements.calorie + menu.calorie
        #
        #     print('log', 'after add ', user_element.calorie)
        #
        #     user_element.save()
        #     user.eaten_elements = user_element
        #     user.save()
        #     return Response(MyUserSerializer(user).data)
        # else:
        #     return Http404('not found this menu : ' + menu_name)
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


class TrickViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trick.objects.all()
    serializer_class = TrickSerializer

    @action(detail=False, methods=['get'])
    def get_random_tricks(self, request):
        import random
        import numpy as np
        size = self.queryset.count()
        count = request.GET['count']
        count = int(count)
        # sample : 从一个list中随机挑选n个数组成list
        random_index = random.sample(range(size), count)
        random_tricks = np.array(self.queryset)[random_index]
        serializer = TrickSerializer(random_tricks, many=True)
        return Response(serializer.data)

# [calorie,carbohydrate,fat ,protein,cellulose,vitaminA,vitaminB1,vitaminB2,vitaminB6,vitaminC,vitaminE,carotene,cholesterol,Mg,Ca,Fe,Zn,Cu,Mn,K ,P ,Na,Se,niacin ,thiamine]
