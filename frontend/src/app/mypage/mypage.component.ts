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

  withdrawal(){
    var withdrawCheck = confirm("회원탈퇴 시 개인화된 추천을 위한 정보가 모두 초기화됩니다.\n 정말 탈퇴하시겠습니까?");
    if(withdrawCheck){
      this.apiService.withdrawal().subscribe(
      result => {
        console.log(result);
        alert('회원탈퇴를 완료하였습니다.');
      },
      error => console.log(error)
    );
    }
    
  }

}
