import { Component, OnInit } from '@angular/core';
import { faStar, faBookmark, faCheck  } from '@fortawesome/free-solid-svg-icons';
import {ActivatedRoute} from '@angular/router';
import {ApiService} from '../api.service';
import {CookieService} from 'ngx-cookie-service';

@Component({
  selector: 'app-lecture-detail',
  templateUrl: './lecture-detail.component.html',
  styleUrls: ['./lecture-detail.component.css']
})
export class LectureDetailComponent implements OnInit {
  star = faStar;
  bookmark = faBookmark;
  check = faCheck;

  favoriteLecture = 0 ;       //관심강의 여부
  favoriteSite = 0 ;       //관심사이트 여부

  lectureIdx : number;
  page : string;
  
  lectureDetail: any=[];
  avg_rating = 0;
  level = 0;
  token : string;
  
  reviews: any = [];
  recommendoverview: any = [];

  //유사한 다른 강의
  similarLectures:[];


  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private cookieService: CookieService,
  ) { }


  ngOnInit(): void {
    this.token = this.cookieService.get('token');
    
    this.avg_rating = 0;
    this.level = 0;

    this.lectureIdx = Number(this.route.snapshot.paramMap.get('lectureIdx'));
    this.page = this.route.snapshot.paramMap.get('page');

    //강의상세 불러오기
    this.apiService.getLectureDetail(this.lectureIdx).subscribe(
      data => {
        this.lectureDetail = data['result'];
        console.log('lecture-detail');
        console.log(this.lectureDetail);
        this.avg_rating = this.lectureDetail.rating;
        this.level = this.lectureDetail.level;

  
        if(this.token){
          //관심 사이트 여부
          this.apiService.isFavoriteSites(this.lectureDetail.siteIdx).subscribe(
            data => {
              if(data['state']=='true'){
                this.favoriteSite = 1;
              }else{
                this.favoriteSite = 0;
              }
              console.log('favor-site?');
              console.log(this.favoriteSite);
            },
            error => {console.log(error)}
          );

          //관심 강의 여부
          this.apiService.isFavoriteLectures(this.lectureIdx).subscribe(
            data => {
              if(data['state']=='true'){
                this.favoriteLecture = 1;
              }else{
                this.favoriteLecture = 0;
              }
              console.log('favor-lecture?');
              console.log(this.favoriteLecture);
            },
            error => console.log(error)
          );

        }

      },
      error => console.log(error)
    );

    //유사한 다른 강의들 불러오기
    //getSimilarLectures
    this.apiService.getSimilarLectures(this.lectureIdx).subscribe(
      data => {
        this.similarLectures = data['result'];
        console.log('similar-lectures:');
        console.log(this.similarLectures);
      },
      error => {console.log(error)}
    );
    
    

  }
  

  //관심 강의 여부 변경
  setFavoriteLecture(){
    if(this.token){
      this.apiService.patchFavoriteLectures(this.lectureIdx).subscribe(
        result => {
          console.log(result);
        },
        error => console.log(error)
      );
      if(this.favoriteLecture == 0){
        this.favoriteLecture = 1;
      }else{
        this.favoriteLecture = 0;
      }
      //window.location.reload();
    }else{
      alert('로그인하셔야 이용할 수 있는 서비스입니다.');
    }
    
  }
  //관심 사이트 여부 변경
  setFavoriteSite(){
    if(this.token){
      this.apiService.patchFavoriteSites(this.lectureDetail.siteIdx).subscribe(
        result => {
          console.log(result);
        },
        error => console.log(error)
      );
      if( this.favoriteSite == 0){
        this.favoriteSite = 1;
      }else{
        this.favoriteSite = 0;
      }
    }else{
      alert('로그인하셔야 이용할 수 있는 서비스입니다.');
    }
    //window.location.reload();
  }
}
