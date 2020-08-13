from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django import views
from django.urls import reverse
from django.views import generic
from unidecode import unidecode
from .models import ModelMV

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Get_mv


class home(views.View):
    def get(self, request):
        lst_v_pop = ModelMV.objects.filter(category_MV='V-Pop').order_by('-time_Post')
        lst_v_pop = lst_v_pop[0:6]  # Lấy 6 mv đầu tiên

        lst_k_pop = ModelMV.objects.filter(category_MV='K-Pop').order_by('-time_Post')
        lst_k_pop = lst_k_pop[0:6]  # Lấy 6 mv đầu tiên

        lst_us_uk = ModelMV.objects.filter(category_MV='US-UK').order_by('-time_Post')
        lst_us_uk = lst_us_uk[0:6]  # Lấy 6 mv đầu tiên

        context = {
            'lst_v_pop': lst_v_pop,
            'lst_k_pop': lst_k_pop,
            'lst_us_uk': lst_us_uk
        }
        return render(request, 'mv/home.html', context)


class detail_mv(generic.DetailView):
    model = ModelMV
    context_object_name = 'mv'
    template_name = 'mv/mv_detail.html'
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'

    # Đếm lượt truy cập mỗi mv
    def get_object(self):
        obj = super().get_object()
        obj.view += 1
        obj.save()
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mv'] = ModelMV.objects.get(slug=self.kwargs['the_slug'])
        context['total_likes'] = context['mv'].total_likes()
        if context['mv'].author_MV.profile.user.last_name:
            name = context['mv'].author_MV.profile.user.last_name + ' ' + context[
                'mv'].author_MV.profile.user.first_name
            context['name'] = name
        else:
            context['name'] = context['mv'].author_MV.profile.user.username
        return context


class mv_detail_frontview(generic.DetailView):
    model = ModelMV
    context_object_name = 'mv'
    template_name = 'mv/mv_detail_frontview.html'
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'


def base(request):
    return render(request, 'mv/base.html')


def upload(request):
    return render(request, 'mv/base.html')


def autosearch(request):
    query1 = request.GET.get('term')
    query = unidecode(query1)
    queryset = ModelMV.objects.filter(name1_MV__icontains=query)
    mylist = []
    mylist += [x.name_MV for x in queryset]

    queryset1 = ModelMV.objects.filter(singer_MV__icontains=query1)
    for x in queryset1:
        mylist.append(x.singer_MV)

    return JsonResponse(mylist, safe=False)


class search(views.View):
    def get(self, request):
        query = request.GET.get('search')

        if query is not None:
            lst_mv = ModelMV.objects.filter(name_MV__icontains=query)
            context = {
                'lst_mv': lst_mv,
                'query': query,
            }

            return render(request, 'mv/search.html', context)
        return HttpResponse(query)


class UpdateMV(generic.UpdateView):
    model = ModelMV
    fields = ['name_MV', 'singer_MV', 'intro_MV', 'img_MV', 'link_Youtube', 'description_MV']
    template_name = 'mv/upload.html'
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'

    def get_absolute_url(self):
        return reverse('mv:mv_detail_frontview', kwargs={'the_slug': self.slug})


@login_required()
def Like_MV(request, the_slug):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('mv:detail_mv', args=[str(the_slug)]))
    else:
        mv = get_object_or_404(ModelMV, id=request.POST.get('mv-id'))

        if mv.likes.filter(id=request.user.id).exists():
            mv.likes.remove(request.user)
        else:
            mv.likes.add(request.user)

        return HttpResponseRedirect(reverse('mv:detail_mv', args=[str(the_slug)]))


class CreateMV(generic.CreateView):
    model = ModelMV
    fields = ['name_MV', 'singer_MV', 'category_MV', 'intro_MV', 'img_MV', 'link_Youtube', 'description_MV']
    template_name = 'mv/upload.html'

    # Nhận biết user post bài
    def form_valid(self, form):
        form.instance.author_MV = self.request.user
        return super().form_valid(form)


class lst_Vpop(generic.ListView):
    model = ModelMV
    template_name = 'mv/v-pop.html'
    context_object_name = 'context'
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        top = ModelMV.objects.filter(category_MV='V-Pop').order_by('-likes')
        context['top'] = top[:3]
        lst = ModelMV.objects.filter(category_MV='V-Pop').order_by('-view')
        context['lst'] = lst
        context['active'] = 'v-pop'
        return context


class lst_Kpop(generic.ListView):
    model = ModelMV
    template_name = 'mv/k-pop.html'
    context_object_name = 'context'
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        top = ModelMV.objects.filter(category_MV='K-Pop').order_by('-likes')
        context['top'] = top[:3]
        lst = ModelMV.objects.filter(category_MV='K-Pop').order_by('-view')
        context['lst'] = lst
        context['active'] = 'k-pop'
        return context


class lst_UsUk(generic.ListView):
    model = ModelMV
    template_name = 'mv/us-uk.html'
    context_object_name = 'context'
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        top = ModelMV.objects.filter(category_MV='US-UK').order_by('-likes')
        context['top'] = top[:3]
        lst = ModelMV.objects.filter(category_MV='US-UK').order_by('-view')
        context['lst'] = lst
        context['active'] = 'us-uk'
        return context


# rest_framework
class mv_api(APIView):
    def get(self, request, the_slug):
        mv = ModelMV.objects.get(slug=the_slug)
        my_data = Get_mv(mv)
        return Response(data=my_data.data, status=status.HTTP_200_OK)

