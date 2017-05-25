# from django.conf import settings
# from forum.models import Session,User
# from django.utils.deprecation import MiddlewareMixin
# import datetime
#
#
# class LoginRequireMiddleware(MiddlewareMixin):
#
#     def process_request(self,request):
#         try:
#             sessid = request.COOKIES.get('sessid')
#             session = Session.objects.get(
#                 key=sessid,
#                 expires__gt=datetime.datetime.now(),
#             )
#             request.session = session
#             request.user = session.user
#         except (Session.DoesNotExist, User.DoesNotExist):
#             request.session = None
#             request.user = None
