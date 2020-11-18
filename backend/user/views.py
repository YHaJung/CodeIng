import datetime
import time

import bcrypt
import jwt
import simplejson as json
from django.conf.global_settings import SECRET_KEY
from django.http import HttpResponse, QueryDict, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Profile, Userinfo, Categoryinterest, Subcategoryinterest

#생년월일에 대한 validation
from .serializers import ProfileSerializer, UserinfoSerializer, CategoryinterestSerializer, \
    SubcategoryinterestSerializer



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
            print('성공')





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


@api_view(['POST'])
def login(request):
    code = 400
    message = '파라미터 입력 오류'
    status_ = status.HTTP_400_BAD_REQUEST

    try:
        # 로그인 로직 -> jwt 발행
        if request.method == 'POST':
            sign_in_dict = QueryDict.dict(request.data)

            # db에 해당 이메일로 가입된 계정이 있는지 확인
            if Profile.objects.filter(email=sign_in_dict['email']).exists():
                user = Profile.objects.get(email=sign_in_dict['email'])
            else:
                raise ValueError('정보없음')

            try:
                # 비밀번호가 일치하면 토큰 발행
                if bcrypt.checkpw(sign_in_dict['userpwd'].encode('utf-8'), user.userpwd.encode('utf-8')):
                    # 토큰은 한 달 동안만 유효
                    expire_ts = int(time.time()) + 3600 * 24 * 30
                    token = jwt.encode({'email': sign_in_dict['email'], 'expire': expire_ts}, SECRET_KEY,
                                       algorithm="HS256")
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


#수정된 회원가입
@api_view(['POST'])
def sign_up(request):
    code = 400
    message ='파라미터 입력 오류'
    status_ = status.HTTP_400_BAD_REQUEST

    try:

        if request.method =='POST':
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

            # 휴대폰 번호 넣었는지 여부
            if(len(sign_up_dict['phonenumber']) == 0):
                code = 402
                message = '휴대폰 번호를 입력하세요'
                status_ = status.HTTP_402_PAYMENT_REQUIRED
                raise Exception


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
            # print(sign_up_dict['userpwd'])


            # userinfo( 닉네임, 프로필사진)
            userinfo_dict = {}

            userinfo_dict['nickname'] = sign_up_dict['nickname']
            userinfo_dict['isdeleted'] = 'N'

            query_dict = QueryDict('', mutable=True)
            query_dict.update(userinfo_dict)
            print(query_dict)
            serializer = UserinfoSerializer(data=query_dict)

            if serializer.is_valid():
                serializer.save()


            del sign_up_dict['nickname']
            del sign_up_dict['userpwdConfirm']
            sign_up_dict['isdeleted'] = 'N'
            sign_up_dict['isblocked'] = 'N'



            query_dict = QueryDict('', mutable=True)
            query_dict.update(sign_up_dict)
            print(query_dict)

            serializer = ProfileSerializer(data=query_dict)
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
@api_view(['GET','POST'])
def sign_up_test(request):
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


