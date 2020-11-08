import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
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

  

  ngOnInit(): void {
  }

}
