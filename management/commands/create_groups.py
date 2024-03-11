




import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cokhi.settings")

# Setup Django
django.setup()

from django.contrib.auth.models import Group, Permission
from nobarcode.models import Sno
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create groups and assign permissions'

    def handle(self, *args, **options):
        # Tạo nhóm toàn quyền
        full_access_group, created = Group.objects.get_or_create(name='Group I')
        full_access_permissions = Permission.objects.filter(content_type__app_label='nobarcode', codename__in=['add_sno', 'change_sno', 'delete_sno'])
        full_access_group.permissions.set(full_access_permissions)

        # Tạo nhóm quyền chỉnh sửa
        edit_access_group, created = Group.objects.get_or_create(name='Group II')
        edit_access_permissions = Permission.objects.filter(content_type__app_label='nobarcode', codename__in=['change_sno'])
        edit_access_group.permissions.set(edit_access_permissions)

        # Tạo nhóm quyền xem
        view_access_group, created = Group.objects.get_or_create(name='Group III')
        view_access_permissions = Permission.objects.filter(content_type__app_label='nobarcode', codename__in=['view_sno'])
        view_access_group.permissions.set(view_access_permissions)

        self.stdout.write(self.style.SUCCESS('Groups and permissions created successfully.'))
