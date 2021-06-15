from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DashBoardView, FBPageView, FBPageCreateView, AdView,AdUpdateView, AdSoretedByDateView, AdSoretedByFBPageView, AdFavoriteListView, AdMemoView, LPListView, FBPageDetailView, FBPageUpdateView

app_name = 'scraping'

urlpatterns = [
    path('', DashBoardView.as_view(), name='dashboard'),
    path('fbpage/', FBPageView.as_view(), name='fbpage'),
    path('fbpage/create/', FBPageCreateView.as_view(), name='fbpage_create'),
    path('fbpage/update/<int:pk>', FBPageUpdateView.as_view(), name='fbpage_update'),
    path('fbpage/detail/<int:pk>', FBPageDetailView.as_view(), name='fbpage_detail'),
    path('ad/', AdView.as_view(), name='ad'),
    path('ad/<int:pk>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('ad/sorted_by_date/', AdSoretedByDateView.as_view(), name='ad_sorted_by_date'),
    path('ad/sorted_by_fbpage/', AdSoretedByFBPageView.as_view(), name='ad_sorted_by_fbpage'),
    path('ad/favorite_list/', AdFavoriteListView.as_view(), name='ad_favorite_list'),
    path('ad/memo/', AdMemoView.as_view(), name='ad_memo'),
    path('lp/list/', LPListView.as_view(), name='lp_list'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
