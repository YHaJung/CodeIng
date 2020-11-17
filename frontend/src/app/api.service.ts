import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {CookieService} from 'ngx-cookie-service';

// api명세서
/*https://docs.google.com/spreadsheets/d/1nkWZT2nQCqGKkkvK8B28_yZliRay6ngx6i9yA_YdLZU/edit#gid=0 */

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  token = this.cookieService.get('token');
  baseUrl = 'http://3.34.74.250/'; // 'http://127.0.0.1:8000/';
  headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Authorization: this.token
  });

  private lectures = ['자료구조와 알고리즘', 'python 배우기'];

  constructor(
    private httpClient: HttpClient,
    private cookieService: CookieService
  ) { }

  // tslint:disable-next-line:typedef
  getLectures() {
    return this.httpClient.get(this.baseUrl + 'lectures', {headers: this.headers});
  }
  searchLecturesAll(keyword) {
    return this.httpClient.get(this.baseUrl + 'lectures?keyword='+keyword, {headers: this.headers});
  }
  searchLecturesFilter(keyword, rate, level) {
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

 //강의 상세
  getLectureDetail(lectureIdx){
    return this.httpClient.get(this.baseUrl + 'lectures/' + lectureIdx, {headers: this.headers});
  }
  // 강의별 리뷰 목록
  // tslint:disable-next-line:typedef
  
  // tslint:disable-next-line:typedef
  getLectureReviews(lectureIdx : number){
    return this.httpClient.get(this.baseUrl + 'lectures/' + lectureIdx + '/review', {headers: this.headers});
  }
  // tslint:disable-next-line:typedef
  getLectureQnas(lectureIdx : number){
    return this.httpClient.get(this.baseUrl + 'lectures/'+lectureIdx+'/qna', {headers: this.headers});
  }
 
  createLectureQnas(lectureIdx : number, title : string, qnades : string, image : string[]){              //
    const newQna = JSON.stringify({title, qnades, image})
    console.log(newQna);
    return this.httpClient.post(this.baseUrl + 'lectures/'+lectureIdx+'/qna', newQna, {headers: this.headers});
  }

/*token cookie 적용할 때
  loginUser(authData){
    const body = JSON.stringify(authData);
    return this.httpClient.post(this.baseUrl+'auth/', body, {headers:this.headers});
  }
  */

  /*
  getLectureDetail(){
    return this.httpClient.get(this.baseUrl + 'lectures/:lectureIdx', {headers: this.headers});
  }
  */
  signin(email:string, userpwd:string){
    const body = JSON.stringify({email, userpwd});
    console.log(body);
    return this.httpClient.post(this.baseUrl + 'login', body, {headers: this.headers});
    //return this.httpClient.get(this.baseUrl + 'user', {params: new HttpParams([email, userpwd])};
  }
  signup(email:string, userpwd:string, userpwdConfirm:string, name:string, phonenumber:string, nickname:string){
    const body = JSON.stringify({email, userpwd, userpwdConfirm, name, phonenumber, nickname});
    console.log(body);
    return this.httpClient.post(this.baseUrl + 'user', body, {headers: this.headers});
    //return this.httpClient.get(this.baseUrl + 'user', {params: new HttpParams([email, userpwd])};
  }
}
