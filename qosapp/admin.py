from django.contrib import admin

from .models import Flow
from .models import Meter
from .models import User
admin.site.register(Flow)
admin.site.register(Meter)
admin.site.register(User)
# Register your models here.
