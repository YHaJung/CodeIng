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

  lectureIdx : number;
  token : string;

  page = 0;
  goWriteQnaPage(){
    if(this.token){
      this.page = 1;
    }else{
      alert('로그인하셔야 이용할 수 있는 서비스입니다.');
    }
  }
  writeFinished(){
    this.page = 0;
  }

  qnas: any = [];
  selectedReview = null;

  

  ngOnInit(): void {
    this.lectureIdx = +this.route.snapshot.paramMap.get('lectureIdx');
    this.token = this.cookieService.get('token');

    this.apiService.getLectureQnas(this.lectureIdx).subscribe(
      data => {
        this.qnas = data['result'];
        console.log('qnas:');
        console.log(this.qnas);
      },
      error => console.log(error)
    );

  }
  //comments
  selectedQnaIdx : number;
  selectQna(qna){
    this.page=2;
    this.selectedQnaIdx = qna.qnaIdx;
    console.log('qnaidx:'+this.selectedQnaIdx);
  }

}
