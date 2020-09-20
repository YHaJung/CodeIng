import { Component, OnInit } from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-lecture-recommend-detail',
  templateUrl: './lecture-recommend-detail.component.html',
  styleUrls: ['./lecture-recommend-detail.component.css']
})
export class LectureRecommendDetailComponent implements OnInit {

  lectures: any = [];
  selectedLecture = null;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.apiService.getLectures().subscribe(
      data => {
        this.lectures = data;
      },
      error => console.log(error)
    );
  }

  // tslint:disable-next-line:typedef
  selectLecture(lecture){
    this.selectedLecture = lecture;
  }

}
