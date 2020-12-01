import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  page = 0;

  constructor(private apiService:ApiService) { }
  signupForm = new FormGroup({
    /*page0*/
    //id-pw
    id: new FormControl(''),//email
    pw: new FormControl(''),
    pwCheck:new FormControl(''),
    //personal info
    name:new FormControl(''),
    //phone
    phoneNum:new FormControl(''),
    

    /*page1*/
    //nickname
    nickname:new FormControl(''),
    school:new FormControl(''),
  });

  //phoneNumCheck(){}
  next(){   //'다음'버튼
    this.page=1;
  }
  back(){   //'이전'버튼
    this.page=0;
  }
  singup(){
    console.log(this.signupForm.value);
    //email:string, userpwd:string, userpwdConfirm:string, name:string, phonenumber:string, nickname:string
    this.apiService.signup(
        this.signupForm.value.id,
        this.signupForm.value.pw,
        this.signupForm.value.pwCheck,
        this.signupForm.value.name,
        this.signupForm.value.phoneNum,
        this.signupForm.value.nickname
      ).subscribe(
      result => {
        console.log(result);
        var signin = confirm('회원가입에 성공하셨습니다. \n로그인하러 가시겠습니까?');
        if(signin){
          window.location.href="/signin";
        }else{
          window.location.href="/home";
        }
        
      },
      error => {
        console.log(error);
        alert(error.error.message);
      }
    );
  }

  ngOnInit(): void {
  }

}
