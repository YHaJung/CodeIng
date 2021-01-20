import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../api.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-favorite-lectures',
  templateUrl: './favorite-lectures.component.html',
  styleUrls: ['./favorite-lectures.component.css']
})
export class FavoriteLecturesComponent implements OnInit {

  constructor(private apiService: ApiService, private route: ActivatedRoute) { }

  lectures = [];
  //page
  pages = [1, 2, 3 ,4, 5];
  currentPage = 1;
  maxPage=0;
  ngOnInit(): void {
    this.loadLectures();
  }

  loadLectures(){
    this.apiService.getFavoriteLectures(this.currentPage).subscribe(
      data => {
        this.lectures = data['result'];
        console.log('favorite-lecture');
        console.log(this.lectures);
        //maxpage 불러오기
        this.maxPage = data['maxPage'];
        console.log('maxPage :');
        console.log( this.maxPage );
      },
      error => console.log(error)
    );
  }

  //page 선택
  selectPage(page){
    if(page<=this.maxPage){
      this.currentPage = page;
      this.loadLectures();
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
