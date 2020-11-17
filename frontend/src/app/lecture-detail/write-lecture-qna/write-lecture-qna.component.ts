import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';
import {ApiService} from '../../api.service';                 //
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-write-lecture-qna',
  templateUrl: './write-lecture-qna.component.html',
  styleUrls: ['./write-lecture-qna.component.css']
})
export class WriteLectureQnaComponent implements OnInit {
  @Output() finish = new EventEmitter();
  lectureIdx : number;
  images : string[] = ["testimg"];

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute
  ) {}                //

  wirteQnaForm = new FormGroup({
    title: new FormControl(''),
    description : new FormControl('')
  })
  
  cancealWriting(){
    this.wirteQnaForm.value.title = '';
    this.wirteQnaForm.value.description = '';
    this.finish.emit();
  }

  creatQna(){                                         //
    console.log(this.lectureIdx, this.wirteQnaForm.value.title, this.wirteQnaForm.value.description, this.images)
    /*token문제로 아직 작동x
    this.apiService.createLectureQnas(
      this.lectureIdx,
      this.wirteQnaForm.value.title,
      this.wirteQnaForm.value.description,
      this.images
    ).subscribe(
      result => console.log(result),
      error => console.log(error)
    );
    */
    
  }

  ngOnInit(): void {
    this.lectureIdx = +this.route.snapshot.paramMap.get('lectureIdx');
  }

}
