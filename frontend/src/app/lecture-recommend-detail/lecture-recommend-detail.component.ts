import { Component, OnInit } from '@angular/core';
import {ApiService} from '../api.service';
import {CookieService}  from 'ngx-cookie-service';

@Component({
  selector: 'app-lecture-recommend-detail',
  templateUrl: './lecture-recommend-detail.component.html',
  styleUrls: ['./lecture-recommend-detail.component.css']
})
export class LectureRecommendDetailComponent implements OnInit {
  constructor(
    private apiService: ApiService,
    private cookieservie: CookieService
  ) { }

  lectures: any = [];
  selectedLecture = null;

  token : string;

  ngOnInit(): void {
    this.token = this.cookieservie.get('token');
    
    this.apiService.getLecturesRecommend().subscribe(
      data => {
        this.lectures = data['result'];
        console.log(this.lectures);
      },
      error => console.log(error)
    );
  }

  // tslint:disable-next-line:typedef
  selectLecture(lecture){
    this.selectedLecture = lecture;
  }

}
