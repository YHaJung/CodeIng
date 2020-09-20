import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-lecture-recommend',
  templateUrl: './lecture-recommend.component.html',
  styleUrls: ['./lecture-recommend.component.css']
})
export class LectureRecommendComponent implements OnInit {

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
