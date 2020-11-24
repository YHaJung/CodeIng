import datetime
import time

import jwt
from django.conf.global_settings import SECRET_KEY
import simplejson as json
from django.db.models import Count

from django.http import JsonResponse, HttpResponse, QueryDict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Lecture, Profile, Classmember, Study, Classtag


def convert_time(createdat):
    now = datetime.datetime.now()
    createdAt = createdat
    time = now - createdAt

    if time < datetime.timedelta(minutes=1):
        return '방금 전'
    elif time < datetime.timedelta(hours=1):
        return str(int(time.seconds / 60)) + '분 전'
    elif time < datetime.timedelta(days=1):
        return str(int(time.seconds / 3600)) + '시간 전'
    elif time < datetime.timedelta(days=7):
        time = now.date() - createdAt.date()
        return str(time.days) + '일 전'
    elif time < datetime.timedelta(weeks=4):
        time = now.date() - createdAt.date()
        return str(int(time.days / 7)) + '주 전'
    elif time < datetime.timedelta(weeks=48):
        time = now.date() - createdAt.date()
        return str(int(time.days / 28)) + '달 전'
    else:
        time = now.date() - createdAt.date()
        return str(int(time.days / (28 * 12))) + '년 전'

def login_decorator(func):
    def wrapper(request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
            #만료 확인
            expire = payload['expire']

            if int(time.time()) > expire:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': '유효기간이 만료된 토큰'}, status=400)


            #유저 확인
            user = Profile.objects.get(email=payload['email'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'isSuccess' : 'false',
                                 'code' : 400,
                                 'message' : 'INVALID_TOKEN' }, status=400)

        except Profile.DoesNotExist:
            return JsonResponse({'isSuccess' : 'false',
                                 'code' : 400,
                                 'message' : 'INVALID_USER' }, status=400)

        return func( request, *args, **kwargs)

    return wrapper


def expire_check(access_token):

        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
            # 만료 확인
            expire = payload['expire']
            if int(time.time()) > expire:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': '유효기간이 만료된 토큰'}, status=400)



        except jwt.exceptions.DecodeError:
            return JsonResponse({'isSuccess' : 'false',
                                 'code' : 400,
                                 'message' : 'INVALID_TOKEN' }, status=400)




# 삭제 함수(comment or qna or review)
def delete(list_value, serializer_type):
    for ele in list_value:
        item = {}
        item['isdeleted'] = 'Y'
        itemQuery = QueryDict('', mutable=True)
        itemQuery.update(item)
        print(itemQuery)
        serializer = serializer_type(ele, data=itemQuery, partial=True)

        if serializer.is_valid():
            serializer.save()


# 예외 처리 함수 (파라미터 입력값 오류)
def for_exception():
    lec_dict = {}
    lec_dict['isSuccess'] = 'false'
    lec_dict['code'] = 400
    lec_dict['message'] = '파라미터 입력값 오류'

    return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

    return HttpResponse(return_value, content_type="text/json-comment-filtered",
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def class_list(request):
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', '1'))
            if page <= 0:
                page = 1

            classes =[]

            class_list = Study.objects.filter(isdeleted='N')[page * 6 - 6:page * 6]
            for c in class_list:

                member = Classmember.objects.filter(classidx__classidx=c.classidx,isdeleted='N').values('classidx__classidx').annotate(count=Count('classidx__classidx'))
                tag = Classtag.objects.filter(classidx__classidx=c.classidx,isdeleted='N')
                tag_list =[]
                for i in tag:
                    tag_list.append(i.tagname)


                classes.append(
                    dict([('classIdx', c.classidx), ('className', c.classname), ('thumbUrl', c.lectureidx.thumburl),
                          ('memberCount', member[0]['count']), ('tags', tag_list), ('password', c.password)]))




            lec_dict = {}
            lec_dict['isSuccess'] = 'true'
            lec_dict['code'] = 200
            lec_dict['message'] = '전체 클래스 목록 조회 성공'
            lec_dict['result'] = classes

            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        except Exception:

            return for_exception()



@api_view(['GET'])
@login_decorator
def myclass_list(request):
    if request.method == 'GET':
        try:

            userIdx = request.user.userinfo.useridx
            page = int(request.GET.get('page', '1'))
            if page <= 0:
                page = 1

            classes =[]

            myclass_list = Classmember.objects.filter(user__useridx = userIdx,isdeleted='N')
            for c in myclass_list:

                member = Classmember.objects.filter(classidx__classidx=c.classidx.classidx,isdeleted='N').values('classidx__classidx').annotate(count=Count('classidx__classidx'))
                tag = Classtag.objects.filter(classidx__classidx=c.classidx.classidx,isdeleted='N')
                tag_list =[]
                for i in tag:
                    tag_list.append(i.tagname)


                classes.append(
                    dict([('classIdx', c.classidx.classidx), ('className', c.classidx.classname), ('thumbUrl', c.classidx.lectureidx.thumburl),
                          ('memberCount', member[0]['count']), ('tags', tag_list), ('password', c.classidx.password)]))




            lec_dict = {}
            lec_dict['isSuccess'] = 'true'
            lec_dict['code'] = 200
            lec_dict['message'] = '나의 클래스 목록 조회 성공'
            lec_dict['result'] = classes

            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        except Exception:

            return for_exception()








