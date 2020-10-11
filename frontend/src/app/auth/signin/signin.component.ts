import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent implements OnInit {

  signinForm = new FormGroup({
    id: new FormControl(''),
    pw: new FormControl('')
  });

  saveForm(){
    console.log(this.signinForm.value);
  }

  constructor() { }

  ngOnInit(): void {
  }

}
