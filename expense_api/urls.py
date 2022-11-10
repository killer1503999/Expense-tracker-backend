from django.urls import path, include
from .views import *

urlpatterns = [path('', userDetailsList.as_view()),
               path('<pk>/', userDetailsList.as_view()),
               #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
               path('<pk>/expense/', expenseDetailsList.as_view()),
               path('<pk>/expense/details/<id>/',
                    expenseDetailsDetails.as_view()),
               path('<pk>/approver/expense/', expenseDetailsList.as_view()),
               path('<pk>/approver/details/<id>/',
                    expenseDetailsDetails.as_view()),
               path('<pk>/approver/access/<id>/', approversAccess.as_view()),
               path('<pk>/approver/access/', approversAccess.as_view())

               ]
