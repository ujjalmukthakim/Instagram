from rest_framework import viewsets, permissions
from .models import MainGroup, SubGroup,PostBooking,WeeklyPost
from .serializers import MainGroupSerializer, SubGroupSerializer,WeeklyPostSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q

from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import DailyActivity

from rest_framework.views import APIView

from users.models import User

class MainGroupViewSet(viewsets.ModelViewSet):
    queryset = MainGroup.objects.all()
    serializer_class = MainGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubGroupViewSet(viewsets.ModelViewSet):
    queryset = SubGroup.objects.all()
    serializer_class = SubGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def done(self, request, pk=None):
        subgroup = self.get_object()
        user = request.user

        if user.role != 'Member':
            return Response({"error": "Only members allowed"}, status=403)

        today = timezone.now().date()

        activity, created = DailyActivity.objects.get_or_create(
            member=user,
            subgroup=subgroup,
            date=today
        )

        return Response({"message": "Done recorded"})


class VerifyActivityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.role != 'Code':
            return Response({"error": "Only Code admin allowed"}, status=403)

        activity_id = request.data.get("activity_id")
        status_value = request.data.get("status")

        activity = DailyActivity.objects.get(id=activity_id)
        activity.status = status_value
        activity.save()

        return Response({"message": "Activity updated"})
    


class SubGroupWeeklyActivities(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subgroup_id):
        user = request.user
        if user.role != 'Code':
            return Response({"error": "Only Code admin allowed"}, status=403)

        today = timezone.now().date()
        start_week = today - timezone.timedelta(days=today.weekday())  # Monday
        end_week = start_week + timezone.timedelta(days=6)  # Sunday

        activities = DailyActivity.objects.filter(
            subgroup_id=subgroup_id,
            date__range=[start_week, end_week]
        ).select_related('member')

        data = []
        for a in activities:
            data.append({
                "id": a.id,
                "member_id": a.member.id,
                "member_username": a.member.username,
                "date": a.date,
                "status": a.status
            })

        return Response(data)
    



class WeeklyActivityPercentage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subgroup_id):
        user = request.user
        if user.role not in ['Code', 'Delta', 'Director', 'CEO']:
            return Response({"error": "Only admins allowed"}, status=403)

        today = timezone.now().date()
        start_week = today - timezone.timedelta(days=today.weekday())
        end_week = start_week + timezone.timedelta(days=6)

        members = User.objects.filter(sub_group_id=subgroup_id, role='Member')

        result = []
        for member in members:
            total_days = 7  # Mon-Sun
            active_days = DailyActivity.objects.filter(
                member=member,
                date__range=[start_week, end_week],
                status='Active'
            ).count()
            percentage = (active_days / total_days) * 100
            result.append({
                "member_id": member.id,
                "username": member.username,
                "activity_percentage": percentage
            })

        return Response(result)


class PostBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'Member':
            return Response({"error": "Only members can book"}, status=403)

        booking_date = request.data.get("booking_date")
        main_group_id = request.data.get("main_group_id")

        # Check if booking is Friday
        booking_day = timezone.datetime.strptime(booking_date, "%Y-%m-%d").weekday()
        if booking_day != 4:  # Friday = 4
            return Response({"error": "Only Fridays can be booked"}, status=400)

        # Check activity %
        start_week = timezone.now().date() - timezone.timedelta(days=timezone.now().date().weekday())
        end_week = start_week + timezone.timedelta(days=6)
        active_days = DailyActivity.objects.filter(
            member=user,
            date__range=[start_week, end_week],
            status='Active'
        ).count()
        percentage = (active_days / 7) * 100
        if percentage < 80:
            return Response({"error": "Activity less than 80%, cannot book"}, status=403)

        # Create booking
        booking, created = PostBooking.objects.get_or_create(
            member=user,
            main_group_id=main_group_id,
            booking_date=booking_date
        )
        if not created:
            return Response({"error": "Already booked this date"}, status=400)

        return Response({"message": "Booking successful"})


class WeeklyPostBooking(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'Member':
            return Response({"error": "Only members can book posts"}, status=403)

        post_link = request.data.get("post_link")
        booking_date = request.data.get("booking_date")
        main_group_id = request.data.get("main_group_id")

        # Check if booking is Friday
        booking_day = timezone.datetime.strptime(booking_date, "%Y-%m-%d").weekday()
        if booking_day == 4:  # Friday = 4
            return Response({"error": "Cannot share post on Friday"}, status=400)

        # Check if member already booked for the week
        start_week = timezone.now().date() - timezone.timedelta(days=timezone.now().date().weekday())
        end_week = start_week + timezone.timedelta(days=6)
        existing_post = WeeklyPost.objects.filter(
            member=user,
            booking_date__range=[start_week, end_week]
        ).first()
        if existing_post:
            return Response({"error": "You already booked a post this week"}, status=400)

        # Create post booking
        post = WeeklyPost.objects.create(
            member=user,
            main_group_id=main_group_id,
            post_link=post_link,
            booking_date=booking_date
        )

        return Response({"message": "Post booked successfully", "post_id": post.id})


class AdminWeeklyPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == 'Delta':
            # Delta sees only their main group
            posts = WeeklyPost.objects.filter(main_group_id=user.main_group.id)
        elif user.role in ['Director', 'CEO']:
            # Director & CEO sees all posts
            posts = WeeklyPost.objects.all()
        else:
            return Response({"error": "Not allowed"}, status=403)

        serializer = WeeklyPostSerializer(posts, many=True)
        return Response(serializer.data)


class ApproveWeeklyPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role not in ['Delta', 'Director', 'CEO']:
            return Response({"error": "Not allowed"}, status=403)

        post_id = request.data.get("post_id")
        status = request.data.get("status")  # Approved or Rejected

        post = WeeklyPost.objects.get(id=post_id)
        post.status = status
        post.save()

        return Response({"message": "Status updated"})
