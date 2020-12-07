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
  baseUrl = 'https://www.coconerd.tk/';//'http://3.34.74.250/';//  'http://127.0.0.1:8000/';
  headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Authorization: this.token
  });

  constructor(
    private httpClient: HttpClient,
    private cookieService: CookieService
  ) { }

  //ranking
  getLectures() {
    return this.httpClient.get(this.baseUrl + 'lectures', {headers: this.headers});
  }
  //강의 검색
  searchLectures(page, keyword, rate, level, lowPrice, highPrice) {
    return this.httpClient.get(this.baseUrl + 'lectures?page='+page+'&keyword='+keyword+'&rating='+rate+'&level='+level+'&lowerLimit='+lowPrice+'&upperLimit='+highPrice, {headers: this.headers});
  }


  //home
  getRankingOverview(page) {
    return this.httpClient.get(this.baseUrl + 'overall-ranking?page='+page, {headers: this.headers});
  }
  getRecommendOverview(page:number) {  // 나중에 api 바꾸기
    if(this.token){
      return this.httpClient.get(this.baseUrl + 'api/user_recommend?page='+page, {headers: this.headers});
    }else{
      return this.httpClient.get(this.baseUrl + 'api/recommend?page='+page, {headers: this.headers});
    }
  }

  // 프로그램 주제별 랭킹
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
    if(this.token){
      return this.httpClient.get(this.baseUrl + 'api/user_recommendlist', {headers: this.headers});
    }else{
      return this.httpClient.get(this.baseUrl + 'api/recommendlist', {headers: this.headers});
    }
  }

 //강의 상세
  getLectureDetail(lectureIdx){
    return this.httpClient.get(this.baseUrl + 'lectures/' + lectureIdx);
  }
  //review
  getLectureReviews(lectureIdx : number, page:number){
    return this.httpClient.get(this.baseUrl + 'lectures/' + lectureIdx + '/review?page='+page, {headers: this.headers});
  }
  createLectureReviews(lectureIdx, totalrating:number, teachingpowerrating:number, pricerating:number, recommend:CharacterData, improvement:string, pros:Array<number>, cons:Array<number>){              //
    const body = JSON.stringify({totalrating, teachingpowerrating, pricerating, recommend, improvement, pros, cons});
    console.log(body);
    return this.httpClient.post(this.baseUrl + 'lectures/'+lectureIdx+'/review', body, {headers: this.headers});
  }
  //qna
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
  //유사한 다른 강의 추천
  getSimilarLectures(lectureIdx : number){
    ///api/:lectureIdx/item_recommend
    //return this.httpClient.get(this.baseUrl + 'overall-ranking?page=1', {headers: this.headers});
    return this.httpClient.get(this.baseUrl + 'api/'+lectureIdx+'/item_recommend', {headers: this.headers});
  }

  //auth
  signin(email:string, userpwd:string){
    const body = JSON.stringify({email, userpwd});
    console.log(body);
    return this.httpClient.post(this.baseUrl + 'login', body, {headers: this.headers});
  }
  signup(email:string, userpwd:string, userpwdConfirm:string, name:string, phonenumber:string, nickname:string){
    const body = JSON.stringify({email, userpwd, userpwdConfirm, name, phonenumber, nickname});
    console.log(body);
    return this.httpClient.post(this.baseUrl + 'user', body, {headers: this.headers});
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
    console.log('personalInfo 수정');
    console.log(body);
    return this.httpClient.patch(this.baseUrl + 'personal-info', body, {headers: this.headers});
  }
  patchProfile(birthday:string, school:string, level:number, job:CharacterData, gender:CharacterData, subcategory:Array<number>, category:Array<number>){
    const body = JSON.stringify({birthday, school, level, job, gender, subcategory, category});
    console.log(body);
    return this.httpClient.patch(this.baseUrl + 'profile', body, {headers: this.headers});
  }
  withdrawal(){/*회원탈퇴 */
    return this.httpClient.delete(this.baseUrl+'user', {headers: this.headers});
  }

  //마이페이지 상세
  //관심 강의
  getFavoriteLectures(){
    return this.httpClient.get(this.baseUrl+'favorite-lectures', {headers: this.headers});
  }
  patchFavoriteLectures(lectureIdx){
    return this.httpClient.patch(this.baseUrl+'favorite-lectures?lectureIdx='+lectureIdx, {}, {headers: this.headers});
  }
  isFavoriteLectures(lectureIdx : number){
    return this.httpClient.get(this.baseUrl+'lectures/'+lectureIdx+'/check-favorite', {headers: this.headers});
  }
  //관심 사이트
  getFavoriteSites(){
    return this.httpClient.get(this.baseUrl+'favorite-sites', {headers: this.headers});
  }
  patchFavoriteSites(siteIdx : number){
    return this.httpClient.patch(this.baseUrl+'favorite-sites?siteIdx='+siteIdx, {}, {headers: this.headers});
  }
  isFavoriteSites(siteIdx : number){
    return this.httpClient.get(this.baseUrl+'sites/'+siteIdx+'/check-favorite', {headers: this.headers});
  }
  //내가쓴 리뷰
  getMyReviews(){
    return this.httpClient.get(this.baseUrl +'my-reviews', {headers: this.headers});
  }
  deleteMyReview(lectureIdx:number, reviewIdx:number){
    return this.httpClient.delete(this.baseUrl +'lectures/'+lectureIdx+'/review/'+reviewIdx, {headers: this.headers});
  }
}