import { Component, OnInit } from '@angular/core';
import { faStar, faBookmark, faCheck  } from '@fortawesome/free-solid-svg-icons';
import {ActivatedRoute} from '@angular/router';
import {ApiService} from '../api.service';

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
  lectureDetail: any=[];
  avg_rating = 0;
  level = 0;
  
  reviews: any = [];
  recommendoverview: any = [];


  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService
  ) { }


  ngOnInit(): void {
    
    this.avg_rating = 0;
    this.level = 0;

    this.lectureIdx = Number(this.route.snapshot.paramMap.get('lectureIdx'));

    //call lecture info
    this.apiService.getLectureDetail(this.lectureIdx).subscribe(
      data => {
        this.lectureDetail = data['result'];
        console.log('lecture-detail');
        console.log(this.lectureDetail);
        this.avg_rating = this.lectureDetail.rating;
        this.level = this.lectureDetail.level;

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
      },
      error => console.log(error)
    );
    //patchFavoriteLectures(lectureIdx:number)
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
  


  /*navigation */
  reviewChecked = 1;
  qnaChecked = 0;
  viewReviews(){
    this.reviewChecked = 1;
    this.qnaChecked = 0;
  }
  viewQna(){
    this.qnaChecked = 1;
    this.reviewChecked = 0;
  }

  setFavoriteLecture(){
    this.apiService.patchFavoriteLectures(this.lectureIdx).subscribe(
      result => {
        console.log(result);
      },
      error => console.log(error)
    );
    window.location.reload();
  }

  setFavoriteSite(){
    this.apiService.patchFavoriteSites(this.lectureDetail.siteIdx).subscribe(
      result => {
        console.log(result);
      },
      error => console.log(error)
    );
    window.location.reload();
  }
}
