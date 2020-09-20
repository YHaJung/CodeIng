import {Component, Input, Output, EventEmitter, OnInit} from '@angular/core';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-lecture-rank-list',
  templateUrl: './lecture-rank-list.component.html',
  styleUrls: ['./lecture-rank-list.component.css']
})
export class LectureRankListComponent implements OnInit {

  @Input() lectures = [];
  @Output() selectLecture = new EventEmitter();
  constructor(

  ) { }

  ngOnInit(): void {

  }

  // tslint:disable-next-line:typedef
  lectureClicked(lecture) {
    this.selectLecture.emit(lecture);
  }

}
