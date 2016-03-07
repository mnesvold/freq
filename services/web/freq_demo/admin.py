from django.contrib import admin

def customize_admin():
    admin.site.site_header = 'Feature Request Tracker'
    admin.site.site_title = 'Freq'
    admin.site.index_title = 'Track Feature Requests with Freq'
    admin.site.site_url = None

    def is_user_active(request):
      return request.user.is_active
    admin.site.has_permission = is_user_active
