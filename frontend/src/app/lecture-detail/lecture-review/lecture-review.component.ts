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

  //page
  pages = [1, 2, 3 ,4, 5];
  currentPage = 1;
  maxPage=1;

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    private cookieService: CookieService,
  ) { }

  ngOnInit(): void {
    this.lectureIdx = Number(this.route.snapshot.paramMap.get('lectureIdx'));
    this.subpage = this.route.snapshot.paramMap.get('subpage').substr(0,7);
    this.loadReviews();
  }
  loadReviews(){
    this.apiService.getLectureReviews(this.lectureIdx, this.currentPage).subscribe(
      data => {
        this.reviews = data['result'];
        console.log(this.reviews);
        //maxpage 불러오기
        this.maxPage = data['maxPage'];
        console.log('maxPage :');
        console.log( this.maxPage );
      },
      error => console.log(error)
    );
  }

  //page 선택
  selectPage(page){
    if(page<=this.maxPage){
      this.currentPage = page;
      this.loadReviews();
    }
  }
  pageMinusJump(){
    if(this.pages[0]!=1){
      this.pages[0] -= 5;
      this.pages[1] -= 5;
      this.pages[2] -= 5;
      this.pages[3] -= 5;
      this.pages[4] -= 5;
    }
  }
  pagePlusJump(){
    this.pages[0] += 5;
    this.pages[1] += 5;
    this.pages[2] += 5;
    this.pages[3] += 5;
    this.pages[4] += 5;
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
