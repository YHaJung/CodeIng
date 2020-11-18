import { Component, EventEmitter, OnInit, Input} from '@angular/core';
import { faStar} from '@fortawesome/free-solid-svg-icons';
//import {Lecture} from '../lecture/lecture';
import {ApiService} from '../api.service';
import {ActivatedRoute} from '@angular/router';//rounter parameter

@Component({
  selector: 'app-lecture-search',
  templateUrl: './lecture-search.component.html',
  styleUrls: ['./lecture-search.component.css']
})
export class LectureSearchComponent implements OnInit {

  lectures:any=[];
  keyword='';
  clickedRate = 0;
  clickedLevel = 0; //제대로 작동x 

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService
  ) { }

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
  rateClicked(rate){
    this.clickedRate= rate;
    this.updateLectures();
  }
  levelClicked(level){
    this.clickedLevel = level;
    this.updateLectures();
  }

  updateLectures(){
    this.apiService.searchLecturesFilter(this.keyword, this.clickedRate, this.clickedLevel).subscribe(
      data => {
        this.lectures = data['result'];
        console.log(this.lectures);
      },
      error => console.log(error)
    );
  }
  
  param1 :string;
  ngOnInit(): void {
    //keyword

    this.keyword = this.route.snapshot.params['keyword'];
    console.log(this.keyword);
    this.apiService.searchLecturesAll(this.keyword).subscribe(
      data => {
        this.lectures = data['result'];
        console.log(this.lectures);
      },
      error => console.log(error)
    );
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
