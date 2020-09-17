import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseUrl = 'http://localhost:8000/api/movies/';
  headers = new HttpHeaders({
    'Content-Type': 'application/json',
    Authorization: 'Token f44d5353e525567f525d74e4cb0d7b3abf806efe'
  });

  private lectures = ['자료구조와 알고리즘', 'python 배우기'];

  constructor(
    private httpClient: HttpClient
  ) { }


  // tslint:disable-next-line:typedef
  getLectures() {
    // const dynamicMovies = this.httpClient.get(this.baseUrl, {headers: this.headers});
    // console.log(dynamicMovies);
    // return this.lectures;
    return this.httpClient.get(this.baseUrl, {headers: this.headers});
  }
}
