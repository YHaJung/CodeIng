import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';
import {CookieService} from 'ngx-cookie-service';
import {Router} from '@angular/router';
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
    private apiService : ApiService
     ) { }
  token : string;
    
  auth : number;
  ngOnInit(): void {
    this.token = this.cookieService.get('token');
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
    this.cookieService.deleteAll();
    this.gohome();
  }

}
