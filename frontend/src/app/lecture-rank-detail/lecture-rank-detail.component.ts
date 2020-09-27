import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-lecture-rank-detail',
  templateUrl: './lecture-rank-detail.component.html',
  styleUrls: ['./lecture-rank-detail.component.css']
})
export class LectureRankDetailComponent implements OnInit {


  lectures: any = [];
  selectedLecture = null;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.apiService.getLecturesRanking().subscribe(
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
