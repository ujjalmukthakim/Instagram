from rest_framework.routers import DefaultRouter
from .views import MainGroupViewSet, SubGroupViewSet
from .views import VerifyActivityView
from .views import SubGroupWeeklyActivities,WeeklyActivityPercentage,PostBookingView,WeeklyPostBooking,AdminWeeklyPosts,ApproveWeeklyPost
from django.urls import path

router = DefaultRouter()
router.register('main-groups', MainGroupViewSet)
router.register('sub-groups', SubGroupViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('verify-activity/', VerifyActivityView.as_view()),
    path('weekly-activities/<int:subgroup_id>/', SubGroupWeeklyActivities.as_view()),
    path('weekly-activity-percent/<int:subgroup_id>/', WeeklyActivityPercentage.as_view()),
    path('book-post/', PostBookingView.as_view()),
    path('book-weekly-post/', WeeklyPostBooking.as_view()),
    path('admin-weekly-posts/', AdminWeeklyPosts.as_view()),
    path('approve-weekly-post/', ApproveWeeklyPost.as_view()),




]
