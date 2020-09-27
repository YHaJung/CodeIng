import { Component, OnInit } from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  lectures: any = [];
  rankingdoverview: any = [];
  recommendoverview: any = [];
  selectedLecture = null;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    // this.apiService.getLectures().subscribe(
    //   data => {
    //     this.lectures = data['result'];
    //     console.log(this.lectures);
    //   },
    //   error => console.log(error)
    // );
    this.apiService.getRankingOverview()
      .subscribe(
      data => {
        this.rankingdoverview = data['result'];
      },
      error => console.log(error)
    );
    this.apiService.getRecommendOverview()
      .subscribe(
        data => {
          this.recommendoverview = data['result'];
          // console.log(this.recommendoverview);
        },
        error => console.log(error)
      );
  }

  // tslint:disable-next-line:typedef
  selectLecture(lecture){
    this.selectedLecture = lecture;
  }

}
