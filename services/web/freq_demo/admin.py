from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm

def customize_admin():
    admin.site.site_header = 'Feature Request Tracker'
    admin.site.site_title = 'Freq'
    admin.site.index_title = 'Track Feature Requests with Freq'
    admin.site.site_url = None

    # allow non-staff users to access admin views
    def is_user_active(request):
      return request.user.is_active
    admin.site.has_permission = is_user_active

    # allow non-staff users to log in
    admin.site.login_form = AuthenticationForm
