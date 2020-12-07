import { Component, OnInit } from '@angular/core';
import {ApiService} from '../api.service';
import {CookieService} from 'ngx-cookie-service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css', '../app.component.css']
})
export class HomeComponent implements OnInit {
  rankingPage = 1;
  recommendPage = 1;

  lectures: any = [];
  rankingdoverview: any = [];
  recommendoverview: any = [];

  token : string;
  nickname : string;
  maxPage:number;//

  constructor(private apiService: ApiService,
             private cookieService: CookieService
  ) { }

  ngOnInit(): void {
    this.token = this.cookieService.get('token');

    if(this.token){
      this.apiService.getPersonalInfo().subscribe(
        data => {
          this.nickname = data['result'].nickname;
          console.log(this.nickname);
        },
        error => console.log(error)
      );
    }
    this.callRankingApi();
    this.callRecommendApi();
  }

  callRankingApi(){
    this.apiService.getRankingOverview(this.rankingPage).subscribe(
      data => {
        this.rankingdoverview = data['result'];
        console.log(this.rankingdoverview);

        console.log('maxPage:');
        this.maxPage = data['maxPage'];
        console.log(data);
      },
      error => console.log(error)
    );
  }
  callRecommendApi(){
    this.apiService.getRecommendOverview(this.recommendPage).subscribe(
      data => {
        this.recommendoverview = data['result'];
        console.log(this.recommendoverview);
      },
      error => console.log(error)
    );
  }


  //change page
  rankingPageMax = 4;
  rankingPageMinus(){
    if(this.rankingPage>1){
      this.rankingPage -= 1;
    }else{
      this.rankingPage = this.rankingPageMax;
    }
    this.callRankingApi();
  }
  rankingPagePuls(){
    if(this.rankingPage<this.rankingPageMax){
      this.rankingPage += 1;
    }else{
      this.rankingPage = 1;
    }
    this.callRankingApi();
  }
  recommendPageMax = 2;
  recommendPageMinus(){
    if(this.recommendPage>1){
      this.recommendPage -= 1;
    }else{
      this.recommendPage = this.recommendPageMax;
    }
    this.callRecommendApi();
  }
  recommendPagePuls(){
    if(this.recommendPage<this.recommendPageMax){
      this.recommendPage += 1;
    }else{
      this.recommendPage = 1;
    }
    this.callRecommendApi();
  }
}
