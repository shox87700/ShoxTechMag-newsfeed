from django.urls import path
from .views import news_list, news_detail, homePageView, contactPageView, errorPageView, categoryarchivePageView, \
    IphoneNewsView, SamsungNewsView, RealmiNewsView, HonorNewsView, XiaomiNewsView, NewsDeleteView, NewsUpdateView, \
    NewsCreateView, admin_page_view, SearchResultsList, popular_news, most_read_news, recent_comments, \
    most_commented_news

urlpatterns = [
    path('', homePageView.as_view(), name="home_page"),
    path('news/', news_list, name="all_news_list"),
    path('news/create/', NewsCreateView.as_view(), name="news_create"),
    path('news/<slug:news>/', news_detail, name="news_detail_page"),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name="news_update"),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name="news_delete"),
    path('contact-us/', contactPageView.as_view(), name="contact_page"),
    path('404-error/', errorPageView, name="404_page"),
    path('category-archive/', categoryarchivePageView, name="category-archive"),
    path('iphone-news/', IphoneNewsView.as_view(), name="iphone_news_page"),
    path('samsung-news/', SamsungNewsView.as_view(), name="samsung_news_page"),
    path('realmi-news/', RealmiNewsView.as_view(), name="realmi_news_page"),
    path('honor-news/', HonorNewsView.as_view(), name="honor_news_page"),
    path('xiaomi-news/', XiaomiNewsView.as_view(), name="xiaomi_news_page"),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresult/', SearchResultsList.as_view(), name="search_results"),
    path('popular/', popular_news, name='popular_news'),
    path('most-read/', most_read_news, name='most_read_news'),
    path('recent-comments/', recent_comments, name='recent_comments'),
    path('most-commented/', most_commented_news, name='most_commented_news'),

]