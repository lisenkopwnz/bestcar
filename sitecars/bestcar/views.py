import logging

from django.utils import timezone

from bestcar.services.services_search import TripFilterService, User_trip_object
from bestcar.utils import DataMixin
from bestcar.models import *
from bestcar.forms import Update_form, Publishing_a_tripForm, SearchForm
from common.elasticsearch.document import PublishingTripDocument
from common.services.services import elasticsearch_formatting_date


from sitecars import settings

from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, Http404, JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin


logger = logging.getLogger('duration_request_view')


class BaseView(View):
    """ Базовый класс который отлавливает все исклюяения ,которые
        не были обработаны ранее """

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self._response(e, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        """Форматируем HTTP ответ с описание ошибки или формируем JSON ответ в случае необходимости """
        if status != 200:
            res = JsonResponse({
                "errorMessage": str(data),
                "status": status
            })
        else:
            res = JsonResponse({
                "data": str(data),
                "status": status
            })
        return res


class HomeBestcar(DataMixin, TemplateView):
    form_class = SearchForm
    model = Publishing_a_trip
    template_name = 'bestcar/index.html'
    title_page = 'Главная страница'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return self.get_mixin_context(context)


class Bus_trip(DataMixin, ListView):
    form_class = SearchForm
    model = Publishing_a_trip
    template_name = 'bestcar/bus_trip.html'
    title_page = 'На автобусе'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return self.get_mixin_context(context)


class Car_trip(DataMixin, ListView):
    form_class = SearchForm
    model = Publishing_a_trip
    template_name = 'bestcar/car_trip.html'
    title_page = 'На машине'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return self.get_mixin_context(context)


class SearchTrip(DataMixin, ListView):
    """
        Класс для поиска поездок с использованием формы поиска и фильтрации данных.
        Наследует от ListView и DataMixin для работы с шаблонами и контекстом.
    """
    context_object_name = 'search_trip_result'
    template_name = 'bestcar/search.html'
    title_page = 'Поиск'

    def get_context_data(self, **kwargs):
        """
            Возвращает контекст для шаблона, добавляя данные из миксина.
        """
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

    def get_data_request(self,form):
        """
            Извлекает и форматирует данные из формы поиска.

            :param form: форма поиска.
            :return: словарь с данными формы и дополнительной информацией из GET-запроса.
        """
        if form.is_valid():

            # Данные формы
            departure = form.cleaned_data['departure']
            arrival = form.cleaned_data['arrival']
            seating = form.cleaned_data['seating']
            datetime_value = form.cleaned_data['datetime']

            # Получаем значение скрытого поля из GET-запроса
            cat = self.request.GET.get('cat')

            return {
                'departure':departure,
                'arrival': arrival,
                'seating': seating,
                'datetime_value': elasticsearch_formatting_date(datetime_value),
                'cat':cat
            }
    @staticmethod
    def is_transport_category(cat):
        """
            Проверяет, является ли переданная категория транспортом.

            :param cat: категория транспорта.
            :return: True, если категория - автобус или автомобиль, иначе False.
        """
        if cat in ('Автобус', 'Автомобиль'):
            return True
        return False

    def get_queryset(self):
        """
            Формирует и возвращает запрос для поиска поездок, учитывая фильтрацию по времени и категориям.

            :return: отфильтрованный запрос для поиска.
        """

        # Создаем запрос для поиска документов,
        # где значение поля departure_time больше или равно текущему времени

        queryset = PublishingTripDocument.search().filter(
            'range', departure_time={'gte': elasticsearch_formatting_date(timezone.now())}
        )

        # Создаем экземпляр формы
        form = SearchForm(self.request.GET)

        # Получаем данные из формы
        data = self.get_data_request(form)
        cat = data.get('cat')

        if SearchTrip.is_transport_category(cat):

            queryset = queryset.filter('term', author__category_name=cat)
            return TripFilterService.filter_trip( queryset, data)

        return TripFilterService.filter_trip( queryset, data)


class Post(DataMixin, LoginRequiredMixin, CreateView):
    form_class = Publishing_a_tripForm
    template_name = 'bestcar/post.html'
    success_url = reverse_lazy('home')
    title_page = 'Опубликовать поездку'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class Update_user_trip(DataMixin, BaseView, UpdateView):
    """
        Представление для извенения параметров поездки
    """
    model = Publishing_a_trip
    form_class = Update_form
    template_name = 'bestcar/update.html'
    success_url = reverse_lazy('home')
    title_page = 'Форма для изменения данных поездки'

    def get(self, request, *args, **kwargs):
        try:
            slug = kwargs['slug']
            User_trip_object.users_trip_object(slug)
            logger.info('запись успешно найдена')
            return super().get(self, request, *args, **kwargs)
        except Http404 as e:
            logger.error(f'произошла ошибка {e}')
            return JsonResponse({
                "errorMessage": str(e),
                "status": 400
            })

    def form_valid(self, form):
        # здесь нужно дабавить отправку сигнала ввиде сообщения об изменениях в поездке
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h>Упс ,что пошло не так</h>")


class About(DataMixin, TemplateView):
    template_name = 'bestcar/about.html'
    title_page = 'О сайте'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