#회원 정보 조회
@api_view(['GET', 'PATCH'])
@login_decorator
def personal_info(request):
    try:
        code = 400
        message = '파라미터 입력 오류'
        status_ = status.HTTP_400_BAD_REQUEST

        if request.method == 'GET':
            userIdx = request.user.userinfo.useridx

            personal_dict={}
            personal_dict['isSuccess'] = 'true'
            personal_dict['code'] = 200
            personal_dict['message'] = '회원정보 조회 성공'

            personal_dict['result'] = dict([('name', request.user.name), ('nickname', request.user.userinfo.nickname),
                              ('phonenumber', request.user.phonenumber),('email', request.user.email)])

            return_value = json.dumps(personal_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            p_dict = QueryDict.dict(request.data)
          

            
            #비밀번호 변경
            if "userpwd" in p_dict and "userpwdConfirm" in p_dict:
                
                # 비번 안 바꿀 경우 
                if len(p_dict['userpwd']) == 0 and len(p_dict['userpwdConfirm'] == 0):
                    data = request.user
                    data.email = p_dict['email']
                    data.phonenumber = p_dict['phonenumber']
                    data.name = p_dict['name']
                    data.nickname = p_dict['nickname']
                    data.save()
                    
                    
                     

                if(p_dict['userpwd'] != p_dict['userpwdConfirm']):
                    raise ValueError("비번불일치")

                # 비밀번호 validation
                validatePasswd(p_dict['userpwd'])

                # 비밀번호 암호화
                password = p_dict['userpwd'].encode('utf-8')  # 입력된 패스워드를 바이트 형태로 인코딩
                password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
                password_crypt = password_crypt.decode('utf-8')  # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
                p_dict['userpwd'] = password_crypt


                data = request.user
                data.email = p_dict['email']
                data.phonenumber = p_dict['phonenumber']
                data.name = p_dict['name']
                data.nickname = p_dict['nickname']
                data.userPwd = p_dict['userpwd']
                data.save()
            #비번 안 바꿀 경우 -> Key 줄 때
            elif "userpwd" not in p_dict and "userpwdConfirm" not in p_dict:
                data = request.user
                data.email = p_dict['email']
                data.phonenumber = p_dict['phonenumber']
                data.name = p_dict['name']
                data.nickname = p_dict['nickname']
                data.save()

            else:
                raise Exception




            return JsonResponse({'isSuccess': 'true',
                                 'code': 200,
                                 'message': '회원정보 수정 성공'}, status=200)



    except ValueError as e:

        if str(e) == '생일':

            return for_exception(407, "올바른 날짜 형식을 기입해야 합니다", status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)

        elif str(e) == '정보없음':

            return for_exception(404, "해당 이메일로 가입된 정보가 없습니다", status.HTTP_404_NOT_FOUND)

        elif str(e) == '비번불일치':

            return for_exception(409, "비밀번호가 일치하지 않습니다", status.HTTP_409_CONFLICT)

        elif str(e) == '비번설정':

            return for_exception(406, "비밀번호는 8자리 이상의 숫자/문자/특수문자의 조합으로 이루어져야 합니다", status.HTTP_406_NOT_ACCEPTABLE)




    except Exception:

        return for_exception(code, message, status_)


# 프로필 정보 조회
@api_view(['GET', 'PATCH'])
@login_decorator
def profile(request):
    try:
        code = 400
        message = '파라미터 입력 오류'
        status_ = status.HTTP_400_BAD_REQUEST

        if request.method == 'GET':
            userIdx = request.user.userinfo.useridx

            category_interest = Categoryinterest.objects.filter(useridx=userIdx, isdeleted='N')
            subcategory_interest = Subcategoryinterest.objects.filter(useridx=userIdx, isdeleted='N')
            cate_list=[]
            subcate_list=[]
            for i in category_interest:
                cate_list.append(
                    dict([('categoryIdx', i.categoryidx.categoryidx), ('categoryName', i.categoryidx.categoryname)]))

            for i in subcategory_interest:
                subcate_list.append(
                    dict([('subcategoryIdx', i.subcategoryidx.subcategoryidx), ('subcategoryName', i.subcategoryidx.subcategoryname)]))

            personal_dict = {}
            personal_dict['isSuccess'] = 'true'
            personal_dict['code'] = 200
            personal_dict['message'] = '프로필 조회 성공'


            personal_dict['result'] = dict([('school', request.user.school), ('gender', request.user.gender),
                                            ('birthday', str(request.user.birthday)), ('level', request.user.level.levelname),
                                            ('job', request.user.job), ('category', cate_list), ('subcategory', subcate_list)
                                            ])


            return_value = json.dumps(personal_dict, indent=4, use_decimal=True, ensure_ascii=False)
            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)


        #프로필 수정 ->
        elif request.method == 'PATCH':
            p_dict = QueryDict.dict(request.data)

            print(p_dict)
            
            #profile -> 받아온 데이터 넣기
            data = request.user

            data.school = p_dict['school']
            data.birthday = p_dict['birthday']
            data.gender = p_dict['gender']
            data.level.levelidx = int(p_dict['level'])
            data.job = p_dict['job']
            data.save()

            # 원래 있던거 삭제하고 다시 넣기
            category_interest = Categoryinterest.objects.filter(useridx=request.user.userinfo.useridx, isdeleted='N')
            subcategory_interest = Subcategoryinterest.objects.filter(useridx=request.user.userinfo.useridx, isdeleted='N')

            # category_interst 값 차례로 삭제
            delete(category_interest, CategoryinterestSerializer)
            delete(subcategory_interest, SubcategoryinterestSerializer)

            # 새로 받아온 값 생성

            for i in range(len(p_dict['category'])):
                category_interest = {}
                category_interest['categoryidx'] = p_dict['category'][i]
                category_interest['useridx'] = request.user.userinfo.useridx
                category_interest['isdeleted'] = 'N'
                print('너 뭐야')
                # 새로운 값 차례로 넣기
                query_dict = QueryDict('', mutable=True)
                query_dict.update(category_interest)
                serializer = CategoryinterestSerializer(data=query_dict)
                if serializer.is_valid():
                    serializer.save()


            for i in range(len(p_dict['subcategory'])):
                subcategory_interest = {}
                subcategory_interest['subcategoryidx'] = p_dict['subcategory'][i]
                subcategory_interest['useridx'] = request.user.userinfo.useridx
                subcategory_interest['isdeleted'] = 'N'

                # 새로운 값 차례로 넣기
                query_dict = QueryDict('', mutable=True)
                query_dict.update(subcategory_interest)
                serializer = SubcategoryinterestSerializer(data=query_dict)
                if serializer.is_valid():
                    serializer.save()
                    print('성공')


            return JsonResponse({'isSuccess': 'true',
                                 'code': 200,
                                 'message': '프로필 수정 성공'}, status=200)



    except ValueError as e:

        if str(e) == '생일':

            return for_exception(407, "올바른 날짜 형식을 기입해야 합니다", status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)

        elif str(e) == '정보없음':

            return for_exception(404, "해당 이메일로 가입된 정보가 없습니다", status.HTTP_404_NOT_FOUND)

        elif str(e) == '비번불일치':

            return for_exception(409, "비밀번호가 일치하지 않습니다", status.HTTP_409_CONFLICT)

        elif str(e) == '비번설정':

            return for_exception(406, "비밀번호는 8자리 이상의 숫자/문자/특수문자의 조합으로 이루어져야 합니다", status.HTTP_406_NOT_ACCEPTABLE)




    except Exception:

        return for_exception(code, message, status_)









