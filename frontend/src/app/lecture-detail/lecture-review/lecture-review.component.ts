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

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    private cookieService: CookieService,
  ) { }

  ngOnInit(): void {
    let thisLectureIdx = +this.route.snapshot.paramMap.get('lectureIdx');

    this.apiService.getLectureReviews(thisLectureIdx).subscribe(
      data => {
        this.reviews = data['result'];
        console.log(this.reviews);
      },
      error => console.log(error)
    );
  }

  write = false;
  goWriteReviewPage(){
    this.token = this.cookieService.get('token');
    if(this.token){
      this.write = true;
    }else{
      alert('로그인하셔야 이용할 수 있는 서비스입니다.');
    }
    
  }
  writeFinished(){
    this.write = false;
  }
}
