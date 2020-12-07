import { Component, EventEmitter, OnInit, Input} from '@angular/core';
import { faStar} from '@fortawesome/free-solid-svg-icons';
import {ApiService} from '../api.service';
import {ActivatedRoute} from '@angular/router';//rounter parameter
import { Options } from '@angular-slider/ngx-slider';

@Component({
  selector: 'app-lecture-search',
  templateUrl: './lecture-search.component.html',
  styleUrls: ['./lecture-search.component.css']
})
export class LectureSearchComponent implements OnInit {

  lectures:any=[];
  keyword='';
  currentRate = 0;
  sendRate = 0;//반올림 별점으로 적용하기 위함
  currentLevel = 6;

  lowPrice = 0;
  highPrice = 200000;
  options: Options = {
    floor: 0,
    ceil: 200000
  };

  pages = [1, 2, 3 ,4, 5];
  currentPage = 1;
  maxPage :number ;/*임시 */

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService
  ) { }

  /*stars */
  star = faStar;
  rateClicked(rate){
    this.currentRate= rate;
    this.searchLectures();
  }
  levelClicked(level){
    this.currentLevel = level;
    this.searchLectures();
  }
  priceClicked(){
    this.searchLectures();
  }

  searchLectures(){
    if(this.currentRate>0.5){
      this.sendRate = this.currentRate - 0.5;
    }else{
      this.sendRate = this.currentRate;
    }
    this.keyword = this.route.snapshot.paramMap.get('keyword');
    console.log('search filter');
    console.log(this.currentPage, this.keyword, this.sendRate, this.currentLevel, this.lowPrice, this.highPrice);
    this.apiService.searchLectures(this.currentPage, this.keyword, this.sendRate, this.currentLevel, this.lowPrice, this.highPrice).subscribe(
      data => {
        this.lectures = data['result'];
       // console.log(this.lectures);
        this.maxPage = data['maxPage'];
        console.log('maxPage :');
        console.log( this.maxPage );
      },
      error => console.log(error)
    );
  }
  
  ngOnInit(): void {
    this.searchLectures();
  }

   //page 선택
  selectPage(page){
    if(page<=this.maxPage){
      this.currentPage = page;
      this.searchLectures();
    }
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
