import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';
import {ApiService} from '../../api.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-lecture-qna',
  templateUrl: './lecture-qna.component.html',
  styleUrls: ['./lecture-qna.component.css']
})
export class LectureQnaComponent implements OnInit {
  /*form */
  qnaForm = new FormGroup({
    question: new FormControl(''),
    //desciption: new FormControl(''),
  });
  searchQna(){
    console.log(this.qnaForm.value);
  }

  qnas: any = [];
  selectedReview = null;

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit(): void {
    let thisLectureIdx = +this.route.snapshot.paramMap.get('lectureIdx');

    this.apiService.getLectureQnas(thisLectureIdx).subscribe(
      data => {
        this.qnas = data['result'];
        console.log(this.qnas);
      },
      error => console.log(error)
    );

  }

}
