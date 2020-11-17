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
    gender:new FormControl(''),
    birth:new FormControl(''),
    email:new FormControl(''),
    //phone
    phoneNum:new FormControl(''),
    certificationNum:new FormControl(''),

    /*page1*/
    //nickname
    nickname:new FormControl(''),
    school:new FormControl(''),
    //belong
    major:new FormControl(''),
    job:new FormControl(''),
    //interest
    interestLanguage:new FormControl(''),
    interestField:new FormControl(''),
  });

  phoneNumCheck(){
  }
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
      },
      error => console.log(error)
    );
  }

  

  ngOnInit(): void {
  }

}
