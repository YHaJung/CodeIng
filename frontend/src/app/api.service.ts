import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

// api명세서
/*https://docs.google.com/spreadsheets/d/1nkWZT2nQCqGKkkvK8B28_yZliRay6ngx6i9yA_YdLZU/edit#gid=0 */

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseUrl = 'http://3.34.74.250/'; // 'http://127.0.0.1:8000/';
  headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Authorization: 'Token 8529e34d1eb5c264103bc0a2b696bae243f509bf'
  });

  private lectures = ['자료구조와 알고리즘', 'python 배우기'];

  constructor(
    private httpClient: HttpClient
  ) { }

  // tslint:disable-next-line:typedef
  getLectures() {
    return this.httpClient.get(this.baseUrl + 'lectures', {headers: this.headers});
  }
  searchLectures(keyword, rate, level) {
    return this.httpClient.get(this.baseUrl + 'lectures?keyword='+keyword+'&rating='+rate+'&level='+level, {headers: this.headers});
  }

  /*for main-page*/
  // tslint:disable-next-line:typedef
  getRankingOverview() {
    return this.httpClient.get(this.baseUrl + 'ranking-overview', {headers: this.headers});
  }
  // tslint:disable-next-line:typedef
  getRecommendOverview() {  // 나중에 api 바꾸기
    return this.httpClient.get(this.baseUrl + 'ranking-overview', {headers: this.headers});
  }

  // 프로그램 주제별 랭킹
  // tslint:disable-next-line:typedef
  getLecturesRanking() {
    return this.httpClient.get(this.baseUrl + 'lectures-ranking', {headers: this.headers});
  }
  // today's recommend
  // tslint:disable-next-line:typedef
  getLecturesRecommend() {  // 나중에 api 바꾸기
    return this.httpClient.get(this.baseUrl + 'lectures', {headers: this.headers});
  }

  // 강의별 리뷰 목록
  // tslint:disable-next-line:typedef
  getLectureDetail(lectureIdx){
    return this.httpClient.get(this.baseUrl + 'lectures/' + lectureIdx, {headers: this.headers});
  }
  // tslint:disable-next-line:typedef
  getLectureReviews(lectureIdx){
    return this.httpClient.get(this.baseUrl + 'lectures/' + lectureIdx + '/review', {headers: this.headers});
  }
  // tslint:disable-next-line:typedef
  getLectureQnas(lectureIdx){
    return this.httpClient.get(this.baseUrl + 'lectures/'+lectureIdx+'/qna', {headers: this.headers});
  }

  /*
  getLectureDetail(){
    return this.httpClient.get(this.baseUrl + 'lectures/:lectureIdx', {headers: this.headers});
  }
  */




  // post example
  /*
  postLectureRate(rate:number, lectureId: number){
    const body =JSON.stringify({stars: rate});
    return this.httpClient.post('${this.baseUrl+""}${lectureId}/rate-/', body, {headers: this.headers});
  }
  */
}
