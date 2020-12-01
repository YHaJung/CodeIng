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

  personalInfo : any =[];
  profile : any = [];
  profilePrint : any = [];/*profile은 전송값이랑 화면 출력값 다른 경우가 많음 */

  /*select - 수준, 카테고리 */
  levelIdx:number;
  mycategoryIdxs : Array<number> = [];
  mysubcategoryIdxs : Array<number> = [];
  
  categories : any = [];
  subcategories : any= [];

  /*profile 수정여부 */
  isReviseAdditionalInfo = 0;

  reviseUserInfoForm = new FormGroup({
    /*personal info */
    pw: new FormControl(''),
    pwCheck:new FormControl(''),
    name:new FormControl(''),
    phonenumber:new FormControl(''),
    nickname:new FormControl(''),
    /*profile */
    birth:new FormControl(''),
    gender:new FormControl('C'), /*초기값 안뜨게 하기위함 */
    school:new FormControl(''),
    job:new FormControl(''),
  });

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
        /*좌측 출력 위해 */
        if(this.profile.birthday == "None") this.profilePrint.birthday = "선택안함";
        else this.profilePrint.birthday = this.profile.birthday;

        if(this.profile.gender == 'W') this.profilePrint.gender = "여성";
        else if(this.profile.gender == 'M') this.profilePrint.gender = "남성";
        else this.profilePrint.gender = "선택안함";

        if(this.profile.school == null) this.profilePrint.school = "선택안함";
        else this.profilePrint.school = this.profile.school;

        if(this.profile.job == "S") this.profilePrint.job = "초등학생";
        else if(this.profile.job == "T") this.profilePrint.job = "중고등학생";
        else if(this.profile.job == "D") this.profilePrint.job = "전공자/개발직군";
        else if(this.profile.job == "N") this.profilePrint.job = "비전공자/비개발직군";
        else  this.profilePrint.job = "선택안함";
        
      },
      error => console.log(error)
    );
    this.apiService.getCategoryList().subscribe(
      data => {
        this.categories= data['result'];
      },
      error => console.log(error)
    );
    this.apiService.getSubcategoryList().subscribe(
      data => {
        this.subcategories = data['result'];
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
    this.profile.subcategory.push({subcategoryIdx : Number(this.newcategory[0]), subcategoryName : this.newcategory[1]});
    console.log(this.profile.subcategory);
  }
  index:string;
  deleteCategory(category){
    this.reviseAdditionalInfo();
    console.log(this.profile.category);
    this.index = this.profile.category.indexOf(category);
    this.profile.category.splice(this.index, 1);
    console.log(this.profile.category);
  }
  deleteSubCategory(subcategory){
    this.reviseAdditionalInfo();
    console.log(this.profile.subcategory);
    this.index = this.profile.subcategory.indexOf(subcategory);
    this.profile.subcategory.splice(this.index, 1);
    console.log(this.profile.subcategory);
  }


  setLevel(event){
    this.levelIdx= event.target.value;
  }
  reviseAdditionalInfo(){
    this.isReviseAdditionalInfo = 1;
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
    if(this.isReviseAdditionalInfo == 1){
      if(this.reviseUserInfoForm.value.birth) this.profile.birthday = this.reviseUserInfoForm.value.birth;
      if(this.reviseUserInfoForm.value.school) this.profile.school = this.reviseUserInfoForm.value.school;
      if(this.levelIdx) this.profile.levelIdx = this.levelIdx;
      if(this.reviseUserInfoForm.value.job) this.profile.job = this.reviseUserInfoForm.value.job;

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

}
