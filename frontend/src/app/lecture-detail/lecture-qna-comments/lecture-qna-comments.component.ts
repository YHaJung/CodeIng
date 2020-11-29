import { Component, OnInit} from '@angular/core';
import {ApiService} from '../../api.service';
import {ActivatedRoute} from '@angular/router';
import {FormGroup, FormControl} from '@angular/forms';
import {CookieService} from "ngx-cookie-service";

@Component({
  selector: 'app-lecture-qna-comments',
  templateUrl: './lecture-qna-comments.component.html',
  styleUrls: ['./lecture-qna-comments.component.css']
})
export class LectureQnaCommentsComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private cookieService: CookieService
  ) { }

  qnaIdx : number;
  qna : any=[];
  comments : any =[];
  lectureIdx : number;
  token : string;

  ngOnInit(): void {
    this.token = this.cookieService.get('token');
    this.lectureIdx = Number(this.route.snapshot.paramMap.get('lectureIdx'));
    this.qnaIdx = Number(this.route.snapshot.paramMap.get('subpage').substr(7,7));

    this.apiService.getLectureQnaSpecific(this.lectureIdx, this.qnaIdx).subscribe(
      data => {
        this.qna = data['result'];
        console.log('qna:');
        console.log(this.qna);
      },
      error => console.log(error)
    );
    this.apiService.getLectureQnaComments(this.lectureIdx, this.qnaIdx).subscribe(
      data => {
        this.comments = data['result'];
        console.log('reply:');
        console.log(this.comments);
      },
      error => console.log(error)
    );
  }

  wirteCommentForm = new FormGroup({
    comment: new FormControl('')
  })
  createComment(){
    if(this.token){
      this.apiService.createLectureQnaComments(this.lectureIdx, this.qna.qnaIdx, this.wirteCommentForm.value.comment
      ).subscribe(
        result => console.log(result),
        error => console.log(error)
      );
      window.location.reload();
    }else{
      alert('로그인 후 이용할 수 있는 서비스입니다.');
    }
  }

}
