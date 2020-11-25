import { Component, OnInit} from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';
import {ApiService} from '../api.service';

interface Category{
  categoryIdx : number,
  categoryName : string
}

@Component({
  selector: 'app-revise-userinfo',
  templateUrl: './revise-userinfo.component.html',
  styleUrls: ['./revise-userinfo.component.css']
})

export class ReviseUserinfoComponent implements OnInit {
  test = 1;
  constructor(private apiService: ApiService) { } 

  reviseUserInfoForm = new FormGroup({
    /*page0*/
    //id-pw
    id: new FormControl(''),//email
    pw: new FormControl(''),
    pwCheck:new FormControl(''),
    //personal info
    name:new FormControl(''),
    gender:new FormControl(''),
    birth:new FormControl(''),

    //phone
    phonenumber:new FormControl(''),
    
    //certificationNum:new FormControl(''),

    /*page1*/
    //nickname
    nickname:new FormControl(''),
    school:new FormControl(''),
    //belong
    job:new FormControl(''),
    //interest
    interestLanguage:new FormControl(''),
    interestField:new FormControl(''),
  });

  profile : any =[];
  personalInfo : any =[];
  mycategoryIdxs : Array<number> = [];
  mysubcategoryIdxs : Array<number> = [];
  
  categories : any =[];
  subcategories : any=[];


  ngOnInit(): void {
    this.apiService.getPersonalInfo().subscribe(
      data => {
        this.personalInfo = data['result'];
        console.log('personalInfo:');
        console.log(this.personalInfo);
      },
      error => console.log(error)
    );
    this.apiService.getProfile().subscribe(
      data => {
        this.profile = data['result'];
        //this.profile.category.push({categoryIdx:1, categoryName:'Ajsx'})
        console.log('profile');
        console.log( this.profile);
      },
      error => console.log(error)
    );
    this.apiService.getCategoryList().subscribe(
      data => {
        this.categories= data['result'];
        console.log('category :');
        console.log(this.categories);
      },
      error => console.log(error)
    );
    this.apiService.getSubcategoryList().subscribe(
      data => {
        this.subcategories = data['result'];
        console.log('subcategories');
        console.log(this.subcategories);
      },
      error => console.log(error)
    );
  }
  newcategory=[];
  addCategory(event){

    this.newcategory = event.target.value.split(',');
    this.profile.category.push({categoryIdx : Number(this.newcategory[0]), categoryName : this.newcategory[1]});
    this.mycategoryIdxs.push(Number(this.newcategory[0]));
    console.log(this.profile.category);
  }
  addSubCategory(event){
    this.newcategory = event.target.value.split(',');
    this.profile.subcategory.push({categoryIdx : Number(this.newcategory[0]), categoryName : this.newcategory[1]});
    this.mysubcategoryIdxs.push(Number(this.newcategory[0]));
    console.log(this.profile.subcategory);
  }

  reviseUserInfo(){
    this.apiService.patchPersonalInfo(this.reviseUserInfoForm.value.id,
                                      this.reviseUserInfoForm.value.pw,
                                      this.reviseUserInfoForm.value.pwCheck,
                                      this.reviseUserInfoForm.value.name,
                                      this.reviseUserInfoForm.value.phonenumber,
                                      this.reviseUserInfoForm.value.nickname
                                      ).subscribe(
      result => {
        console.log(result);
      },
      error => console.log(error)
    );
    this.apiService.patchProfile(this.reviseUserInfoForm.value.birth,
                                  this.reviseUserInfoForm.value.school,
                                  this.reviseUserInfoForm.value.level,
                                  this.reviseUserInfoForm.value.job,
                                  this.reviseUserInfoForm.value.gender,
                                  this.mysubcategoryIdxs,
                                  this.mycategoryIdxs
                                  ).subscribe(
      result => {
      console.log(result);
      },
      error => console.log(error)
      );
    
  }

}
