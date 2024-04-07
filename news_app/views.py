from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from hitcount.views import HitCountMixin
from hitcount.utils import get_hitcount_model

from .models import News, Category, Comment
from .forms import ContactForm, CommentForm
from news_project.custom_permissions import OnlyLoggedSuperUser

def news_list(request):
#   news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)

@login_required
def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    #hitcount_login
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        "comments": comments,
        'comment_count': comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    return render(request, 'news/news_detail.html', context)


# def homePageView(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by('-publish_time')[:9]
#     local_news = News.published.all().filter(category__name="Iphone").order_by('-publish_time')[0:6]
#     context = {
#         'news_list': news_list,
#         "categories": categories,
#         "local_news": local_news,
#     }
#
#     return render(request, 'news/home.html', context)

class homePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:9]
        context['local_news'] = News.published.all().filter(category__name="Iphone").order_by('-publish_time')[0:6]
        context['samsung_news'] = News.published.all().filter(category__name="Samsung")
        context['xiaomi_news'] = News.published.all().filter(category__name="Xiaomi")
        context['realmi_news'] = News.published.all().filter(category__name="Realmi")
        context['honor_news'] = News.published.all().filter(category__name="Honor")
        return context

# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur!")
#     context = {
#         "form": form
#     }
#     return render(request, 'news/contact.html', context)


class contactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur</h2>")
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)


def errorPageView(request):
    context = {

    }

    return render(request, 'news/404.html', context)


def categoryarchivePageView(request):
    context ={

    }

    return render(request, 'news/category-archive.html', context)


class IphoneNewsView(ListView):
    model = News
    template_name = 'news/iphone.html'
    context_object_name = 'iphone_news'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Iphone")
        return news


class XiaomiNewsView(ListView):
    model = News
    template_name = 'news/xiaomi.html'
    context_object_name = 'xiaomi_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Xiaomi")
        return news


class RealmiNewsView(ListView):
    model = News
    template_name = 'news/realmi.html'
    context_object_name = 'realmi_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Realmi")
        return news


class HonorNewsView(ListView):
    model = News
    template_name = 'news/honor.html'
    context_object_name = 'honor_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Honor")
        return news


class SamsungNewsView(ListView):
    model = News
    template_name = 'news/samsung.html'
    context_object_name = 'samsung_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Samsung")
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status', )
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )