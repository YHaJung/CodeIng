import { Component, EventEmitter, OnInit, Input} from '@angular/core';
import { faStar} from '@fortawesome/free-solid-svg-icons';
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
  currentRate = 0;
  currentLevel = 0;
  currentPrice = 0;
  pages = [1, 2, 3 ,4, 5];
  currentPage = 1;

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService
  ) { }

  /*stars */
  star = faStar;
  rateHovered = 0;
  levelHovered = 0;
  priceHovered = 0;
  rateHover(rate){
    this.rateHovered = rate;   //마우스 가져가면 별 바뀜
  }
  levelHover(level){
    this.levelHovered = level;   //마우스 가져가면 별 바뀜
  }
  priceHover(price){
    this.priceHovered = price;   //마우스 가져가면 별 바뀜
  }
  rateClicked(rate){
    this.currentRate= rate;
    this.searchLectures();
  }
  levelClicked(level){
    this.currentLevel = level;
    this.searchLectures();
  }
  priceClicked(price){
    this.currentPrice = price;
    this.searchLectures();
  }

  searchLectures(){
    this.keyword = this.route.snapshot.paramMap.get('keyword');
    console.log(this.currentPage, this.keyword, this.currentRate, this.currentLevel, this.currentPrice*20000);
    this.apiService.searchLectures(this.currentPage, this.keyword, this.currentRate, this.currentLevel, this.currentPrice*20000).subscribe(
      data => {
        this.lectures = data['result'];
        console.log(this.lectures);
      },
      error => console.log(error)
    );
  }
  
  ngOnInit(): void {
    this.searchLectures();
  }

  selectPage(page){
    this.currentPage = page;
    this.searchLectures();
  }
  pageMinusJump(){
    if(this.pages[0]!=1){
      this.pages[0] -= 5;
      this.pages[1] -= 5;
      this.pages[2] -= 5;
      this.pages[3] -= 5;
      this.pages[4] -= 5;
    }
  }
  pagePlusJump(){
    this.pages[0] += 5;
    this.pages[1] += 5;
    this.pages[2] += 5;
    this.pages[3] += 5;
    this.pages[4] += 5;
  }
}
