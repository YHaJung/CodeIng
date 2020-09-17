import { Component, OnInit } from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  lectures: any = [];
  selectedLecture = null;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.apiService.getLectures().subscribe(
      data => {
        this.lectures = data;
      },
      error => console.log(error)
    );
  }

  // tslint:disable-next-line:typedef
  selectLecture(lecture){
    this.selectedLecture = lecture;
  }

}
