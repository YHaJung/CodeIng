import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../api.service';
import {ActivatedRoute} from '@angular/router';
import {CookieService} from 'ngx-cookie-service';

@Component({
  selector: 'app-lecture-review',
  templateUrl: './lecture-review.component.html',
  styleUrls: ['./lecture-review.component.css']
})
export class LectureReviewComponent implements OnInit {

  reviews: any = [];
  selectedReview = null;

  token:string;

  lectureIdx:number;
  subpage:string;

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    private cookieService: CookieService,
  ) { }

  ngOnInit(): void {
    this.lectureIdx = Number(this.route.snapshot.paramMap.get('lectureIdx'));
    this.subpage = this.route.snapshot.paramMap.get('subpage').substr(0,7);
    this.apiService.getLectureReviews(this.lectureIdx).subscribe(
      data => {
        this.reviews = data['result'];
        console.log(this.reviews);
      },
      error => console.log(error)
    );
  }

  goWriteReviewPage(){
    this.token = this.cookieService.get('token');
    if(this.token){
      window.location.href="/lecturedetail/"+this.lectureIdx+"/review/write"
    }else{
      alert('로그인하셔야 이용할 수 있는 서비스입니다.');
    }
  }
}
