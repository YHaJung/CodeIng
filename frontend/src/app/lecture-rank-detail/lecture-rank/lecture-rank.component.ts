import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-lecture-rank',
  templateUrl: './lecture-rank.component.html',
  styleUrls: ['./lecture-rank.component.css']
})
export class LectureRankComponent implements OnInit {

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
