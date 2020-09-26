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
    Likesforreview, Qna, Likesforqna, Qnaimage, Comment, Commentimage, Pros
from rest_framework import viewsets, status
from .serializers import LectureSerializer, CategorySerializer, QnaSerializer, CommentSerializer, \
    CommentimageSerializer, QnaimageSerializer, ReviewSerializer, ReviewprosSerializer, ReviewconsSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    authentication_classes = (TokenAuthentication,)  # 기본적으로는 하나의 Auth를 이용하는데 추가할 수 있음
    permission_classes = (IsAuthenticated,)  # 이 함수는 authentication이 필요


# 이미지 삭제 함수(comment or qna)
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
            selected_level = float(request.GET.get('level', '0'))
            selected_price = int(request.GET.get('price', '0'))
            selected_rating = float(request.GET.get('rating', '0'))
            page = int(request.GET.get('page', '1'))
            if page <= 0:
                page = 1

            # 잘못된 파라미터 값이 들어왔을 경우
            if selected_level < 0 or selected_level > 5 or selected_rating < 0 or selected_rating > 5 or selected_price < 0:
                raise Exception

            # 쿼리문
            lectures = Lecture.objects.filter(
                level__gte=selected_level, rating__gte=selected_rating, price__lte=selected_price).select_related(
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

                info.append(
                    dict([('lectureIdx', lec.lectureidx), ('lectureName', lec.lecturename), ('professor', lec.lecturer),
                          ('price', price_sql), ('level', lec.level), ('rating', lec.rating),
                          ('thumbUrl', lec.thumburl), ('siteName', h)]))

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
                                                                  subcategoryidx=subcategoryIdx).select_related(
                    'lecture').order_by('-lecture__rating')
            else:
                # 카테고리만 골랐을 경우,
                category_ranking = Lecturecategory.objects.filter(categoryidx=categoryIdx).select_related(
                    'lecture').order_by('-lecture__rating')

            category_ranking_all = category_ranking.values('lecture__lectureidx', 'lecture__lecturename',
                                                           'lecture__lecturer', 'lecture__thumburl', 'lecture__price',
                                                           'lecture__level', 'lecture__siteinfo__sitename').distinct()[
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
                rank.append(
                    dict([('lectureIdx', c['lecture__lectureidx']), ('lectureName', c['lecture__lecturename']),
                          ('professor', c['lecture__lecturer']),
                          ('price', price_sql), ('level', c['lecture__level']), ('thumbUrl', c['lecture__thumburl']),
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

        detail_dict['result'] = dict([('lectureIdx', lecture.lectureidx), ('lectureName', lecture.lecturename),
                                      ('lectureLink', lecture.lecturelink),
                                      ('price', price_sql), ('level', lecture.level), ('rating', lecture.rating)])

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

            likes = Likesforreview.objects.filter(review__lectureidx=pk).select_related('review').values('review').annotate(
                count=Count('review'))

            likes_dict = {}

            for i in likes:
                likes_dict[i['review']] = i['count']

            major = {'Y': '전공자', 'N': '비전공자'}
            job = {'S': '학생', 'D': '개발자', 'N': '비개발 직군'}

            print(len(review_userinfo))
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
                     ('job', job[r.profile.job]), ('major', major[r.profile.major]), ('reviewidx', r.reviewidx),
                     ('totalRating', r.totalrating),
                     ('priceRating', r.pricerating), ('teachingpowerRating', r.teachingpowerrating),
                     ('recommend', r.recommend), ('improvement', r.improvement),
                     ('likesCount', likes_count), ('pros', pros_list), ('cons', cons_list)
                     ]))

            review_dict['result'] = review_list
            return_value = json.dumps(review_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        elif request.method == 'POST':
            # 리뷰 저장
            a = Review.objects.last()
            reviewIdx = a.reviewidx + 1
            # 리뷰
            review_dict = QueryDict.dict(request.data)
            # 장점
            pros_list_dict = {}
            pros_list_dict['pros'] = review_dict['pros']
            # 단점
            cons_list_dict ={}
            cons_list_dict['cons'] = review_dict['cons']

            review_dict['profile'] = 1 # 나중에 writer 확인하는 로직 작성 시 변경
            review_dict['lectureidx'] = pk
            review_dict['isdeleted'] = 'N'
            del review_dict['pros']
            del review_dict['cons']

            query_dict = QueryDict('', mutable=True)
            query_dict.update(review_dict)

            serializer = ReviewSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save()

            for pros in pros_list_dict['pros']:
                temp_pros_dict = {}
                temp_pros_dict['pros'] = pros
                temp_pros_dict['review'] = reviewIdx
                temp_pros_dict['isdeleted'] ='N'

                query_dict = QueryDict('', mutable=True)
                query_dict.update(temp_pros_dict)
                print(temp_pros_dict)

                serializer = ReviewprosSerializer(data=query_dict)
                if serializer.is_valid():
                    serializer.save()


            for cons in cons_list_dict['cons']:
                temp_cons_dict = {}
                temp_cons_dict['cons'] = cons
                temp_cons_dict['review'] = reviewIdx
                temp_cons_dict['isdeleted'] ='N'

                query_dict = QueryDict('', mutable=True)
                query_dict.update(temp_cons_dict)
                print(temp_cons_dict)

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
def review_detail(request, pk, reviewIdx):
    try:

        review_item = Review.objects.get(pk=reviewIdx)
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
                review_dict['improvement']=""

            # 리뷰 테이블에 수정사항 반영
            reviewQuery = QueryDict('', mutable=True)
            reviewQuery.update(review_dict)
            serializer = ReviewSerializer(review_item, data=reviewQuery, partial=True)

            if serializer.is_valid():
                serializer.save(isblocked='N')

            #기존의 장단점 삭제
            delete(pros_item, ReviewprosSerializer)
            delete(cons_item, ReviewconsSerializer)

            # 장단점 새로 넣기
            for pros in pros_list_dict['pros']:
                temp_pros_dict = {}
                temp_pros_dict['pros'] = pros
                temp_pros_dict['review'] = reviewIdx
                temp_pros_dict['isdeleted'] ='N'

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
                temp_cons_dict['isdeleted'] ='N'

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


@api_view(['GET', 'POST'])
def qna_list(request, pk):

    try:
        if request.method == 'GET':
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
                print(r.createdat)
                qna_list.append(dict(
                    [('qnaIdx', r.qnaidx), ('qnaTitle', r.title), ('qnaDes', r.qnades),
                     ('profileImg', r.userinfo.profileimg),
                     ('likesCount', likes_count)
                     ]))

            qna_dict['result'] = qna_list

            return_value = json.dumps(qna_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        elif request.method == 'POST':

            # qna 저장
            a = Qna.objects.last()
            qnaIdx = a.qnaidx + 1

            qna_dict = QueryDict.dict(request.data)
            images = QueryDict.dict(request.data)

            qna_dict['lecture'] = pk
            qna_dict['userinfo'] = 1  # 나중에 writer 확인하는 로직 작성 시 변경
            if 'image' in qna_dict:
                del qna_dict['image']
                print(qna_dict)
            query_dict = QueryDict('', mutable=True)
            query_dict.update(qna_dict)

            serializer = QnaSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save(isblocked='N', isdeleted='N')

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

    except Exception:
        return for_exception()


@api_view(['GET', 'PUT', 'DELETE'])
def qna_detail(request, pk, qnaIdx):
    try:
        qna_item = Qna.objects.get(pk=qnaIdx)
        qna_image_item = Qnaimage.objects.filter(qna=qnaIdx, isdeleted='N')

        if request.method == 'GET':
            item = Qna.objects.select_related('userinfo').get(pk=qnaIdx)
            qnaimages = Qnaimage.objects.filter(qnaidx=qnaIdx).values('imgurl')

            qna_image = []
            qna_detail_dict = {}
            qna_detail_dict['isSuccess'] = 'true'
            qna_detail_dict['code'] = 200
            qna_detail_dict['message'] = 'qna 상세 정보 조회 성공'

            for i in qnaimages:
                qna_image.append(i['imgurl'])

            print(item.qnaidx, item.title, item.qnades, item.userinfo.profileimg, item.userinfo.nickname,
                  item.createdat)

            qna_detail_dict['result'] = (dict(
                [('qnaIdx', item.qnaidx), ('qnaTitle', item.title), ('qnaDes', item.qnades),
                 ('profileImg', item.userinfo.profileimg),
                 ('nickname', item.userinfo.nickname), ('image', qna_image)]))

            return_value = json.dumps(qna_detail_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        elif request.method == 'PUT':

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
            #qna의 댓글 삭제
            if serializer.is_valid():
                serializer.save()
                # qna image 값 차례로 삭제
                delete(qna_image_item, QnaimageSerializer)


            comments =Comment.objects.filter(qna=pk)

            images = Commentimage.objects.filter(isdeleted='N',comment__qna=qnaIdx)


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

                if i.commentidx in parent_list:
                    children = reply.filter(parentidx=i.commentidx)
                    for child in children:
                        reply_image_list = []
                        images3 = images.filter(comment=child.commentidx).values('imageurl')
                        for h in images3:
                            reply_image_list.append(h['imageurl'])
                        reply_list.append(dict([('commentIdx', child.commentidx), ('commentDes', child.commentdes),
                                                ('nickname', child.userinfo.nickname), ('image', reply_image_list)]))

                comments_list.append(dict(
                    [('commentIdx', i.commentidx), ('commentDes', i.commentdes), ('nickname', i.userinfo.nickname),
                     ('image', image_list), ('reply', reply_list)]))

                comment_dict['result'] = comments_list

            return_value = json.dumps(comment_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        elif request.method == 'POST':
            # 댓글 저장
            a = Comment.objects.last()
            commentIdx = a.commentidx + 1

            comment_dict = QueryDict.dict(request.data)
            images = QueryDict.dict(request.data)
            print(comment_dict)
            comment_dict['qna'] = qnaIdx
            comment_dict['userinfo'] = 1  # 나중에 writer 확인하는 로직 작성 시 변경
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
def comment_detail(request, pk, qnaIdx, commentIdx):
    try:

        comment_item = Comment.objects.get(pk=commentIdx)
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
