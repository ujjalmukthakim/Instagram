from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from groups.models import MainGroup, SubGroup

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {}

        # CEO: sees all users
        if user.role == "CEO":
            data["members"] = User.objects.count()
            data["pending"] = User.objects.filter(is_approved=False).count()

        # DIRECTOR: sees all main groups (you can customize which main groups they manage)
        elif user.role == "DIRECTOR":
            main_groups = MainGroup.objects.all()  # adjust if director only manages specific groups
            users_in_groups = User.objects.filter(main_group__in=main_groups)
            data["members"] = users_in_groups.count()
            data["pending"] = users_in_groups.filter(is_approved=False).count()

        # DELTA: sees their main group + all its subgroups
        elif user.role == "DELTA":
            main_group = user.main_group
            subgroups = SubGroup.objects.filter(main_group=main_group)
            users_in_subgroups = User.objects.filter(sub_group__in=subgroups)
            data["members"] = users_in_subgroups.count()
            data["pending"] = users_in_subgroups.filter(is_approved=False).count()

        # CODE: sees only their own subgroup
        elif user.role == "CODE":
            sub_group = user.sub_group
            users_in_subgroup = User.objects.filter(sub_group=sub_group)
            data["members"] = users_in_subgroup.count()
            data["pending"] = users_in_subgroup.filter(is_approved=False).count()

        # Normal user
        else:
            data["members"] = 1
            data["pending"] = 0

        return Response(data)
