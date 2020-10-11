import datetime
import time

import bcrypt
import jwt
import simplejson as json
from django.conf.global_settings import SECRET_KEY
from django.http import HttpResponse, QueryDict, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Profile, Userinfo

#생년월일에 대한 validation
from .serializers import ProfileSerializer, UserinfoSerializer, CategoryinterestSerializer, \
    SubcategoryinterestSerializer





def validateBirth(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("생일")

#비밀번호에 대한 validation
def validatePasswd(value):
    # check for digit

    if len(value) < 8:
        raise ValueError("비번설정")
    if not any(char.isdigit() for char in value):
        raise ValueError

    if not any(char.isalpha() for char in value):
        raise ValueError("비번설정")

    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if not any(char in special_characters for char in value):
        raise ValueError("비번설정")


# 이메일에 대한 validation
def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
       return False

# 예외 처리 함수 (파라미터 입력값 오류)
def for_exception(code = 400, message = '파라미터 값 오류', status_=400):
    lec_dict = {}
    lec_dict['isSuccess'] = 'false'
    lec_dict['code'] = code
    lec_dict['message'] = message

    return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

    return HttpResponse(return_value, content_type="text/json-comment-filtered",
                        status=status_)

@api_view(['POST'])
def check_email(request):
    code = 400
    message ='파라미터 입력 오류'
    status_ = status.HTTP_400_BAD_REQUEST

    try:
        sign_up_dict = QueryDict.dict(request.data)

        #이메일 형식 확인

        if not validateEmail(sign_up_dict['email']):  # 이메일에 대한 validation
            code = 401
            message = '이메일 형식 오류'
            status_ = status.HTTP_401_UNAUTHORIZED
            raise Exception

        #이메일 존재 확인
        exist = Profile.objects.filter(email=sign_up_dict['email'])
        if exist.exists():
            code = 402
            message = '이미 존재하는 이메일입니다'
            status_ = status.HTTP_402_PAYMENT_REQUIRED
            raise Exception
            #에러 일으키기


        email_dict ={}
        email_dict['isSuccess'] = 'true'
        email_dict['code'] = 200
        email_dict['message'] = '사용가능한 이메일입니다'
        return_value = json.dumps(email_dict, indent=4, use_decimal=True, ensure_ascii=False)
        return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

    except Exception:

        return for_exception(code, message, status_)


@api_view(['GET','POST'])
def sign_up(request):
    code = 400
    message ='파라미터 입력 오류'
    status_ = status.HTTP_400_BAD_REQUEST

    try:
        # 로그인 로직 -> jwt 발행
        if request.method =='GET':
            sign_in_dict = QueryDict.dict(request.data)

            # db에 해당 이메일로 가입된 계정이 있는지 확인
            if Profile.objects.filter(email=sign_in_dict['email']).exists():
                user = Profile.objects.get(email=sign_in_dict['email'])
            else:
                raise ValueError('정보없음')

            try:
                #비밀번호가 일치하면 토큰 발행
                if bcrypt.checkpw(sign_in_dict['userpwd'].encode('utf-8'), user.userpwd.encode('utf-8')):
                    # 토큰은 한 달 동안만 유효
                    expire_ts = int(time.time()) + 3600*24*30
                    token = jwt.encode({'email': sign_in_dict['email'],'expire':expire_ts}, SECRET_KEY, algorithm="HS256")
                    token = token.decode('utf-8')  # 유니코드 문자열로 디코딩
                else:
                    raise ValueError('비번불일치')
            except:
                raise ValueError('비번불일치')

            token_dict = {}
            token_dict['isSuccess'] = 'true'
            token_dict['code'] = 200
            token_dict['token'] = token
            return_value = json.dumps(token_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


        elif request.method =='POST':
            sign_up_dict = QueryDict.dict(request.data)

            # 이메일 형식 확인
            if not validateEmail(sign_up_dict['email']):  # 이메일에 대한 validation
                code = 401
                message = '이메일 형식 오류'
                status_ = status.HTTP_401_UNAUTHORIZED
                raise Exception

            # 이메일 존재 확인
            exist = Profile.objects.filter(email=sign_up_dict['email'])
            if exist.exists():
                code = 402
                message = '이미 존재하는 이메일입니다'
                status_ = status.HTTP_402_PAYMENT_REQUIRED
                raise Exception
                # 에러 일으키기

            # 비밀번호 일치 여부 확인
            if sign_up_dict['userpwd'] != sign_up_dict['userpwdConfirm']:
                code = 403
                message = '비밀번호가 일치하지 않습니다'
                status_ = status.HTTP_403_FORBIDDEN
                raise Exception

            # 비밀번호 validation
            validatePasswd(sign_up_dict['userpwd'])

            # 비밀번호 암호화
            password = sign_up_dict['userpwd'].encode('utf-8')  # 입력된 패스워드를 바이트 형태로 인코딩
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
            password_crypt = password_crypt.decode('utf-8')  # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
            sign_up_dict['userpwd'] = password_crypt
            print(sign_up_dict['userpwd'])

            # 생일 날짜 형식 확인
            validateBirth(sign_up_dict['birthday'])
            # userinfo( 닉네임, 프로필사진)
            userinfo_dict = {}

            userinfo_dict['profileimg'] = sign_up_dict['profileimg']
            userinfo_dict['nickname'] = sign_up_dict['nickname']
            userinfo_dict['isdeleted'] = 'N'

            query_dict = QueryDict('', mutable=True)
            query_dict.update(userinfo_dict)
            print(query_dict)
            serializer = UserinfoSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save()

            del sign_up_dict['profileimg']
            del sign_up_dict['nickname']
            del sign_up_dict['userpwdConfirm']
            sign_up_dict['isdeleted'] = 'N'
            sign_up_dict['isblocked'] = 'N'

            # 관심 카테고리
            category_dict = {}
            category_dict['category'] = sign_up_dict['category']
            del sign_up_dict['category']
            # 관심 서브 카테고리
            subcategory_dict = {}
            subcategory_dict['subcategory'] = sign_up_dict['subcategory']
            del sign_up_dict['subcategory']

            query_dict = QueryDict('', mutable=True)
            query_dict.update(sign_up_dict)
            print(query_dict)
            serializer = ProfileSerializer(data=query_dict)
            if serializer.is_valid():
                serializer.save()

            a = Userinfo.objects.last()
            userIdx = a.useridx

            for i in category_dict['category']:
                category = {}
                category['useridx'] = userIdx
                category['categoryidx'] = i
                category['isdeleted'] = 'N'
                query_dict = QueryDict('', mutable=True)
                query_dict.update(category)
                print(query_dict)
                serializer = CategoryinterestSerializer(data=query_dict)
                if serializer.is_valid():
                    serializer.save()

            for i in subcategory_dict['subcategory']:
                subcategory = {}
                subcategory['useridx'] = userIdx
                subcategory['subcategoryidx'] = i
                subcategory['isdeleted'] = 'N'

                query_dict = QueryDict('', mutable=True)
                query_dict.update(subcategory)
                print(query_dict)
                serializer = SubcategoryinterestSerializer(data=query_dict)
                if serializer.is_valid():
                    serializer.save()

            email_dict = {}
            email_dict['isSuccess'] = 'true'
            email_dict['code'] = 200
            email_dict['message'] = '회원가입 성공'
            return_value = json.dumps(email_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

    except ValueError as e:
        print(type(e))
        if str(e) == '생일':
            return for_exception(407, "올바른 날짜 형식을 기입해야 합니다", status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)
        elif str(e) == '정보없음':
            return for_exception(404, "해당 이메일로 가입된 정보가 없습니다", status.HTTP_404_NOT_FOUND)
        elif str(e) == '비번불일치':
            return for_exception(409, "비밀번호가 틀렸습니다", status.HTTP_409_CONFLICT)
        elif str(e) == '비번설정':
            return for_exception(406, "비밀번호는 8자리 이상의 숫자/문자/특수문자의 조합으로 이루어져야 합니다", status.HTTP_406_NOT_ACCEPTABLE)



    except Exception:

        return for_exception(code, message, status_)


@api_view(['GET'])
def google_login(request):
    print('hi')
    return JsonResponse({}, status=200)



