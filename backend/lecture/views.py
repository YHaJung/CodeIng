from datetime import datetime
from django.utils import timezone
import simplejson as json
from django.db.models import Count

from django.http import JsonResponse, HttpResponse, QueryDict
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.core import serializers
from .models import Lecture, Category, Siteinfo, Lecturecategory, Review, Userinfo, Profile, Reviewpros, Reviewcons, \
    Likesforreview, Qna, Likesforqna, Qnaimage
from rest_framework import viewsets, status
from .serializers import LectureSerializer, CategorySerializer, QnaSerializer
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

##################################
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

            # 쿼리문
            lectures = Lecture.objects.filter(
                level__gte=selected_level, rating__gte=selected_rating, price__lte=selected_price).select_related('siteinfo')[page*6-6:page*6]
            lec_dict = {}
            lec_dict['isSuccess'] = 'true'
            lec_dict['code'] = 200
            lec_dict['message'] = '강의 목록 조회 성공'
            info = []

            for lec in lectures:
                h = lec.siteinfo.sitename
                price_sql = lec.price
                if price_sql == 0:
                    price_sql = 'free'
                elif price_sql == -1:
                    price_sql ='membership'


                info.append(
                    dict([('lectureIdx', lec.lectureidx), ('lectureName', lec.lecturename), ('professor', lec.lecturer),
                          ('price', price_sql), ('level', lec.level), ('rating', lec.rating),
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
################################
@api_view(['GET'])
def lectures_ranking(request):
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', '1'))
            categoryIdx = int(request.GET.get('categoryIdx', '1'))
            subcategoryIdx = int(request.GET.get('subcategoryIdx', '0'))

            subcategory = Lecturecategory.objects.filter(categoryidx=categoryIdx).select_related('subcategory').values('subcategory__subcategoryname','subcategory__subcategoryidx').distinct().order_by('subcategory__subcategoryidx')

            subcategory_list =[]
            for ele in subcategory:
                subcategory_list.append(
                dict([('subcategoryIdx',ele['subcategory__subcategoryidx']),('subcategoryName',ele['subcategory__subcategoryname'])])
                )

            if subcategoryIdx !=0:
                # 서브카테고리까지 골랐을 경우,
                category_ranking = Lecturecategory.objects.filter(categoryidx=categoryIdx,subcategoryidx=subcategoryIdx).select_related('lecture').order_by('-lecture__rating')
            else:
                #카테고리만 골랐을 경우,
                category_ranking = Lecturecategory.objects.filter(categoryidx=categoryIdx).select_related('lecture').order_by('-lecture__rating')

            category_ranking_all = category_ranking.values('lecture__lectureidx','lecture__lecturename','lecture__lecturer','lecture__thumburl','lecture__price','lecture__level','lecture__siteinfo__sitename').distinct()[page*5-5:page*5]

            lec_rank_dict = {}
            lec_rank_dict['isSuccess'] = 'true'
            lec_rank_dict['code'] = 200
            lec_rank_dict['message'] = '카테고리 별 랭킹 조회 성공'

            lec_rank_dict['subcategory'] = subcategory_list
            rank = []


            for c in category_ranking_all:

                price_sql = c['lecture__price']
                if price_sql == 0:
                    price_sql = 'free'
                elif price_sql == -1:
                    price_sql = 'membership'
                rank.append(
                dict([('lectureIdx', c['lecture__lectureidx']), ('lectureName', c['lecture__lecturename']), ('professor', c['lecture__lecturer']),
                      ('price', price_sql), ('level', c['lecture__level']),('thumbUrl', c['lecture__thumburl']), ('siteName', c['lecture__siteinfo__sitename'])]))

            lec_rank_dict['result'] = rank

            return_value = json.dumps(lec_rank_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)



        except Exception:

            lec_dict = {}
            lec_dict['isSuccess'] = 'false'
            lec_dict['code'] = 400
            lec_dict['message'] = '파라미터 입력값 오류'

            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_400_BAD_REQUEST)

##################################
@api_view(['GET'])
def ranking_overview(request):
    try:
        overview_list = []
        overview_dict = {}
        overview_dict['isSuccess'] = 'true'
        overview_dict['code'] = 200
        overview_dict['message'] = '카테고리 별 랭킹 미리보기 조회 성공'

        categoryIdx = int(request.GET.get('categoryIdx', '1'))
        overview = Lecturecategory.objects.select_related('lecture')
        overview2 = overview.filter(categoryidx=categoryIdx).values('categoryidx','lecture__lectureidx','lecture__lecturename','lecture__lecturer','lecture__thumburl','lecture__level','lecture__siteinfo__sitename').distinct().order_by('-lecture__rating')[:5]
        cnt =1
        for i in overview2:
            overview_list.append(
                dict([('ranking',cnt),('lectureIdx', i['lecture__lectureidx']), ('lectureName', i['lecture__lecturename']),
                      ('level', i['lecture__level']), ('thumbUrl', i['lecture__thumburl']),
                      ('siteName', i['lecture__siteinfo__sitename'])]))
            cnt+=1
        overview_dict['result'] = overview_list
        return_value = json.dumps(overview_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Exception:

        lec_dict = {}
        lec_dict['isSuccess'] = 'false'
        lec_dict['code'] = 400
        lec_dict['message'] = '파라미터 입력값 오류'

        return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def lecture_detail(request, pk):
    try:
        lecture = Lecture.objects.get(pk=pk)
        print(lecture)
        detail_list = []

        detail_dict = {}
        detail_dict['isSuccess'] = 'true'
        detail_dict['code'] = 200
        detail_dict['message'] = '강의 상세보기 조회 성공'
        price_sql = lecture.price
        if price_sql == 0:
            price_sql = 'free'
        elif price_sql == -1:
            price_sql = 'membership'

        detail_dict['result'] = dict([('lectureIdx', lecture.lectureidx), ('lectureName', lecture.lecturename), ('lectureLink', lecture.lecturelink),
                      ('price', price_sql), ('level', lecture.level), ('rating', lecture.rating)])


        return_value = json.dumps(detail_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

    except Exception:

        lec_dict = {}
        lec_dict['isSuccess'] = 'false'
        lec_dict['code'] = 400
        lec_dict['message'] = '파라미터 입력값 오류'

        return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def review_list(request, pk):
    try:
        page = int(request.GET.get('page', '1'))
        review_list = []
        review_dict = {}
        review_dict['isSuccess'] = 'true'
        review_dict['code'] = 200
        review_dict['message'] = '강의 리뷰 목록 조회 성공'

        review_userinfo = Review.objects.filter(lectureidx=pk).select_related('profile')[page*5-5:page*5]

        pros = Reviewpros.objects.filter(review__lectureidx=pk).select_related('review')

        cons = Reviewcons.objects.filter(review__lectureidx=pk).select_related('review')

        likes = Likesforreview.objects.filter(review__lectureidx=pk).select_related('review').values('review').annotate(count=Count('review'))

        likes_dict = {}

        for i in likes:
            likes_dict[i['review']] = i['count']


        major={'Y':'전공자', 'N':'비전공자'}
        job={'S':'학생','D':'개발자','N':'비개발 직군'}

        print(len(review_userinfo))
        for r in review_userinfo:

             if r.isblocked =='Y':
                 continue
             a = r.reviewidx
             try:
               likes_count = likes_dict[a]
             except Exception:
                  likes_count =0
                  pass

             pros2 = pros.filter(review=r.reviewidx)
             pros_list = []
             cons2 = cons.filter(review=r.reviewidx)
             cons_list = []

             for p in pros2:
                 pros_list.append(p.pros.prostype)


             for c in cons2:
                 cons_list.append(c.cons.constype)


             review_list.append(dict([('nickname', r.profile.userinfo.nickname),('userlevel', r.profile.level.levelname), ('profileImage', r.profile.userinfo.profileimg),
                                      ('job', job[r.profile.job]),('major', major[r.profile.major]), ('reviewidx', r.reviewidx),('totalRating', r.totalrating),
                                      ('priceRating', r.pricerating), ('teachingpowerRating', r.teachingpowerrating),('recommend',r.recommend) , ('improvement',r.improvement),
                                      ('likesCount',likes_count),('pros',pros_list),('cons',cons_list)
                                     ]))

        review_dict['result'] = review_list
        return_value = json.dumps(review_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Exception:

        lec_dict = {}
        lec_dict['isSuccess'] = 'false'
        lec_dict['code'] = 400
        lec_dict['message'] = '파라미터 입력값 오류'

        return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def qna_list(request, pk):
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', '1'))

            qna_list = []
            qna_dict = {}
            qna_dict['isSuccess'] = 'true'
            qna_dict['code'] = 200
            qna_dict['message'] = 'qna 목록 조회 성공'

            qna = Qna.objects.filter(lecture__lectureidx=pk,isblocked='N',isdeleted='N').select_related('userinfo','lecture')[page*5-5:page*5]

            likes = Likesforqna.objects.filter(qna__lecture__lectureidx=pk).select_related('qna').values('qna').annotate(count=Count('qna'))
            likes_dict = {}

            for i in likes:
                likes_dict[i['qna']] = i['count']


            for r in qna:
                try:
                    likes_count = likes_dict[r.qnaidx]
                except Exception:
                    likes_count = 0
                    pass
                print(r.createdat)
                qna_list.append(dict(
                  [('qnaIdx', r.qnaidx), ('qnaTitle', r.title),('qnaDes',r.qnades),('profileImg',r.userinfo.profileimg),
                   ('likesCount', likes_count)
                 ]))

            qna_dict['result'] = qna_list


            return_value = json.dumps(qna_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)



        except Exception:

            lec_dict = {}
            lec_dict['isSuccess'] = 'false'
            lec_dict['code'] = 400
            lec_dict['message'] = '파라미터 입력값 오류'

            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':

        try:
            serializer = QnaSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(isblocked='N',isdeleted='N')

                post_qna = {}
                post_qna['isSuccess'] = 'true'
                post_qna['code'] = 201
                post_qna['message'] = 'qna 작성 성공'
                post_qna['result'] = serializer.data

                return Response(post_qna, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


        except Exception:

            lec_dict = {}
            lec_dict['isSuccess'] = 'false'
            lec_dict['code'] = 400
            lec_dict['message'] = '파라미터 입력값 오류'

            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def qna_detail(request, pk, qnaIdx):
    try:
        qna_item = Qna.objects.get(pk=qnaIdx)

        if request.method =='GET':
            item = Qna.objects.select_related('userinfo').get(pk=qnaIdx)
            qnaimages = Qnaimage.objects.filter(qnaidx=qnaIdx).values('imgurl')
            for i in qnaimages:
                print(i['imgurl'])
            print(item.qnaidx, item.title, item.qnades, item.userinfo.profileimg, item.userinfo.nickname, item.createdat)



        elif request.method == 'PUT':
        # 내가 쓴 글일때만 수정 가능 -> 토큰에 해당하는 useridx랑 글 idx 비교하기, 이미지 수정은 어떻게 ..? ..?
            print(request.data, '이다')
            serializer = QnaSerializer(qna_item, data=request.data, partial=True)

            if serializer.is_valid():
               serializer.save()

            return Response(serializer.data)

        elif request.method == 'DELETE':
        # 내가 쓴 글 일때만 삭제 가능 -> 토큰에 해당하는 useridx랑 글 idx 비교하기, qna의 모든 답글, 이미지도 동시에 삭제되어야함
            item ={}
            item['isdeleted']='Y'
            itemQuery = QueryDict('', mutable=True)
            itemQuery.update(item)
            serializer = QnaSerializer(qna_item, data=itemQuery, partial=True)

            if serializer.is_valid():
               serializer.save()

            return Response(serializer.data)

    except Qna.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:

            lec_dict = {}
            lec_dict['isSuccess'] = 'false'
            lec_dict['code'] = 400
            lec_dict['message'] = '파라미터 입력값 오류'

            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_400_BAD_REQUEST)
