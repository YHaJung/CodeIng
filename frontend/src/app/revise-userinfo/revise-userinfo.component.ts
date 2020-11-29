import { Component, OnInit} from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';
import {ApiService} from '../api.service';
import {faMinusSquare } from '@fortawesome/free-regular-svg-icons';

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
  ischecked = 1;
  deleteIcon = faMinusSquare;
  constructor(private apiService: ApiService) { } 

  levelIdx:number;
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
  });

  profile : any =[];
  personalInfo : any =[];
  mycategoryIdxs : Array<number> = [];
  mysubcategoryIdxs : Array<number> = [];
  
  categories : any = [];
  subcategories : any= [];


  ngOnInit(): void {
    this.apiService.getPersonalInfo().subscribe(
      data => {
        this.personalInfo = data['result'];
        //console.log(this.reviseUserInfoForm.value.id, this.reviseUserInfoForm.value.name, this.reviseUserInfoForm.value.phonenumber, this.reviseUserInfoForm.value.nickname);
      },
      error => console.log(error)
    );
    this.apiService.getProfile().subscribe(
      data => {
        this.profile = data['result'];
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
    console.log(this.profile.category);
  }
  addSubCategory(event){
    this.newcategory = event.target.value.split(',');
    this.profile.subcategory.push({categoryIdx : Number(this.newcategory[0]), categoryName : this.newcategory[1]});
    console.log(this.profile.subcategory);
  }
  index:string;
  deleteCategory(category){
    console.log(this.profile.category);
    this.index = this.profile.category.indexOf(category);
    this.profile.category.splice(this.index, 1);
    console.log(this.profile.category);
  }
  deleteSubCategory(subcategory){
    console.log(this.profile.subcategory);
    this.index = this.profile.subcategory.indexOf(subcategory);
    this.profile.subcategory.splice(this.index, 1);
    console.log(this.profile.subcategory);
  }


  setLevel(event){
    this.levelIdx= event.target.value;
  }

  reviseUserInfo(){
    //회원정보
    if(this.reviseUserInfoForm.value.id) this.personalInfo.email = this.reviseUserInfoForm.value.id;
    if(this.reviseUserInfoForm.value.name) this.personalInfo.name = this.reviseUserInfoForm.value.name;
    if(this.reviseUserInfoForm.value.phonenumber) this.personalInfo.phonenumber = this.reviseUserInfoForm.value.phonenumber;
    if(this.reviseUserInfoForm.value.nickname) this.personalInfo.nickname = this.reviseUserInfoForm.value.nickname;
    this.apiService.patchPersonalInfo(this.personalInfo.email,
                                      this.reviseUserInfoForm.value.pw,
                                      this.reviseUserInfoForm.value.pwCheck,
                                      this.personalInfo.name,
                                      this.personalInfo.phonenumber,
                                      this.personalInfo.nickname
                                      ).subscribe(
      result => {
        console.log(result);
      },
      error => console.log(error)
    );
    //프로필
    if(this.reviseUserInfoForm.value.birth) this.profile.birthday = this.reviseUserInfoForm.value.birth;
    if(this.reviseUserInfoForm.value.school) this.profile.school = this.reviseUserInfoForm.value.school;
    if(this.levelIdx) this.profile.levelIdx = this.levelIdx;
    //if(this.reviseUserInfoForm.value.job) this.profile.job = this.reviseUserInfoForm.value.job;

    if(this.reviseUserInfoForm.value.gender) this.profile.gender = this.reviseUserInfoForm.value.gender;
    for(let category of this.profile.category){
      this.mycategoryIdxs.push(category.categoryIdx);
    }
    for(let subcategory of this.profile.subcategory){
      this.mysubcategoryIdxs.push(subcategory.subcategoryIdx);
    }
    this.apiService.patchProfile(this.profile.birthday,
                                  this.profile.school,
                                  this.profile.levelIdx,
                                  this.profile.job,
                                  this.profile.gender,
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
