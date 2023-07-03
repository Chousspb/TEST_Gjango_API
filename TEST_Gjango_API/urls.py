from django.conf.urls.static import static
from django.urls import path
from TEST_Gjango_API import settings
from salary.views import login, get_salary, token, expired, index
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", index, name="index"),
    path("login/", login, name="login"),  # Изменение пути здесь
    path("salary/", get_salary, name="salary"),
    path("token/", token, name="token"),  # Изменение пути здесь
    path("expired/", expired, name="expired"),  # Изменение пути здесь
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)