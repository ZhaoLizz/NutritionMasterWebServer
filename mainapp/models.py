from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Occupation(models.Model):
    """
    特殊职业
    """
    occupation_name = models.CharField(max_length=16, unique=True, primary_key=True)

    def __str__(self):
        return self.occupation_name


class FoodMaterial(models.Model):
    """
    食材
    """
    material_name = models.CharField(max_length=64, primary_key=True)
    # material_effect = models.ManyToManyField(Physique, through='MaterialEffect')  # 食材_效果_体质

    def __str__(self):
        return self.material_name


class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=128, primary_key=True)
    # physical_name = models.ForeignKey(Physique, on_delete=models.CASCADE, blank=True, null=True)
    calorie = models.IntegerField(default=-1)
    minutes = models.IntegerField(default=0)
    flavor = models.CharField(max_length=64)
    technology = models.CharField(max_length=16)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    practice = models.TextField(default='')
    cook_quantity = models.ManyToManyField(FoodMaterial, through='CookQuantity')  # 菜谱_做菜用量_食材

    def __str__(self):
        return self.name


class MenuClassification(models.Model):
    """
    菜谱的功能分类
    """
    classification = models.CharField(max_length=16, primary_key=True)  # 分类名称
    cure_occupation = models.ManyToManyField(Occupation, blank=True, null=True)  # 菜谱功能分类_可治愈的职业_特殊职业
    menu_effect = models.ManyToManyField(Menu)

    def __str__(self):
        return self.classification


class Physique(models.Model):
    """
    体质
    """
    physical_name = models.CharField(max_length=64, primary_key=True)
    # physical_feature = models.TextField(null=True)
    # exercise_method = models.TextField(null=True)
    cure_material = models.ManyToManyField(FoodMaterial, blank=True, null=True)

    def __str__(self):
        return self.physical_name


#
# class MaterialEffect(models.Model):
#     """
#     食材效果
#     """
#     food_material = models.ForeignKey(FoodMaterial, on_delete=models.CASCADE)
#     physique = models.ForeignKey(Physique, on_delete=models.CASCADE)
#     material_effect = models.IntegerField()
#
#     def __str__(self):
#         return self.food_material.material_name + " " + str(self.material_effect) + " " + self.physique.physical_name


class CookQuantity(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    material = models.ForeignKey(FoodMaterial, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=64, default='')

    def __str__(self):
        return self.menu.name + " -- " + self.material.material_name + " -- " + str(self.quantity)

    class Meta:
        unique_together = ('menu', 'material')


#
# class PhysicalProperty(models.Model):
#     """
#     体质性状
#     """
#     property_name = models.CharField(max_length=64, primary_key=True)
#     physical_state = models.ManyToManyField(Physique)
#
#     def __str__(self):
#         return self.property_name


class MyUser(AbstractUser):
    physical_name = models.ForeignKey(Physique, on_delete=models.CASCADE, blank=True, null=True)
    occupation_name = models.ForeignKey(Occupation, on_delete=models.CASCADE, blank=True, null=True)
    sex = models.IntegerField(default=1)

    def __str__(self):
        return self.username


class UploadFile(models.Model):
    file = models.FileField(upload_to='mainapp/media')

    def __str__(self):
        return self.file
