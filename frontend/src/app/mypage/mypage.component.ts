import { Component, OnInit } from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-mypage',
  templateUrl: './mypage.component.html',
  styleUrls: ['./mypage.component.css']
})
export class MypageComponent implements OnInit {

  constructor(private apiService: ApiService) { }
  profile:any=[];//name, nickname, email, phonenumber   -- 필수
  personalInfo:any=[];//school, job, level, birthday, gender, category[], subcategory[]    -- 선택
  ngOnInit(): void {
    this.apiService.getPersonalInfo().subscribe(
      data => {
        this.personalInfo = data['result'];
        console.log(this.personalInfo);
      },
      error => console.log(error)
    );
    this.apiService.getProfile().subscribe(
      data => {
        this.profile = data['result'];
        console.log(this.profile);
      },
      error => console.log(error)
    );
  }

}
