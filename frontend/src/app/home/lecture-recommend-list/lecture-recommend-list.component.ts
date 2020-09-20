import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-lecture-recommend-list',
  templateUrl: './lecture-recommend-list.component.html',
  styleUrls: ['./lecture-recommend-list.component.css']
})
export class LectureRecommendListComponent implements OnInit {
  @Input() lectures = [];
  @Output() selectLecture = new EventEmitter();
  constructor() {
  }

  ngOnInit(): void {
  }

  // tslint:disable-next-line:typedef
  lectureClicked(lecture) {
    // console.log(lecture);
    this.selectLecture.emit(lecture);
  }

}
