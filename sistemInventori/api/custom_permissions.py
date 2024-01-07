from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
   def has_permission(self, request, view):
      if request.user.jabatan == "admin":
         return True
      return False

class IsItSupport(BasePermission):
   def has_permission(self, request, view):
      if request.user.jabatan == "it_support":
         return True
      return False

class IsKaryawan(BasePermission):
   def has_permission(self, request, view):
      if request.user.jabatan == "karyawan":
         return True
      return False

class IsRoleExtend(BasePermission):
   def has_permission(self, request, view):
      if request.user.jabatan == "karyawan" or request.user.jabatan == "it_support":
         if request.method == "GET":
            return True