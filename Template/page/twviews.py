from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, InvalidPage
from page.models import Category, Good
from django.http import HttpResponse, Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ProcessFormView
from django.core.urlresolvers import reverse
from django.views.generic.base import ContextMixin

class GoodListView(ListView):
    template_name = "index.html"
    paginate_by = 2
    cat = None

    def get(self, request, *args, **kwargs):
        if self.kwargs["cat_id"] == None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk = self.kwargs["cat_id"])
        return super(GoodListView,self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodListView,self).get_context_data(**kwargs)
        context["cats"] = Category.objects.order_by("name")
        context["category"] = self.cat
        return context

    def get_queryset(self):
        return Good.objects.filter(category = self.cat).order_by("name")

class CategoryListMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(CategoryListMixin, self).get_context_data(**kwargs)
        context["cats"] = Category.objects.order_by("name")
        return context




class GoodDetailView(DetailView):
    template_name = "good.html"
    model = Good
    pk_url_kwarg = "good_id"

    def get_context_data(self, **kwargs):
        context = super(GoodDetailView,self).get_context_data(**kwargs)
        try:
            context["pn"] = self.request.GET["page"]
        except KeyError:
            context["pn"] = "1"
        context["cats"] = Category.objects.order_by("name")
        return context

class GoodEditMixin(CategoryListMixin):
    def get_context_data(self, **kwargs):
        context = super(GoodEditMixin, self).get_context_data(**kwargs)
        try:
            context["pn"]= self.request.GET["page"]
        except KeyError:
            context["pn"]= "1"
        return context

class GoodEditView(ProcessFormView):
    def post(self, request, *args, **kwargs):
        try:
            pn = request.GET["page"]
        except KeyError:
            pn = "1"
        self.success_url = self.success_url + "?page="+pn
        return super(GoodEditView, self).post(request, *args, **kwargs)

class GoodCreate(CreateView, GoodEditMixin):
    model = Good
    template_name = "good_add.html"
    def get(self, request, *args, **kwargs):
        if self.kwargs["cat_id"] != None:
            self.initial["category"]=Category.objects.get(pk = self.kwargs["cat_id"])
        return super(GoodCreate, self).get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.success_url = reverse("index" , kwargs={"cat_id": Category.objects.get(pk = self.kwargs["cat_id"]).id})
        return super(GoodCreate, self).post(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(GoodCreate, self).get_context_data(**kwargs)
        context["category"]= Category.objects.get(pk = self.kwargs["cat_id"])
        return context

class GoodUpdate(UpdateView, GoodEditMixin, GoodEditView):
    model = Good
    template_name = "good_edit.html"
    pk_url_kwarg = "good_id"
    def post(self, request, *args, **kwargs):
        self.success_url = reverse("index", kwargs = {"cat_id": Good.objects.get(pk=kwargs["good_id"]).category.id})
        return super(GoodUpdate, self).post(request, *args, **kwargs)

class GoodDelete(DeleteView, GoodEditMixin, GoodEditView):
    model = Good
    template_name = "good_delete.html"
    pk_url_kwarg = "good_id"
    def post(self, request, *args, **kwargs):
        self.success_url = reverse("index", kwargs = {"cat_id": Good.objects.get(pk = kwargs["good_id"].category.id)})
        return super(GoodDelete, self).post(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(GoodDelete, self).get_context_data(**kwargs)
        context["good"]= Good.objects.get(pk = kwargs["good_id"])
        return context



