import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LectureCardSmallComponent } from './lecture-card-small.component';



@NgModule({
  declarations: [LectureCardSmallComponent],
  imports: [
    CommonModule
  ], exports:[
    LectureCardSmallComponent
  ]
})
export class LectureCardSmallModule { }
