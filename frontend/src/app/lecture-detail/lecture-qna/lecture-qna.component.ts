import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../api.service';
import {ActivatedRoute} from '@angular/router';
import {CookieService} from 'ngx-cookie-service';


@Component({
  selector: 'app-lecture-qna',
  templateUrl: './lecture-qna.component.html',
  styleUrls: ['./lecture-qna.component.css']
})
export class LectureQnaComponent implements OnInit {
  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    private cookieService: CookieService,
  ) { }
  token : string;
  
  lectureIdx : number;
  page :string;
  subpage : string;

  selectedQnaIdx : number;
  qnas: any = [];
  selectedReview = null;

  //page
  pages = [1, 2, 3 ,4, 5];
  currentPage = 1;
  maxPage=1;

  goWriteQnaPage(){
    if(this.token){
      window.location.href="/lecturedetail/"+this.lectureIdx+"/qna/write";
    }else{
      alert('로그인하셔야 이용할 수 있는 서비스입니다.');
    }
  }

  ngOnInit(): void {
    this.token = this.cookieService.get('token');
    this.lectureIdx = Number(this.route.snapshot.paramMap.get('lectureIdx'));
    this.page = this.route.snapshot.paramMap.get('page');
    this.subpage = this.route.snapshot.paramMap.get('subpage').substr(0,7);
    this.loadQna();
  }

  loadQna(){
    this.apiService.getLectureQnas(this.lectureIdx).subscribe(
      data => {
        this.qnas = data['result'];
        console.log(this.qnas);
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
      this.loadQna();
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

  //comments
  selectQna(qna){
    window.location.href="/lecturedetail/"+this.lectureIdx+"/qna/comment"+qna.qnaIdx;
  }

}
