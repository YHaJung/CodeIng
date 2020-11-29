import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-lecture-rank-detail',
  templateUrl: './lecture-rank-detail.component.html',
  styleUrls: ['./lecture-rank-detail.component.css']
})

export class LectureRankDetailComponent implements OnInit {
  subcategories :any =[];
  categories :any=[];
  lectures:any=[];
  lectureIdxs=[1, 2, 3, 4, 5];

  pages = [1, 2, 3 ,4, 5];
  currentPage = 1;
  currentCategoryIdx = 0;
  currentSubCategoryIdx = 0;

  allLectures: any = [];
  
  categoryLectures:any=[];
  selectedLecture = null;

  subcategoryNum = 10;

  getMoreSubcategory(){
    this.subcategoryNum += 10;
  }

  constructor(private apiService: ApiService) { }

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
        console.log('lectures :');
        console.log(this.lectures);
      },
      error => console.log(error)
    );
  }
  //카테고리 선택
  selectCategory(index:number){
    this.currentCategoryIdx = index;
    this.currentPage = 1;
    this.loadLectures();
  }
  selectSubCategory(index:number){
    this.currentSubCategoryIdx = index;
    this.currentPage = 1;
    this.loadLectures();
  }
  //page 선택
  selectPage(page){
    this.currentPage = page;
    this.loadLectures();
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
