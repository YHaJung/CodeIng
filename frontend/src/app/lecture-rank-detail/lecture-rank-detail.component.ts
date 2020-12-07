import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-lecture-rank-detail',
  templateUrl: './lecture-rank-detail.component.html',
  styleUrls: ['./lecture-rank-detail.component.css']
})

export class LectureRankDetailComponent implements OnInit {
  constructor(private apiService: ApiService) { }
  
  lectures:any=[];
  
  //page
  pages = [1, 2, 3 ,4, 5];
  currentPage = 1;
  maxPage=1;
  
  //category
  subcategories :any =[];
  categories :any=[];
  currentCategoryIdx = 0;
  currentSubCategoryIdx = 0;
  currentCategoryName = "전체";
  currentSubCategoryName = "전체";

 //...눌러서 언어 개수 늘리기에 사용
  subcategoryNum = 10;

  //...눌러서 언어 개수 늘리기
  getMoreSubcategory(){
    this.subcategoryNum += 10;
  }

  ngOnInit(): void {
    this.loadLectures();
    this.apiService.getSubcategoryList().subscribe(
      data => {
        this.subcategories = data['result'];
        console.log('sub categories :');
        console.log(this.subcategories);
      },
      error => console.log(error)
    );
    this.apiService.getCategoryList().subscribe(
      data => {
        this.categories= data['result'] ;
        console.log('categories :');
        console.log(this.categories);
      },
      error => console.log(error)
    );
  }

  loadLectures(){
    this.apiService.getALLLecturesRanking(this.currentPage, this.currentCategoryIdx , this.currentSubCategoryIdx).subscribe(
      data => {
        this.lectures = data['result'];
        console.log(this.lectures);

        this.maxPage = data['maxPage'];
        console.log('maxPage :');
        console.log( this.maxPage );
      },
      error => console.log(error)
    );
  }
  //카테고리 선택
  selectCategory(category){
    this.currentCategoryIdx = category.categoryIdx;
    this.currentCategoryName = category.categoryName;
    this.pages=[1,2,3,4,5];
    this.currentPage = 1;
    this.loadLectures();
  }
  selectSubCategory(subcategory){
    this.currentSubCategoryIdx = subcategory.subcategoryIdx;
    this.currentSubCategoryName = subcategory.subcategoryName;
    this.currentPage = 1;
    this.pages=[1,2,3,4,5];
    this.loadLectures();
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
