import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';
import {CookieService} from 'ngx-cookie-service';
import {Router, ActivatedRoute} from '@angular/router';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
  constructor( 
    private cookieService: CookieService,
    private router : Router,
    private route : ActivatedRoute,
    private apiService : ApiService
     ) { }
  token : string;
  nickname : string;
  searchtext = "강의 제목 검색하기";
  searchedText : string;
  ngOnInit(): void {
    this.token = this.cookieService.get('token');
    this.searchedText= this.route.snapshot.paramMap.get('keyword');
    if(this.searchedText && this.searchedText!='""'){
      this.searchtext = this.searchedText;
    }

    if(this.token){
      this.apiService.getPersonalInfo().subscribe(
        data => {
          this.nickname = data['result'].nickname;
          console.log(this.nickname);
        },
        error => console.log(error)
      );
    }

  }
  gohome(){
    if(this.router.url.split('/')[1]=='home'){
      window.location.reload();
    }
  }
  
  /*form */
  keyword='';
  searchForm = new FormGroup({
    keywordForm: new FormControl('')
  });
  searchLectures(){
    this.keyword=this.searchForm.value.keywordForm;
    window.location.reload();
  }

  //log out
  logout(){
    //alert('logout');
    this.cookieService.delete('token','/');
    window.location.reload();
    //this.gohome();
  }

}
