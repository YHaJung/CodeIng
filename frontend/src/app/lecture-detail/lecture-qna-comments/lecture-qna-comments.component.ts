import { Component, OnInit, Input } from '@angular/core';
import {ApiService} from '../../api.service';
import {ActivatedRoute} from '@angular/router';
import {FormGroup, FormControl} from '@angular/forms';

@Component({
  selector: 'app-lecture-qna-comments',
  templateUrl: './lecture-qna-comments.component.html',
  styleUrls: ['./lecture-qna-comments.component.css']
})
export class LectureQnaCommentsComponent implements OnInit {
  @Input() qnaIdx : number;
  constructor(private route: ActivatedRoute,private apiService: ApiService) { }

  qna : any=[];
  comments : any =[];
  lectureIdx : number;

  ngOnInit(): void {
    this.lectureIdx = Number(this.route.snapshot.paramMap.get('lectureIdx'));
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
    this.apiService.createLectureQnaComments(this.lectureIdx, this.qna.qnaIdx, this.wirteCommentForm.value.comment
    ).subscribe(
      result => console.log(result),
      error => console.log(error)
    );
    window.location.reload();
  }

}
