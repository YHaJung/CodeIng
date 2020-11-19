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
  lectureIdx : number;

  write = false;
  goWriteQnaPage(){
    this.write = true;
  }
  writeFinished(){
    this.write = false;
  }

  qnas: any = [];
  selectedReview = null;

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit(): void {
    this.lectureIdx = +this.route.snapshot.paramMap.get('lectureIdx');

    this.apiService.getLectureQnas(this.lectureIdx).subscribe(
      data => {
        this.qnas = data['result'];
        console.log('qnas:');
        console.log(this.qnas);
      },
      error => console.log(error)
    );

  }

}
