import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-myreviews',
  templateUrl: './myreviews.component.html',
  styleUrls: ['./myreviews.component.css']
})
export class MyreviewsComponent implements OnInit {

  constructor(private apiService: ApiService,) { }
  reviews : [];
  //page
  pages = [1, 2, 3 ,4, 5];
  currentPage = 1;
  maxPage=0;
  ngOnInit(): void {
    this.loadReviews();
  }

  loadReviews(){
    this.apiService.getMyReviews(this.currentPage).subscribe(
      data => {
        this.reviews = data['result'];
        console.log(this.reviews);
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
      this.loadReviews();
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
