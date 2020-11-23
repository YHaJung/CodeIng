import datetime
import time

import jwt
from django.conf.global_settings import SECRET_KEY
import simplejson as json
from django.db.models import Count

from django.http import JsonResponse, HttpResponse, QueryDict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Lecture, Category, Siteinfo, Lecturecategory, Review, Userinfo, Profile, Reviewpros, Reviewcons, \
    Likesforreview, Qna, Likesforqna, Qnaimage, Comment, Commentimage, Pros, Favoritesite, Favoritelecture
from rest_framework import viewsets, status
from .serializers import LectureSerializer, CategorySerializer, QnaSerializer, CommentSerializer, \
    CommentimageSerializer, QnaimageSerializer, ReviewSerializer, ReviewprosSerializer, ReviewconsSerializer, \
    FavoritesiteSerializer, FavoritelectureSerializer


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
def lecture_list(request):
    if request.method == 'GET':
        try:
            # param 값이 0~5 사이의 숫자값이 아니면, 예외처리하기
            selected_level = int(request.GET.get('level', '0'))
            selected_price = int(request.GET.get('price', '0'))
            selected_rating = float(request.GET.get('rating', '0'))
            input_keyword = request.GET.get('keyword','')
            page = int(request.GET.get('page', '1'))



            if page <= 0:
                page = 1

            # 잘못된 파라미터 값이 들어왔을 경우
            if selected_level < 0 or selected_level > 5 or selected_rating < 0 or selected_rating > 5 or selected_price < 0:
                raise Exception



            if input_keyword =='':
                # 쿼리문
                if selected_level == 0:
                    lectures = Lecture.objects.filter(
                        rating__gte=selected_rating)[page * 6 - 6:page * 6]

                else:
                    lectures = Lecture.objects.filter(
                        level__levelidx=selected_level, rating__gte=selected_rating,
                        price__lte=selected_price).select_related(
                        'siteinfo')[page * 6 - 6:page * 6]




            else:
                if selected_level == 0:
                    lectures = Lecture.objects.filter(lecturename__icontains=input_keyword,
                                                      rating__gte=selected_rating,
                                                      price__lte=selected_price).select_related(
                        'siteinfo')[page * 6 - 6:page * 6]


                else:

                    lectures = Lecture.objects.filter(lecturename__icontains=input_keyword,
                        level__levelidx=selected_level, rating__gte=selected_rating, price__lte=selected_price).select_related(
                        'siteinfo')[page * 6 - 6:page * 6]


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
                    price_sql = 'membership'
                else:
                    price_sql = format(price_sql,',')

                info.append(
                    dict([('lectureIdx', lec.lectureidx), ('lectureName', lec.lecturename), ('professor', lec.lecturer),
                          ('price', price_sql), ('levelIdx', lec.level.levelidx), ('levelName', lec.level.levelname), ('rating', lec.rating),
                          ('thumbUrl', lec.thumburl), ('siteName', h)]))
            lec_dict['result'] = info

            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        except Exception:

            return for_exception()


@api_view(['GET'])
def subcategory_list(request):
    if request.method == 'GET':
        try:
            category_idx = int(request.GET.get('categoryIdx', '1'))


            subcategorys = Lecturecategory.objects.filter(categoryidx=category_idx).values(
            'subcategory__subcategoryidx', 'subcategory__subcategoryname').distinct().order_by('subcategory__subcategoryidx')

            lec_dict = {}
            lec_dict['isSuccess'] = 'true'
            lec_dict['code'] = 200
            lec_dict['message'] = '서브카테고리 목록 조회 성공'
            info = []

            for sub in subcategorys:

                info.append(
                    dict([('subcategoryIdx', sub['subcategory__subcategoryidx']), ('subcategoryName', sub['subcategory__subcategoryname'])]))

            lec_dict['result'] = info

            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        except Exception:

            return for_exception()




