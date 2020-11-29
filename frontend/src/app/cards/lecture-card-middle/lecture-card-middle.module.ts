import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LectureCardMiddleComponent } from './lecture-card-middle.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {RouterModule} from '@angular/router';



@NgModule({
  declarations: [LectureCardMiddleComponent],
  imports: [
    CommonModule,
    FontAwesomeModule,
    RouterModule
  ],
  exports:[
    LectureCardMiddleComponent
  ]
})
export class LectureCardMiddleModule { }
