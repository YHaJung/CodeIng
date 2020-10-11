import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent{
  title = 'CodeIng';
  mainFlag = 1;
  signinFlag = 0;
  signupFlag = 0;


}
