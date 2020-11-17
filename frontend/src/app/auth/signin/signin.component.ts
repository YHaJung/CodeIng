import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent implements OnInit {
  constructor(private apiService:ApiService) { }
  signinForm = new FormGroup({
    id: new FormControl(''),
    pw: new FormControl('')
  });
  user:[];
  login(){
    console.log(this.signinForm.value);
    this.apiService.signin('suyeon7979@gmail.com','afsasag123!').subscribe(
      data => {
        this.user = data['token'];
        console.log('token:');
        console.log(this.user);
      },
      error => console.log(error)
    );
  }

  

  ngOnInit(): void {
  }

}
