from typing import Any
from django.http import HttpRequest
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView, RedirectView, ListView, DetailView
from .models import Product, Image, Category , Comment , Like
from order.models import OrderItem
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
# Create your views here.


class Products(ListView):
    template_name = 'products/product.html'
    model = Product  # object Product.objects.filter(id=pk)
    context_object_name = 'products_all'
    paginate_by = 6

    def get_queryset(self):
        if self.request.user.is_authenticated :
            return [ (product.can_like(self.request.user),product) for product in Product.objects.filter(category__id=self.kwargs['pk']) ]
        else :
            return [ (False,product) for product in Product.objects.filter(category__id=self.kwargs['pk']) ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.ten_product_new()
        context["top_cells"] = OrderItem.top_cell_product()
        context["ten_discounts"] = Product.objects.ten_is_discount()
        if  Category.objects.filter(category__id=self.kwargs['pk']).exists():
            print('category true')
            context['category']=Category.objects.filter(category__id=self.kwargs['pk'])
        context['len']=len(self.get_queryset())
        # [ liked.can_like(self.request.user) for liked in self.get_queryset() ]
        # context['liked']=[ liked.can_like(self.request.user) for liked in self.get_queryset() ]
        return context


class DetailProduct(ListView):
    template_name = 'products/details.html'
    model = Product  # object Car.objects.filter(id=pk)
    slug_field = 'slug'
    context_object_name = 'product'
   
    # queryset=Product.objects.get(slug=slug_field)
    def get_queryset(self):
        return Product.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = Image.objects.filter(product=self.get_queryset())

        context["relateds"] = Product.objects.filter(category=self.get_queryset().category).exclude(
            id=self.get_queryset().id)
        comments=Comment.objects.select_related('product').filter(product=self.get_queryset(),is_reply=False)
        paginator=Paginator(comments,3)
        page_number=self.request.GET.get("page",1)
        page_objj=paginator.get_page(page_number)
        # context["comments"]=comments
        context["page_obj"]=page_objj
        if self.request.user.is_authenticated:
            context['liked']=True if self.get_queryset().can_like(self.request.user) else False
        else :
            context['liked']=False
        return context

        
class CommentAdd(View):

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.product=Product.objects.get(pk=kwargs['get_id'])
        return super().setup(request, *args, **kwargs)

    def post(self,request,get_id):
        if request.user.is_authenticated :
            if request.POST['body']  :
                comment=Comment(user=request.user,product=self.product,body=request.POST['body'])
                comment.save()
                messages.success(request,'comment add    ','success')
            else :
                messages.success(request,'your text is empty','danger')
        else :
            messages.success(request,'you are not login ','danger')
        return redirect('products:detail',self.product.slug)
    
class LikeAdd(View):

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.product=Product.objects.get(pk=kwargs['get_id'])
        self.like= Like.objects.deleted()
        return super().setup(request, *args, **kwargs)

    def get(self,request,get_id):
        if request.user.is_authenticated :
            
            if  self.product.can_like(request.user) and self.product.exist_like(request.user)  :
                like=Like.objects.get(product=self.product,user=request.user)
                like.undelete()
                messages.success(request,'Like Done  ','success')
                
            elif self.product.can_like(request.user) and not self.product.exist_like(request.user) :
                like=Like(user=request.user,product=self.product)
                like.save()
                messages.success(request,'Like Done  ','success')
                
            else :
                like=Like.objects.get(product=self.product,user=request.user)
                like.delete()
                # like.is_deleted=True
                # like.save()
                messages.success(request,' Unlike Done ','danger')
        else:
            messages.success(request,'You are not Login ','danger')
        return redirect('products:detail',self.product.slug)
    


class Search(ListView):
    template_name = 'products/product.html'
    context_object_name = 'products_all'
    paginate_by = 6

    def get_queryset(self):
        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            search_query = self.request.GET.get('search')
            search =  [ (product.can_like(self.request.user),product) for product in Product.objects.filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query))]
            return search
        else:
            return [ (product.can_like(self.request.user),product) for product in Product.objects.all() ]
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.ten_product_new()
        context["top_cells"] = OrderItem.top_cell_product()
        context["ten_discounts"] = Product.objects.ten_is_discount()
        context['len']=len(self.get_queryset())
        return context
