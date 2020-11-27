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
  //강의 검색
  searchLectures(page, keyword, rate, level, price) {
    return this.httpClient.get(this.baseUrl + 'lectures?page='+page+'&keyword='+keyword+'&rating='+rate+'&level='+level+'&price='+price, {headers: this.headers});
  }


  /*for main-page*/
  // tslint:disable-next-line:typedef
  getRankingOverview(categoryIdx) {
    return this.httpClient.get(this.baseUrl + 'ranking-overview?categoryIdx='+categoryIdx, {headers: this.headers});
  }
  // tslint:disable-next-line:typedef
  getRecommendOverview(categoryIdx) {  // 나중에 api 바꾸기
    return this.httpClient.get(this.baseUrl + 'ranking-overview?categoryIdx='+categoryIdx, {headers: this.headers});
  }

  // 프로그램 주제별 랭킹
  // tslint:disable-next-line:typedef
  getALLLecturesRanking(page:number, categoryIdx:number, subCategoryIdx:number) {
    return this.httpClient.get(this.baseUrl + 'lectures-ranking?page='+page+'&categoryIdx='+categoryIdx+'&subcategoryIdx='+subCategoryIdx, {headers: this.headers});
  }
  getSubcategoryList(){
    return this.httpClient.get(this.baseUrl + 'subcategory-list', {headers: this.headers});
  }
  getCategoryList(){
    return this.httpClient.get(this.baseUrl + 'category-list', {headers: this.headers});
  }
  // today's recommend
  // tslint:disable-next-line:typedef
  getLecturesRecommend() {  // 나중에 api 바꾸기
    return this.httpClient.get(this.baseUrl + 'api/recommendlist', {headers: this.headers});
  }

 //강의 상세
  getLectureDetail(lectureIdx){
    return this.httpClient.get(this.baseUrl + 'lectures/' + lectureIdx);
  }
  // 강의별 리뷰 목록
  // tslint:disable-next-line:typedef
  
  // tslint:disable-next-line:typedef
  getLectureReviews(lectureIdx : number){
    return this.httpClient.get(this.baseUrl + 'lectures/' + lectureIdx + '/review', {headers: this.headers});
  }
  createLectureReviews(lectureIdx, totalrating:number, teachingpowerrating:number, pricerating:number, recommend:CharacterData, improvement:string, pros:Array<number>, cons:Array<number>){              //
    const body = JSON.stringify({totalrating, teachingpowerrating, pricerating, recommend, improvement, pros, cons});
    console.log(body);
    return this.httpClient.post(this.baseUrl + 'lectures/'+lectureIdx+'/review', body, {headers: this.headers});
  }
  // tslint:disable-next-line:typedef
  getLectureQnas(lectureIdx : number){
    return this.httpClient.get(this.baseUrl + 'lectures/'+lectureIdx+'/qna', {headers: this.headers});
  }
  createLectureQnas(lectureIdx : number, title : string, qnades : string, image : string[]){              //
    const body = JSON.stringify({title, qnades, image});
    console.log(body);
    return this.httpClient.post(this.baseUrl + 'lectures/'+lectureIdx+'/qna', body, {headers: this.headers});
  }
  //comments
  getLectureQnaSpecific(lectureIdx : number, qnaIdx : number){
     return this.httpClient.get(this.baseUrl + 'lectures/'+lectureIdx+'/qna/'+qnaIdx, {headers: this.headers});
  }
  getLectureQnaComments(lectureIdx : number, qnaIdx : number){
    return this.httpClient.get(this.baseUrl + 'lectures/'+lectureIdx+'/qna/'+qnaIdx+'/comment', {headers: this.headers});
  }
  createLectureQnaComments(lectureIdx : number, qnaIdx : number, commentdes:string){
    const body = JSON.stringify({commentdes});
    return this.httpClient.post(this.baseUrl + 'lectures/'+lectureIdx+'/qna/'+qnaIdx+'/comment', body, {headers: this.headers});
  }


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

  //mypage
  //개인정보
  getPersonalInfo(){
    return this.httpClient.get(this.baseUrl+'personal-info', {headers: this.headers});
  }
  getProfile(){
    return this.httpClient.get(this.baseUrl+'profile', {headers: this.headers});
  }
  patchPersonalInfo(email:string, userpwd:string, userpwdConfirm:string, name:string, phonenumber:string, nickname:string){
    const body = JSON.stringify({email, userpwd, userpwdConfirm, name, phonenumber, nickname});
    /*
    const body = {
      'email' : email,
      'name' : name,
      'nickname': nickname,
      'phonenumber': phonenumber,
      'userpwd': userpwd,
      'userpwdConfirm': userpwdConfirm
    };
    */
    console.log('personalInfo 수정');
    console.log(body);
    return this.httpClient.patch(this.baseUrl + 'personal-info', body, {headers: this.headers});
  }
  patchProfile(birthday:string, school:string, level:number, job:CharacterData, gender:CharacterData, subcategory:Array<number>, category:Array<number>){
    const body = JSON.stringify({birthday, school, level, job, gender, subcategory, category});
    console.log(body);
    return this.httpClient.patch(this.baseUrl + 'profile', body, {headers: this.headers});
  }

  //마이페이지 상세
  getFavoriteLectures(){
    return this.httpClient.get(this.baseUrl+'favorite-lectures', {headers: this.headers});
  }
  getMyReviews(){
    return this.httpClient.get(this.baseUrl +'my-reviews', {headers: this.headers});
  }
  deleteMyReview(lectureIdx:number, reviewIdx:number){
    return this.httpClient.delete(this.baseUrl +'lectures/'+lectureIdx+'/review/'+reviewIdx, {headers: this.headers});
  }
  
  patchFavoriteLectures(lectureIdx){
    return this.httpClient.patch(this.baseUrl+'favorite-lectures?lectureIdx='+lectureIdx, {}, {headers: this.headers});
  }///lecture/:lectureIdx/check-favorite
  isFavoriteLectures(lectureIdx : number){
    return this.httpClient.get(this.baseUrl+'lectures/'+lectureIdx+'/check-favorite', {headers: this.headers});
  }
  

  //개인정보조회
  /*
  getPersonalInfo(){
    return this.httpClient.get(this.baseUrl+'personalInfo', {headers: this.headers});
  }
  */

}