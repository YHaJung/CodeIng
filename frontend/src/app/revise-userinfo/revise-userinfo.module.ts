import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReviseUserinfoComponent } from './revise-userinfo.component';
import {ReactiveFormsModule } from '@angular/forms';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@NgModule({
  declarations: [ReviseUserinfoComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule ,
    FontAwesomeModule 
  ],
  exports:[ReviseUserinfoComponent]
})
export class ReviseUserinfoModule { }
