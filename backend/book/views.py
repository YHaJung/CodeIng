import simplejson as json
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Book
from lecture.views import for_exception


@api_view(['GET'])

def book_list(request):
    if request.method == 'GET':
        try:

            src = request.GET.get('site')



            books = Book.objects.filter(site=src)

            lec_dict = {}
            lec_dict['isSuccess'] = 'true'
            lec_dict['code'] = 200
            lec_dict['message'] = '도서 목록 조회 성공'
            info = []

            for book in books:
               print(book.booktitle)
               link = book.link
               title = book.booktitle
               site = book.site
               thumb = book.thumbnail
               info.append(
                    dict([('bookIdx', link),('title', title),('site', site), ('thumbnail', thumb)]))

            lec_dict['result'] = info


            return_value = json.dumps(lec_dict, indent=4, use_decimal=True, ensure_ascii=False)

            return HttpResponse(return_value, content_type="text/json-comment-filtered", status=status.HTTP_200_OK)

        except Exception:

            return for_exception()


