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
  /* input에서 불러온 값이 기본값으로 들어가 있게(수정에서 사용)
  searchForm;

  @Input() set text(val){
    this.searchForm = new FormGroup({
      title: new FormControl(val.title)
  });
  }
  */
  
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
    this.router.navigate(['/']);
    window.location.reload();
  }

}
