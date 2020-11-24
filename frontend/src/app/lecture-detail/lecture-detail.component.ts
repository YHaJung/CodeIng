import { Component, OnInit } from '@angular/core';
import { faStar, faBookmark  } from '@fortawesome/free-solid-svg-icons';
import {ActivatedRoute} from '@angular/router';
import {ApiService} from '../api.service';
import { Options } from '@angular-slider/ngx-slider';

@Component({
  selector: 'app-lecture-detail',
  templateUrl: './lecture-detail.component.html',
  styleUrls: ['./lecture-detail.component.css']
})
export class LectureDetailComponent implements OnInit {
  star = faStar;
  bookmark = faBookmark;
  favoriteLecture = false;
  lectureIdx : string;

  setFavoriteLecture(){
    this.apiService.patchFavoriteLectures(this.lectureIdx).subscribe(
      result => {
        console.log(result);
      },
      error => console.log(error)
    );
    if(this.favoriteLecture == false){
      this.favoriteLecture = true;
    }else{
      this.favoriteLecture = false;
    }
  }


  lectureDetail: any=[];
  title :string;
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

    this.lectureIdx = this.route.snapshot.paramMap.get('lectureIdx');

    //call lecture info
    this.apiService.getLectureDetail(this.lectureIdx).subscribe(
      data => {
        this.lectureDetail = data['result'];
        console.log(this.lectureDetail);
        this.title = this.lectureDetail.lectureName;
        this.avg_rating = this.lectureDetail.rating;
        this.level = this.lectureDetail.level;
      },
      error => console.log(error)
    );
    //patchFavoriteLectures(lectureIdx:number)

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

}
