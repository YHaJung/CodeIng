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
    this.apiService.signin(this.signinForm.value.id, this.signinForm.value.pw).subscribe(
      result => {
        console.log(result);
      },
      error => console.log(error)
    );
  }

  

  ngOnInit(): void {
  }

}
