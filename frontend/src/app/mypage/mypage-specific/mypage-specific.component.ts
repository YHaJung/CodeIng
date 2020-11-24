import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-mypage-specific',
  templateUrl: './mypage-specific.component.html',
  styleUrls: ['./mypage-specific.component.css']
})
export class MypageSpecificComponent implements OnInit {

  constructor(private route: ActivatedRoute, private apiService: ApiService ) { }
  mypagekey = 0;
  profile:any=[];//name, nickname, email, phonenumber   -- 필수
  personalInfo:any=[];//school, job, level, birthday, gender, category[], subcategory[]    -- 선택
  ngOnInit(): void {
    this.mypagekey = +this.route.snapshot.paramMap.get('mypagekey');

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
