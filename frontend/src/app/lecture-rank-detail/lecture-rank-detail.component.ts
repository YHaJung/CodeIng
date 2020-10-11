import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-lecture-rank-detail',
  templateUrl: './lecture-rank-detail.component.html',
  styleUrls: ['./lecture-rank-detail.component.css']
})
export class LectureRankDetailComponent implements OnInit {


  allLectures: any = [];
  subcategories:any=[];
  categoryLectures:any=[];
  selectedLecture = null;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.apiService.getLectures().subscribe(
      data => {
        this.allLectures = data;
        console.log(this.allLectures);
      },
      error => console.log(error)
    );
    this.apiService.getLecturesRanking().subscribe(
      data => {
        this.subcategories = data['subcategory'];
        console.log(data);
      },
      error => console.log(error)
    );
    this.apiService.getLecturesRanking().subscribe(
      data => {
        this.categoryLectures = data['result'];
        console.log(this.categoryLectures);
      },
      error => console.log(error)
    );
  }

  // tslint:disable-next-line:typedef
  /*
  selectLecture(allLecture){
    this.selectedLecture = allLecture;
  }
  */
}
