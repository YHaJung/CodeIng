import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseUrl = 'http://localhost:8000/';
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
  // tslint:disable-next-line:typedef
  getRankingOverview() {
    return this.httpClient.get(this.baseUrl + 'ranking-overview', {headers: this.headers});
  }

  // tslint:disable-next-line:typedef
  getRecommendOverview() {
    return this.httpClient.get(this.baseUrl + 'api/KNN_IBCF/7', {headers: this.headers});
  }
  // tslint:disable-next-line:typedef
  getLecturesRanking() {
    return this.httpClient.get(this.baseUrl + 'lectures-ranking', {headers: this.headers});
  }
  // tslint:disable-next-line:typedef
  getLecturesRecommend() {
    return this.httpClient.get(this.baseUrl + 'api/KNN_IBCF/', {headers: this.headers});
  }
}