@api_view(['GET'])
def lectures_ranking(request):
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', '1'))
            categoryIdx = int(request.GET.get('categoryIdx', '1'))
            subcategoryIdx = int(request.GET.get('subcategoryIdx', '0'))

            subcategory = Lecturecategory.objects.filter(categoryidx=categoryIdx).select_related('subcategory').values(
                'subcategory__subcategoryname', 'subcategory__subcategoryidx').distinct().order_by(
                'subcategory__subcategoryidx')

            subcategory_list = []
            for ele in subcategory:
                subcategory_list.append(
                    dict([('subcategoryIdx', ele['subcategory__subcategoryidx']),
                          ('subcategoryName', ele['subcategory__subcategoryname'])])
                )

            if subcategoryIdx != 0:
                # 서브카테고리까지 골랐을 경우,

                category_ranking = Lecturecategory.objects.filter(categoryidx=categoryIdx,
                                                                  subcategory=subcategoryIdx).select_related('lecture').order_by('-lecture__rating')
            else:
                # 카테고리만 골랐을 경우,
                category_ranking = Lecturecategory.objects.filter(categoryidx=categoryIdx).select_related(
                    'lecture').order_by('-lecture__rating')

            category_ranking_all = category_ranking.values('lecture__lectureidx', 'lecture__lecturename','lecture__rating',
                                                           'lecture__lecturer', 'lecture__thumburl', 'lecture__price',
                                                           'lecture__level__levelname', 'lecture__siteinfo__sitename').distinct()[
                                   page * 5 - 5:page * 5]


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
                else:
                    price_sql = format(price_sql, ',')
                rank.append(
                    dict([('lectureIdx', c['lecture__lectureidx']), ('lectureName', c['lecture__lecturename']),
                          ('professor', c['lecture__lecturer']),('rating', c['lecture__rating']),
                          ('price', price_sql), ('level', c['lecture__level__levelname']), ('thumbUrl', c['lecture__thumburl']),
                          ('siteName', c['lecture__siteinfo__sitename'])]))

            lec_rank_dict['result'] = rank

            return_value = json.dumps(lec_rank_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)



        except Exception:

            return for_exception()


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
        overview2 = overview.filter(categoryidx=categoryIdx).values('categoryidx', 'lecture__lectureidx',
                                                                    'lecture__lecturename', 'lecture__lecturer',
                                                                    'lecture__thumburl', 'lecture__level',
                                                                    'lecture__siteinfo__sitename').distinct().order_by(
            '-lecture__rating')[:5]
        cnt = 1
        for i in overview2:



            overview_list.append(
                dict([('ranking', cnt), ('lectureIdx', i['lecture__lectureidx']),
                      ('lectureName', i['lecture__lecturename']),
                      ('level', i['lecture__level']), ('thumbUrl', i['lecture__thumburl']),
                      ('siteName', i['lecture__siteinfo__sitename'])]))
            cnt += 1
        overview_dict['result'] = overview_list
        return_value = json.dumps(overview_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Exception:

        return for_exception()



@api_view(['GET'])
def overall_ranking(request):
    try:
        overview_list = []
        overview_dict = {}
        overview_dict['isSuccess'] = 'true'
        overview_dict['code'] = 200
        overview_dict['message'] = '강의 전체 랭킹 조회 성공'

        lectures = Lecture.objects.all().order_by('-rating')[:5]
        for lec in lectures:
            price_sql = lec.price

            if price_sql == 0:
                price_sql = 'free'
            elif price_sql == -1:
                price_sql = 'membership'
            else:
                price_sql = format(price_sql, ',')

            overview_list.append(
                dict([('lectureIdx', lec.lectureidx), ('lectureName', lec.lecturename),
                      ('siteName', lec.siteinfo.sitename),
                      ('price', price_sql), ('thumbUrl', lec.thumburl),
                      ('rating', lec.rating), ('level', lec.level.levelname)]))

        overview_dict['result'] = overview_list
        return_value = json.dumps(overview_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Exception:

        return for_exception()










@api_view(['GET'])
def lecture_detail(request, pk):
    try:
        lecture = Lecture.objects.get(pk=pk)
        print(lecture)

        detail_dict = {}
        detail_dict['isSuccess'] = 'true'
        detail_dict['code'] = 200
        detail_dict['message'] = '강의 상세보기 조회 성공'
        price_sql = lecture.price
        if price_sql == 0:
            price_sql = 'free'
        elif price_sql == -1:
            price_sql = 'membership'

        else:
            price_sql = format(price_sql, ',')

        detail_dict['result'] = dict([('lectureIdx', lecture.lectureidx), ('lectureName', lecture.lecturename),
                                      ('lectureLink', lecture.lecturelink),
                                      ('price', price_sql), ('level', lecture.level.levelname), ('rating', lecture.rating), ('thumbUrl', lecture.thumburl)])

        return_value = json.dumps(detail_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

    except Exception:
        return for_exception()


@api_view(['GET','POST'])
def review_list(request, pk):
    try:
        if request.method == 'GET':
            page = int(request.GET.get('page', '1'))
            review_list = []
            review_dict = {}
            review_dict['isSuccess'] = 'true'
            review_dict['code'] = 200
            review_dict['message'] = '강의 리뷰 목록 조회 성공'

            review_userinfo = Review.objects.filter(lectureidx=pk).select_related('profile')[page * 5 - 5:page * 5]

            pros = Reviewpros.objects.filter(review__lectureidx=pk).select_related('review')

            cons = Reviewcons.objects.filter(review__lectureidx=pk).select_related('review')

            likes = Likesforreview.objects.filter(review__lectureidx=pk).select_related('review').values(
                'review').annotate(
                count=Count('review'))

            likes_dict = {}

            for i in likes:
                likes_dict[i['review']] = i['count']


            job = {'S': '초등학생', 'D': '전공자/비전공자', 'N': '비전공자/비개발 직군', 'T':'중/고등학생' }

            print(len(review_userinfo),"이다")
            for r in review_userinfo:

                if r.isblocked == 'Y':
                    continue
                a = r.reviewidx
                try:
                    likes_count = likes_dict[a]
                except Exception:
                    likes_count = 0
                    pass

                pros2 = pros.filter(review=r.reviewidx)
                pros_list = []
                cons2 = cons.filter(review=r.reviewidx)
                cons_list = []


                for p in pros2:
                    pros_list.append(p.pros.prostype)

                for c in cons2:
                    cons_list.append(c.cons.constype)


                review_list.append(dict(
                    [('nickname', r.profile.userinfo.nickname), ('userlevel', r.profile.level.levelname),
                     ('profileImage', r.profile.userinfo.profileimg),
                     ('job', r.profile.job), ('reviewidx', r.reviewidx),
                     ('totalRating', r.totalrating),
                     ('priceRating', r.pricerating), ('teachingpowerRating', r.teachingpowerrating),
                     ('recommend', r.recommend), ('improvement', r.improvement),
                     ('likesCount', likes_count), ('pros', pros_list), ('cons', cons_list)
                     ]))

            review_dict['result'] = review_list
            return_value = json.dumps(review_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        elif request.method == 'POST':
            try:
                access_token = request.headers.get('Authorization', None)
                payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')

                # 만료 확인
                expire = payload['expire']

                if int(time.time()) > expire:
                    return JsonResponse({'isSuccess': 'false',
                                         'code': 400,
                                         'message': '유효기간이 만료된 토큰'}, status=400)

                user = Profile.objects.get(email=payload['email'])
                request.user = user

            except jwt.exceptions.DecodeError:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': 'INVALID_TOKEN'}, status=400)

            except Profile.DoesNotExist:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': 'INVALID_USER'}, status=400)

            # jwt를 통해 얻어낸 정보
            userIdx = request.user.userinfo.useridx

            # 리뷰 저장
            a = Review.objects.last()
            reviewIdx = a.reviewidx + 1
            # 리뷰
            review_dict = QueryDict.dict(request.data)
            # 장점
            pros_list_dict = {}
            pros_list_dict['pros'] = review_dict['pros']
            # 단점
            cons_list_dict = {}
            cons_list_dict['cons'] = review_dict['cons']

            review_dict['profile'] = userIdx
            review_dict['lectureidx'] = pk
            review_dict['isdeleted'] = 'N'
            del review_dict['pros']
            del review_dict['cons']

            query_dict = QueryDict('', mutable=True)
            query_dict.update(review_dict)

            serializer = ReviewSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save()

            # 문자열 ->
            tmp = pros_list_dict['pros'][1:-1]
            new_list = tmp.split(',')

            for pros in new_list:
                temp_pros_dict = {}
                temp_pros_dict['pros'] = pros
                temp_pros_dict['review'] = reviewIdx
                temp_pros_dict['isdeleted'] = 'N'

                query_dict = QueryDict('', mutable=True)
                query_dict.update(temp_pros_dict)
                print(temp_pros_dict)

                serializer = ReviewprosSerializer(data=query_dict)
                if serializer.is_valid():
                    serializer.save()
            # 문자열 ->
            tmp = cons_list_dict['cons'][1:-1]
            new_list = tmp.split(',')

            for cons in new_list:

                temp_cons_dict = {}
                temp_cons_dict['cons'] = cons
                temp_cons_dict['review'] = reviewIdx
                temp_cons_dict['isdeleted'] = 'N'

                query_dict = QueryDict('', mutable=True)
                query_dict.update(temp_cons_dict)


                serializer = ReviewconsSerializer(data=query_dict)
                if serializer.is_valid():
                    serializer.save()

            post_review = {}
            post_review['isSuccess'] = 'true'
            post_review['code'] = 201
            post_review['message'] = '리뷰 작성 성공'

            return_value = json.dumps(post_review, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_201_CREATED)

    except Exception:
        return for_exception()



@api_view(['PUT', 'DELETE'])
@login_decorator
def review_detail(request, pk, reviewIdx):
    try:
        #jwt를 통해 얻어낸 정보
        userIdx = request.user.userinfo.useridx
        review_item = Review.objects.get(pk=reviewIdx)
        writerIdx = review_item.profile.userinfo.useridx

        if userIdx != writerIdx:
            return JsonResponse({'isSuccess': 'false',
                                 'code': 400,
                                 'message': '본인의 리뷰만 수정/삭제할 수 있습니다.'}, status=400)

        pros_item = Reviewpros.objects.filter(review=reviewIdx, isdeleted='N')
        cons_item = Reviewcons.objects.filter(review=reviewIdx, isdeleted='N')

        if request.method == 'PUT':

            review_dict = QueryDict.dict(request.data)
            pros_list_dict = {}
            pros_list_dict['pros'] = review_dict['pros']
            # 단점
            cons_list_dict = {}
            cons_list_dict['cons'] = review_dict['cons']
            del review_dict['pros']
            del review_dict['cons']

            if 'improvement' not in review_dict:
                review_dict['improvement'] = ""

            # 리뷰 테이블에 수정사항 반영
            reviewQuery = QueryDict('', mutable=True)
            reviewQuery.update(review_dict)
            serializer = ReviewSerializer(review_item, data=reviewQuery, partial=True)

            if serializer.is_valid():
                serializer.save(isblocked='N')

            # 기존의 장단점 삭제
            delete(pros_item, ReviewprosSerializer)
            delete(cons_item, ReviewconsSerializer)

            # 장단점 새로 넣기
            for pros in pros_list_dict['pros']:
                temp_pros_dict = {}
                temp_pros_dict['pros'] = pros
                temp_pros_dict['review'] = reviewIdx
                temp_pros_dict['isdeleted'] = 'N'

                query_dict = QueryDict('', mutable=True)
                query_dict.update(temp_pros_dict)
                print(query_dict)

                serializer = ReviewprosSerializer(data=query_dict)
                if serializer.is_valid():
                    serializer.save()

            for cons in cons_list_dict['cons']:
                temp_cons_dict = {}
                temp_cons_dict['cons'] = cons
                temp_cons_dict['review'] = reviewIdx
                temp_cons_dict['isdeleted'] = 'N'

                query_dict = QueryDict('', mutable=True)
                query_dict.update(temp_cons_dict)
                print(temp_cons_dict)

                serializer = ReviewconsSerializer(data=query_dict)
                if serializer.is_valid():
                    serializer.save()

            put_review = {}
            put_review['isSuccess'] = 'true'
            put_review['code'] = 200
            put_review['message'] = '리뷰 수정 성공'

            return_value = json.dumps(put_review, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered",
                                status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            # 내가 쓴 글 일때만 삭제 가능 -> 토큰에 해당하는 useridx랑 글 idx 비교하기, qna의 모든 답글, 이미지도 동시에 삭제되어야함
            item = {}
            item['isdeleted'] = 'Y'
            itemQuery = QueryDict('', mutable=True)
            itemQuery.update(item)
            serializer = ReviewSerializer(review_item, data=itemQuery, partial=True)

            if serializer.is_valid():
                serializer.save()

                # pros cons 삭제
                delete(pros_item, ReviewprosSerializer)
                delete(cons_item, ReviewconsSerializer)

            del_comment = {}
            del_comment['isSuccess'] = 'true'
            del_comment['code'] = 200
            del_comment['message'] = '리뷰 삭제 성공'

            return_value = json.dumps(del_comment, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered",
                                status=status.HTTP_400_BAD_REQUEST)

    except Exception:

        return for_exception()


@api_view(['GET','POST'])
def qna_list(request, pk):
    try:
        if request.method == 'POST':
            # qna 저장
            expire_check(request.headers.get('Authorization', None))
            try:

                access_token = request.headers.get('Authorization', None)
                payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')

                user = Profile.objects.get(email=payload['email'])
                request.user = user
            except jwt.exceptions.DecodeError:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': 'INVALID_TOKEN'}, status=400)

            except Profile.DoesNotExist:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': 'INVALID_USER'}, status=400)

            a = Qna.objects.last()
            qnaIdx = a.qnaidx + 1
            userIdx = request.user.userinfo.useridx

            qna_dict = QueryDict.dict(request.data)
            images = QueryDict.dict(request.data)

            qna_dict['lecture'] = pk
            qna_dict['userinfo'] = userIdx
            if 'image' in qna_dict:
                del qna_dict['image']
                print(qna_dict)
            query_dict = QueryDict('', mutable=True)
            query_dict.update(qna_dict)

            serializer = QnaSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save(isblocked='N', isdeleted='N')
            else:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': '제목/내용은 반드시 입력해야 합니다'}, status=400)

            # 댓글첨부된 이미지 저장
            if 'image' in images:
                for i in range(len(images['image'])):

                    qna_image_dict = {}
                    qna_image_dict['imgurl'] = images['image'][i]
                    qna_image_dict['qna'] = qnaIdx
                    qna_image_dict['isdeleted'] = 'N'

                    query_dict = QueryDict('', mutable=True)
                    query_dict.update(qna_image_dict)
                    print(query_dict)

                    serializer = QnaimageSerializer(data=query_dict)
                    if serializer.is_valid():
                        serializer.save()

            post_comment = {}
            post_comment['isSuccess'] = 'true'
            post_comment['code'] = 201
            post_comment['message'] = 'qna 작성 성공'

            return_value = json.dumps(post_comment, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_201_CREATED)

        elif request.method == 'GET':
            page = int(request.GET.get('page', '1'))

            qna_list = []
            qna_dict = {}
            qna_dict['isSuccess'] = 'true'
            qna_dict['code'] = 200
            qna_dict['message'] = 'qna 목록 조회 성공'

            qna = Qna.objects.filter(lecture__lectureidx=pk, isblocked='N', isdeleted='N').select_related('userinfo',
                                                                                                          'lecture')[
                  page * 5 - 5:page * 5]

            likes = Likesforqna.objects.filter(qna__lecture__lectureidx=pk).select_related('qna').values(
                'qna').annotate(count=Count('qna'))
            likes_dict = {}

            for i in likes:
                likes_dict[i['qna']] = i['count']

            for r in qna:
                try:
                    likes_count = likes_dict[r.qnaidx]
                except Exception:
                    likes_count = 0
                    pass
                #시간 변환
                time = convert_time(r.createdat)

                qna_list.append(dict(
                    [('qnaIdx', r.qnaidx), ('qnaTitle', r.title), ('qnaDes', r.qnades),
                     ('profileImg', r.userinfo.profileimg),
                     ('likesCount', likes_count), ('createdAt',time )
                     ]))

            qna_dict['result'] = qna_list

            return_value = json.dumps(qna_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Exception:
        return for_exception()


@api_view(['GET','PUT', 'DELETE'])
def qna_detail(request, pk, qnaIdx):
    try:
        if request.method == 'GET':
            item = Qna.objects.select_related('userinfo').get(pk=qnaIdx)

            qnaimages = Qnaimage.objects.filter(qna=qnaIdx).values('imgurl')
            qna_image = []
            qna_detail_dict = {}
            qna_detail_dict['isSuccess'] = 'true'
            qna_detail_dict['code'] = 200
            qna_detail_dict['message'] = 'qna 상세 정보 조회 성공'

            for i in qnaimages:
                qna_image.append(i['imgurl'])

            print(item.qnaidx, item.title, item.qnades, item.userinfo.profileimg, item.userinfo.nickname,
                  item.createdat)

            # 시간 변환
            time = convert_time(item.createdat)

            qna_detail_dict['result'] = (dict(
                [('qnaIdx', item.qnaidx), ('qnaTitle', item.title), ('qnaDes', item.qnades),
                 ('profileImg', item.userinfo.profileimg),
                 ('nickname', item.userinfo.nickname), ('image', qna_image), ('createAt',time)]))

            return_value = json.dumps(qna_detail_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


        else:

            try:
                expire_check(request.headers.get('Authorization', None))
                access_token = request.headers.get('Authorization', None)
                payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')

                user = Profile.objects.get(email=payload['email'])
                request.user = user

            except jwt.exceptions.DecodeError:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': 'INVALID_TOKEN'}, status=400)

            except Profile.DoesNotExist:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': 'INVALID_USER'}, status=400)

            userIdx = request.user.userinfo.useridx
            qna_item = Qna.objects.get(pk=qnaIdx)
            writerIdx = qna_item.userinfo.useridx
            if userIdx != writerIdx:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': '본인의 qna만 수정/삭제할 수 있습니다.'}, status=400)

            qna_image_item = Qnaimage.objects.filter(qna=qnaIdx, isdeleted='N')

            if request.method == 'PUT':


                qna_dict = QueryDict.dict(request.data)
                images = QueryDict.dict(request.data)
                if 'image' in qna_dict:  # 사진도 수정을 원할 경우
                    # 사진 지우고 사진은 따로 삭제후 저장
                    del qna_dict['image']

                    # comment image 값 차례로 삭제

                    delete(qna_image_item, QnaimageSerializer)

                    for i in range(len(images['image'])):
                        qna_image_dict = {}
                        qna_image_dict['imgurl'] = images['image'][i]
                        qna_image_dict['qna'] = qnaIdx
                        qna_image_dict['isdeleted'] = 'N'

                        # 새로운 값 차례로 넣기
                        query_dict = QueryDict('', mutable=True)
                        query_dict.update(qna_image_dict)
                        serializer = QnaimageSerializer(data=query_dict)
                        if serializer.is_valid():
                            serializer.save()

                qnaQuery = QueryDict('', mutable=True)
                qnaQuery.update(qna_dict)
                serializer = QnaSerializer(qna_item, data=qnaQuery, partial=True)

                if serializer.is_valid():
                    serializer.save()

                put_comment = {}
                put_comment['isSuccess'] = 'true'
                put_comment['code'] = 200
                put_comment['message'] = 'qna 수정 성공'

                return_value = json.dumps(put_comment, indent=4, use_decimal=True, ensure_ascii=False)

                return HttpResponse(return_value, content_type="text/json-comment-filtered",
                                    status=status.HTTP_400_BAD_REQUEST)


            elif request.method == 'DELETE':

                # 내가 쓴 글 일때만 삭제 가능 -> 토큰에 해당하는 useridx랑 글 idx 비교하기, qna의 모든 답글, 이미지도 동시에 삭제되어야함

                item = {}
                item['isdeleted'] = 'Y'
                itemQuery = QueryDict('', mutable=True)
                itemQuery.update(item)

                serializer = QnaSerializer(qna_item, data=itemQuery, partial=True)
                # qna의 댓글 삭제
                if serializer.is_valid():
                    serializer.save()
                    # qna image 값 차례로 삭제
                    delete(qna_image_item, QnaimageSerializer)

                comments = Comment.objects.filter(qna=pk)

                images = Commentimage.objects.filter(isdeleted='N', comment__qna=qnaIdx)

                for ele in comments:

                    item = {}
                    item['isdeleted'] = 'Y'
                    itemQuery = QueryDict('', mutable=True)
                    itemQuery.update(item)
                    serializer = CommentSerializer(ele, data=itemQuery, partial=True)

                    if serializer.is_valid():
                        serializer.save()

                        # comment image 값 차례로 삭제

                        images_per_comment = images.filter(comment=ele.commentidx)
                        delete(images_per_comment, CommentimageSerializer)

                del_qna = {}
                del_qna['isSuccess'] = 'true'
                del_qna['code'] = 200
                del_qna['message'] = 'qna 삭제 성공'

                return_value = json.dumps(del_qna, indent=4, use_decimal=True, ensure_ascii=False)

                return HttpResponse(return_value, content_type="text/json-comment-filtered",

                                    status=status.HTTP_400_BAD_REQUEST)

    except Qna.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return for_exception()


@api_view(['GET', 'POST'])
def comment_list(request, pk, qnaIdx):
    try:
        if request.method == 'GET':

            comment = Comment.objects.filter(qna=qnaIdx, parentidx__isnull=True, isdeleted='N',
                                             isblocked='N').select_related('userinfo')
            reply = Comment.objects.filter(qna=qnaIdx, parentidx__isnull=False, isdeleted='N', isblocked='N')
            type = reply.values('parentidx').annotate(count=Count('parentidx'))

            # qna 글을 참조하는 모든 사진 불러오기
            images = Commentimage.objects.filter(comment__qna__qnaidx=qnaIdx, isdeleted='N')

            parent_list = []
            comment_dict = {}

            comment_dict['isSuccess'] = 'true'
            comment_dict['code'] = 200
            comment_dict['message'] = '댓글 리스트 조회 성공'
            comments_list = []

            for i in type:
                parent_list.append(i['parentidx'])

            for i in reply:
                print(i.commentidx, i.parentidx)

            for i in comment:
                image_list = []
                reply_list = []
                images2 = images.filter(comment=i.commentidx).values('imageurl')
                for j in images2:
                    image_list.append(j['imageurl'])

                # 시간 변환
                time = convert_time(i.createdat)

                if i.commentidx in parent_list:
                    children = reply.filter(parentidx=i.commentidx)
                    for child in children:
                        reply_image_list = []
                        images3 = images.filter(comment=child.commentidx).values('imageurl')
                        for h in images3:
                            reply_image_list.append(h['imageurl'])
                        # 시간 변환
                        child_time = convert_time(child.createdat)
                        reply_list.append(dict([('commentIdx', child.commentidx), ('commentDes', child.commentdes),
                                                ('nickname', child.userinfo.nickname), ('image', reply_image_list),('createdAt',child_time)]))

                comments_list.append(dict(
                    [('commentIdx', i.commentidx), ('commentDes', i.commentdes), ('nickname', i.userinfo.nickname),
                     ('image', image_list), ('reply', reply_list),('createdAt',time)]))

                comment_dict['result'] = comments_list

            return_value = json.dumps(comment_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        elif request.method == 'POST':
            # 댓글 저장
            try:
                expire_check(request.headers.get('Authorization', None))

                access_token = request.headers.get('Authorization', None)
                payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')

                user = Profile.objects.get(email=payload['email'])
                request.user = user

            except jwt.exceptions.DecodeError:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': 'INVALID_TOKEN'}, status=400)

            except Profile.DoesNotExist:
                return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': 'INVALID_USER'}, status=400)

            a = Comment.objects.last()
            commentIdx = a.commentidx + 1
            userIdx = request.user.userinfo.useridx
            comment_dict = QueryDict.dict(request.data)
            images = QueryDict.dict(request.data)
            print(comment_dict)
            comment_dict['qna'] = qnaIdx
            comment_dict['userinfo'] = userIdx
            if 'image' in comment_dict:
                del comment_dict['image']
                print(comment_dict)
            query_dict = QueryDict('', mutable=True)
            query_dict.update(comment_dict)
            serializer = CommentSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save(isblocked='N', isdeleted='N')

            # 댓글첨부된 이미지 저장
            if 'image' in images:
                for i in range(len(images['image'])):

                    comment_image_dict = {}
                    comment_image_dict['imageurl'] = images['image'][i]
                    comment_image_dict['comment'] = commentIdx
                    comment_image_dict['isdeleted'] = 'N'
                    print(comment_image_dict)
                    query_dict = QueryDict('', mutable=True)
                    query_dict.update(comment_image_dict)
                    print(query_dict)

                    serializer = CommentimageSerializer(data=query_dict)
                    if serializer.is_valid():
                        serializer.save()

            post_comment = {}
            post_comment['isSuccess'] = 'true'
            post_comment['code'] = 201
            post_comment['message'] = '댓글 작성 성공'

            return_value = json.dumps(post_comment, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_201_CREATED)



    except Qna.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return for_exception()


@api_view(['PUT', 'DELETE'])
@login_decorator
def comment_detail(request, pk, qnaIdx, commentIdx):
    try:
        userIdx = request.user.userinfo.useridx
        comment_item = Comment.objects.get(pk=commentIdx)

        if userIdx != comment_item.userinfo.useridx:
            return JsonResponse({'isSuccess': 'false',
                                     'code': 400,
                                     'message': '자신의 댓글만 수정/삭제 가능합니다'}, status=400)

        comment_image_item = Commentimage.objects.filter(comment=commentIdx, isdeleted='N')
        print(comment_item)

        if request.method == 'PUT':
            comment_dict = QueryDict.dict(request.data)
            images = QueryDict.dict(request.data)
            if 'image' in comment_dict:  # 사진도 수정을 원할 경우
                # 사진 지우고 사진은 따로 삭제후 저장
                del comment_dict['image']

                # comment image 값 차례로 삭제
                delete(comment_image_item, CommentimageSerializer)

                for i in range(len(images['image'])):
                    comment_image_dict = {}
                    comment_image_dict['imageurl'] = images['image'][i]
                    comment_image_dict['comment'] = commentIdx
                    comment_image_dict['isdeleted'] = 'N'

                    # 새로운 값 차례로 넣기
                    query_dict = QueryDict('', mutable=True)
                    query_dict.update(comment_image_dict)

                    serializer = CommentimageSerializer(data=query_dict)
                    if serializer.is_valid():
                        serializer.save()

            commentQuery = QueryDict('', mutable=True)
            commentQuery.update(comment_dict)
            serializer = CommentSerializer(comment_item, data=commentQuery, partial=True)

            if serializer.is_valid():
                serializer.save()

            put_comment = {}
            put_comment['isSuccess'] = 'true'
            put_comment['code'] = 200
            put_comment['message'] = '댓글 수정 성공'

            return_value = json.dumps(put_comment, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered",
                                status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            # 내가 쓴 글 일때만 삭제 가능 -> 토큰에 해당하는 useridx랑 글 idx 비교하기, qna의 모든 답글, 이미지도 동시에 삭제되어야함
            item = {}
            item['isdeleted'] = 'Y'
            itemQuery = QueryDict('', mutable=True)
            itemQuery.update(item)
            serializer = CommentSerializer(comment_item, data=itemQuery, partial=True)

            if serializer.is_valid():
                serializer.save()

                # comment image 값 차례로 삭제
                delete(comment_image_item, CommentimageSerializer)

            del_comment = {}
            del_comment['isSuccess'] = 'true'
            del_comment['code'] = 200
            del_comment['message'] = '댓글 삭제 성공'

            return_value = json.dumps(del_comment, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered",
                                status=status.HTTP_400_BAD_REQUEST)

    except Exception:

        return for_exception()


@api_view(['GET', 'PATCH'])
@login_decorator
def favorite_sites(request):
    try:
        if request.method == 'GET':
            userIdx = request.user.userinfo.useridx
            favorite_sites = Favoritesite.objects.filter(user=userIdx, isdeleted='N')
            favsites_list = []

            for i in favorite_sites:

                favsites_list.append(
                    dict([('siteIdx', i.siteinfo.siteidx), ('siteName', i.siteinfo.sitename)]))

            favsite_dict={}
            favsite_dict['isSuccess'] = 'true'
            favsite_dict['code'] = 200
            favsite_dict['message'] = '즐겨찾기한 사이트 조회 성공'
            favsite_dict['result'] = favsites_list

            return_value = json.dumps(favsite_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            userIdx = request.user.userinfo.useridx
            siteIdx = int(request.GET.get('siteIdx'))
            favsite = Favoritesite.objects.filter(user=userIdx, siteinfo__siteidx=siteIdx)
            favsite_dict = {}
            if favsite.exists():

                if favsite.filter(isdeleted='N'):  # 이미 즐겨찾기함 -> 즐겨찾기 해제
                    favsite_dict['isdeleted'] ='Y'

                else:  # 즐겨찾기 해제(기록 O) -> 즐겨찾기 추가
                    favsite_dict['isdeleted'] ='N'

                favsiteQuery = QueryDict('', mutable=True)
                favsiteQuery.update(favsite_dict)
                serializer = FavoritesiteSerializer(favsite[0], data=favsiteQuery, partial=True)
                if serializer.is_valid():
                    serializer.save()

            else:

                favsite_dict['user'] = userIdx
                favsite_dict['siteinfo'] = siteIdx
                favsite_dict['isdeleted'] ='N'
                favsiteQuery = QueryDict('', mutable=True)
                favsiteQuery.update(favsite_dict)
                print(favsiteQuery)

                serializer = FavoritesiteSerializer(data=favsiteQuery)

                if serializer.is_valid():
                    serializer.save()

            favlec_dict = {}
            favlec_dict['isSuccess'] = 'true'
            favlec_dict['code'] = 200
            favlec_dict['message'] = '사이트 즐겨찾기 여부 변경'

            return_value = json.dumps(favlec_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)



    except Favoritesite.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return for_exception()


@api_view(['GET', 'PATCH'])
@login_decorator
def favorite_lectures(request):
    try:
        userIdx = request.user.userinfo.useridx

        if request.method == 'GET':
            page = int(request.GET.get('page', '1'))
            if page <= 0:
                page = 1
            favlectures_list=[]
            fav_lectures = Favoritelecture.objects.filter(user=userIdx, isdeleted='N')[page * 5 - 5:page * 5]
            for i in fav_lectures:
                price_sql = i.lecture.price
                if price_sql == 0:
                    price_sql = 'free'
                elif price_sql == -1:
                    price_sql = 'membership'
                else:
                    price_sql = format(price_sql,',')

                favlectures_list.append(
                    dict([('lectureIdx', i.lecture.lectureidx), ('lectureName', i.lecture.lecturename), ('price', price_sql),('level',i.lecture.level.levelname),
                          ('rating',i.lecture.rating),('thumbUrl',i.lecture.thumburl),('siteName',i.lecture.siteinfo.siteidx),('professor',i.lecture.lecturer)]))


            favlecture_dict={}
            favlecture_dict['isSuccess'] = 'true'
            favlecture_dict['code'] = 200
            favlecture_dict['message'] = '즐겨찾기한 강의 조회 성공'
            favlecture_dict['result'] = favlectures_list

            return_value = json.dumps(favlecture_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        elif request.method == 'PATCH':

            lectureIdx = int(request.GET.get('lectureIdx'))
            favlectures = Favoritelecture.objects.filter(user=userIdx, lecture=lectureIdx)
            favlectures_dict = {}

            if favlectures.exists():

                if favlectures.filter(isdeleted='N'):  # 이미 즐겨찾기함 -> 즐겨찾기 해제
                    favlectures_dict['isdeleted'] ='Y'

                else:  # 즐겨찾기 해제(기록 O) -> 즐겨찾기 추가
                    favlectures_dict['isdeleted'] ='N'

                favlectureQuery = QueryDict('', mutable=True)
                favlectureQuery.update(favlectures_dict)
                print(favlectureQuery)
                serializer = FavoritelectureSerializer(favlectures[0], data=favlectureQuery, partial=True)

                if serializer.is_valid():
                    serializer.save()

            else:
                favlectures_dict['user'] = userIdx
                favlectures_dict['lecture'] = lectureIdx
                favlectures_dict['isdeleted'] ='N'
                favlectureQuery = QueryDict('', mutable=True)
                favlectureQuery.update(favlectures_dict)
                print(favlectureQuery)

                serializer = FavoritelectureSerializer(data=favlectureQuery)
                if serializer.is_valid():
                    serializer.save()

            favlec_dict = {}
            favlec_dict['isSuccess'] = 'true'
            favlec_dict['code'] = 200
            favlec_dict['message'] = '강의 즐겨찾기 여부 변경'

            return_value = json.dumps(favlec_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

    except Favoritelecture.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return for_exception()


@api_view(['GET'])
@login_decorator
def my_reviews(request):
    try:
        userIdx = request.user.userinfo.useridx
        page = int(request.GET.get('page', '1'))
        if page <= 0:
            page = 1


        my_review_list=[]
        my_review = Review.objects.filter(profile__userinfo__useridx=userIdx, isdeleted='N')[page * 5 - 5:page * 5]

        pros = Reviewpros.objects.filter(review__profile__userinfo__useridx=userIdx, isdeleted='N')

        cons = Reviewcons.objects.filter(review__profile__userinfo__useridx=userIdx, isdeleted='N')

        likes = Likesforreview.objects.filter(review__profile__userinfo__useridx=userIdx).values('review').annotate(count=Count('review'))

        for i in my_review:

            likes_dict = {}

            #내가 쓴 리뷰 중 하나의 리뷰라도 좋아요를 받았을 경우
            for k in likes:
                likes_dict[k['review']] = k['count']


            try:
                likes_count = likes_dict[i.reviewidx]
            except Exception:
                likes_count = 0


            pros2 = pros.filter(review__reviewidx=i.reviewidx)
            pros_list = []
            cons2 = cons.filter(review__reviewidx=i.reviewidx)
            cons_list = []

            for p in pros2:
                pros_list.append(p.pros.prostype)

            for c in cons2:
                cons_list.append(c.cons.constype)


            my_review_list.append(
                dict([('reviewIdx', i.reviewidx),('lectureIdx',i.lectureidx.lectureidx),('lectureName',i.lectureidx.lecturename), ('totalRating', i.totalrating), ('priceRating', i.pricerating),
                      ('teachingpowerRating',i.teachingpowerrating),('recommend',i.recommend),('improvement',i.improvement),
                      ('pros',pros_list),('cons',cons_list), ('likesCount', likes_count)]))


        my_review_dict={}
        my_review_dict['isSuccess'] = 'true'
        my_review_dict['code'] = 200
        my_review_dict['message'] = '내가 쓴 리뷰 조회 성공'
        my_review_dict['result'] = my_review_list

        return_value = json.dumps(my_review_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return for_exception()


@api_view(['GET'])
@login_decorator
def my_qnas(request):
    try:
        userIdx = request.user.userinfo.useridx
        page = int(request.GET.get('page', '1'))
        if page <= 0:
            page = 1


        my_qna_list=[]
        my_qna = Qna.objects.filter(userinfo=userIdx, isdeleted='N', isblocked='N')[page * 5 - 5:page * 5]

        likes = Likesforqna.objects.filter(qna__userinfo=userIdx).values('qna').annotate(count=Count('qna'))

        for i in my_qna:

            likes_dict = {}

            for k in likes:
                likes_dict[k['qna']] = k['count']

                try:
                    likes_count = likes_dict[i.qnaidx]
                except Exception:
                    likes_count = 0
                    pass


            my_qna_list.append(
                dict([('qnaIdx', i.qnaidx),('qnaTitle',i.title),('qnaDes',i.qnades),('likesCount', likes_count)]))


        my_qna_dict={}
        my_qna_dict['isSuccess'] = 'true'
        my_qna_dict['code'] = 200
        my_qna_dict['message'] = '내가 쓴 리뷰 조회 성공'
        my_qna_dict['result'] = my_qna_list

        return_value = json.dumps(my_qna_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return for_exception()

@api_view(['GET'])
@login_decorator
def my_qnas(request):
    try:
        userIdx = request.user.userinfo.useridx

        page = int(request.GET.get('page', '1'))
        if page <= 0:
            page = 1


        my_qna_list=[]
        my_qna = Qna.objects.filter(userinfo=userIdx, isdeleted='N', isblocked='N')[page * 5 - 5:page * 5]

        likes = Likesforqna.objects.filter(qna__userinfo=userIdx).values('qna').annotate(count=Count('qna'))

        for i in my_qna:

            likes_dict = {}

            for k in likes:
                likes_dict[k['qna']] = k['count']

                try:
                    likes_count = likes_dict[i.qnaidx]
                except Exception:
                    likes_count = 0
                    pass


            my_qna_list.append(
                dict([('qnaIdx', i.qnaidx),('qnaTitle',i.title),('qnaDes',i.qnades),('likesCount', likes_count)]))


        my_qna_dict={}
        my_qna_dict['isSuccess'] = 'true'
        my_qna_dict['code'] = 200
        my_qna_dict['message'] = '내가 쓴 리뷰 조회 성공'
        my_qna_dict['result'] = my_qna_list

        return_value = json.dumps(my_qna_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return for_exception()


@api_view(['GET'])
@login_decorator
def my_qnas(request):
    try:

        userIdx = request.user.userinfo.useridx

        page = int(request.GET.get('page', '1'))
        if page <= 0:
            page = 1


        my_qna_list=[]
        my_qna = Qna.objects.filter(userinfo=userIdx, isdeleted='N', isblocked='N')[page * 5 - 5:page * 5]

        likes = Likesforqna.objects.filter(qna__userinfo=userIdx).values('qna').annotate(count=Count('qna'))

        for i in my_qna:

            likes_dict = {}

            for k in likes:
                likes_dict[k['qna']] = k['count']

                try:
                    likes_count = likes_dict[i.qnaidx]
                except Exception:
                    likes_count = 0
                    pass


            my_qna_list.append(
                dict([('qnaIdx', i.qnaidx),('qnaTitle',i.title),('qnaDes',i.qnades),('likesCount', likes_count)]))


        my_qna_dict={}
        my_qna_dict['isSuccess'] = 'true'
        my_qna_dict['code'] = 200
        my_qna_dict['message'] = '내가 쓴 리뷰 조회 성공'
        my_qna_dict['result'] = my_qna_list

        return_value = json.dumps(my_qna_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return for_exception()


@api_view(['GET'])
@login_decorator
def my_comments(request):
    try:
        userIdx = request.user.userinfo.useridx
        page = int(request.GET.get('page', '1'))
        if page <= 0:
            page = 1


        my_comment_list=[]
        my_comment = Comment.objects.filter(userinfo=userIdx, isdeleted='N', isblocked='N', qna__isdeleted='N', qna__isblocked='N').values(
            'qna__qnaidx', 'qna__title', 'qna__qnades','qna__userinfo__nickname','qna__userinfo__profileimg').distinct()[page * 5 - 5:page * 5]

        qnas = []
        for i in my_comment:
            qnas.append(i['qna__qnaidx'])

        likes = Likesforqna.objects.filter(isdeleted='N',qna__in=qnas).values('qna').annotate(count=Count('qna'))

        for i in my_comment:

            likes_dict = {}

            for k in likes:
                likes_dict[k['qna']] = k['count']

                try:
                    likes_count = likes_dict[i['qna__qnaidx']]
                except Exception:
                    likes_count = 0
                    pass


            my_comment_list.append(
                dict([('qnaIdx', i['qna__qnaidx']),('qnaTitle',i['qna__title']),('qnaDes',i['qna__qnades']),('nickname',i['qna__userinfo__nickname']),
                      ('profileImg',i['qna__userinfo__profileimg']),('likes',likes_count)]))


        my_qna_dict={}
        my_qna_dict['isSuccess'] = 'true'
        my_qna_dict['code'] = 200
        my_qna_dict['message'] = '댓글 쓴 글 조회 성공'
        my_qna_dict['result'] = my_comment_list

        return_value = json.dumps(my_qna_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return for_exception()



@api_view(['GET'])
def category_list(request):
    try:
        cate =[]
        categoryList = Category.objects.all()


        for i in categoryList:
            cate.append(dict([('categoryIdx', i.categoryidx),('categoryName', i.categoryname)]))

        my_qna2_dict={}
        my_qna2_dict['isSuccess'] = 'true'
        my_qna2_dict['code'] = 200
        my_qna2_dict['message'] = '카테고리 리스트 조회 성공'
        my_qna2_dict['result'] = categoryList

        return JsonResponse({'isSuccess': 'true',
                             'code': 200,
                             'message': '카테고리 리스트 조회 성공',
                             'result': cate}, status=200)



    except Exception:
        return for_exception()















