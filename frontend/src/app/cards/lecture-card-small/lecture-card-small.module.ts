import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LectureCardSmallComponent } from './lecture-card-small.component';
import {RouterModule} from '@angular/router';



@NgModule({
  declarations: [LectureCardSmallComponent],
  imports: [
    CommonModule,
    RouterModule
  ], exports:[
    LectureCardSmallComponent
  ]
})
export class LectureCardSmallModule { }
