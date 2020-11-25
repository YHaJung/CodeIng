import { Component, OnInit } from '@angular/core';
import {ApiService} from '../api.service';
import {CookieService} from 'ngx-cookie-service';
import {ActivatedRoute} from '@angular/router';

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
  selectedLecture = null;

  token : string;
  nickname : string;

  constructor(private apiService: ApiService,
             private cookieService: CookieService,
             private route: ActivatedRoute 
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
        console.log(this.rankingdoverview.length);
      },
      error => console.log(error)
    );
  }
  callRecommendApi(){
    if(this.token){
      this.apiService.getRecommendOverview(this.recommendPage).subscribe(
        data => {
          this.recommendoverview = data['result'];
          console.log(this.recommendoverview);
        },
        error => console.log(error)
      );
    }else{
      this.apiService.getRecommendOverview(this.recommendPage).subscribe(
        data => {
          this.recommendoverview = data['result'];
          console.log(this.recommendoverview);
        },
        error => console.log(error)
      );
    }
  }

  // tslint:disable-next-line:typedef
  selectLecture(lecture){
    this.selectedLecture = lecture;
  }


  //change page
  rankingPageMinus(){
    if(this.rankingPage>1){
      this.rankingPage -= 1;
      this.callRankingApi();
    }
  }
  rankingPagePuls(){
    this.rankingPage += 1;
    this.callRankingApi();
  }
  recommendPageMinus(){
    if(this.recommendPage>1){
      this.recommendPage -= 1;
      this.callRecommendApi();
    }
  }
  recommendPagePuls(){
    this.recommendPage += 1;
    this.callRecommendApi();
  }
}
