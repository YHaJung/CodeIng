import simplejson as json

from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.core import serializers
from .models import Lecture, Category, Siteinfo
from rest_framework import viewsets, status
from .serializers import LectureSerializer, CategorySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    authentication_classes = (TokenAuthentication,)  # 기본적으로는 하나의 Auth를 이용하는데 추가할 수 있음
    permission_classes = (IsAuthenticated,)  # 이 함수는 authentication이 필요


@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        snippets = Category.objects.all()
        serializer = CategorySerializer(snippets, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    try:
        snippet = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(snippet)

        return Response(serializer.data)
    elif request.method == 'PUT':
        print(request.data, '이다')
        serializer = CategorySerializer(snippet, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        snippet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def lecture_list(request):
    if request.method == 'GET':
        try:

            # param 값이 0~5 사이의 숫자값이 아니면, 예외처리하기
            selected_level = float(request.GET.get('level', '0'))
            selected_price = int(request.GET.get('price', '0'))
            selected_rating = float(request.GET.get('rating', '0'))
            page = int(request.GET.get('page','1'))
            if page<=0:
                page = 1

            #잘못된 파라미터 값이 들어왔을 경우
            if selected_level<0 or selected_level>5 or selected_rating<0 or selected_rating>5 or selected_price<0:
                raise Exception
            # print(selected_level,selected_price, selected_rating,'이다아아아')
            # 쿼리문
            lectures = Lecture.objects.filter(level__gte=selected_level, rating__gte=selected_rating).select_related(
                'siteinfo')[page*6-5:page*6+1]
            lec_dict = {}
            lec_dict['isSuccess'] = 'true'
            lec_dict['code'] = 200
            lec_dict['message'] = '강의 목록 조회 성공'
            info = []

            for lec in lectures:
                h = lec.siteinfo.sitename
                info.append(
                    dict([('lectureIdx', lec.lectureidx), ('lectureName', lec.lecturename), ('professor', lec.lecturer),
                          ('price', lec.price), ('level', lec.level), ('rating', lec.rating),
                          ('thumbUrl', lec.thumburl), ('siteName', h)]))

            lec_dict['result'] = info

            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        except Exception:

            lec_dict = {}
            lec_dict['isSuccess'] = 'false'
            lec_dict['code'] = 400
            lec_dict['message'] = '파라미터 입력값 오류'

            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_400_BAD_REQUEST)
