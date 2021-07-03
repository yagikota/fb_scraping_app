from typing import Counter
from django.db import models
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Advertisement, Page
from django.urls import reverse_lazy
from django.views.generic.list import MultipleObjectMixin
from collections import Counter
# Create your views here.

class DashBoardView(TemplateView):
    template_name = "dashboard.html"

class FBPageView(ListView):
    template_name = "fbpage.html"
    paginate_by = 10
    page_num = Page.objects.values('page_id').annotate(latest=models.Min('scraped_at')).count()
    queryset = Page.objects.all()[::-1][:page_num]

class FBPageCreateView(CreateView):
    template_name = "fbpage_create.html"
    model = Page
    fields = ('page_id',)
    success_url = reverse_lazy('scraping:dashboard')

class FBPageUpdateView(UpdateView):
    template_name = "fbpage_update.html"
    model = Page
    fields = ('is_notable',)
    success_url = reverse_lazy('scraping:dashboard')

class FBPageDetailView(DetailView, MultipleObjectMixin):
    template_name = "fbpage_detail.html"
    model = Page
    paginate_by = 9

    def get_context_data(self, **kwargs):
        object_list = Advertisement.objects.filter(parent=self.object)
        context = super(FBPageDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context

class FBPageDeleteView(DeleteView):
    template_name = "fbpage_delete.html"
    model = Page

class AdView(ListView):
    template_name = "ad.html"
    model = Advertisement
    context_object_name = 'advertisements'
    paginate_by = 9

class AdUpdateView(UpdateView):
    template_name = "ad_update.html"
    model = Advertisement
    fields = ('memo', 'is_favorite')
    success_url = reverse_lazy('scraping:dashboard')


class AdSoretedByDateView(ListView):
    template_name = "ad_sorted_by_date.html"
    model = Page
    context_object_name = 'pages'
    queryset = Page.objects.order_by('-scraped_at')
    paginate_by = 12

class AdSoretedByFBPageView(ListView):
    template_name = "ad_sorted_by_fbpage.html"
    model = Page
    context_object_name = 'pages'
    queryset = Page.objects.order_by('page_id')
    paginate_by = 12

class LPListView(TemplateView):
    template_name = "lp_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lp_urls = []
        for ad in Advertisement.objects.all():
            lp_urls.append(ad.lp_url)
        count = Counter(lp_urls)
        count_lp_url = []
        for key, val in count.items():
            count_lp_url.append([key,val])
        context['count_lp_url'] = count_lp_url
        return context

class AdMemoView(ListView):
    template_name = "ad_memo.html"
    model = Advertisement
    context_object_name = 'advertisements'
    paginate_by = 12

class AdFavoriteListView(ListView):
    template_name = "ad_favorite_list.html"
    model = Advertisement
    context_object_name = 'advertisements'
    paginate_by = 12
