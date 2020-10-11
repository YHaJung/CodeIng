import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { faStar } from '@fortawesome/free-solid-svg-icons';
//import {Lecture} from '../lecture/lecture';

@Component({
  selector: 'app-lecture-search',
  templateUrl: './lecture-search.component.html',
  styleUrls: ['./lecture-search.component.css']
})
export class LectureSearchComponent implements OnInit {
  
  
  constructor() { }

  ngOnInit(): void {
  }
  /*stars */
  star = faStar;
  rateHovered = 0;
  levelHovered = 0;
  rateHover(rate){
    this.rateHovered = rate;   //마우스 가져가면 별 바뀜
  }
  levelHover(level){
    this.levelHovered = level;   //마우스 가져가면 별 바뀜
  }


  /*제품 상세로 넘어갈 때 쓰기
  @Output() selectPage = new EventEmitter();
  lecture = [];
  viewReviews(lecture){
    this.selectPage.emit(lecture);
  }
  */

  /*
  postLectureRate(rate, lecture){
  }
  */

}
