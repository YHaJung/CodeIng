import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReviseUserinfoComponent } from './revise-userinfo.component';
import {ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [ReviseUserinfoComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule 
  ],
  exports:[ReviseUserinfoComponent]
})
export class ReviseUserinfoModule { }
