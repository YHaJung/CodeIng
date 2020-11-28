import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LectureCardMiddleComponent } from './lecture-card-middle.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';



@NgModule({
  declarations: [LectureCardMiddleComponent],
  imports: [
    CommonModule,
    FontAwesomeModule 
  ],
  exports:[
    LectureCardMiddleComponent
  ]
})
export class LectureCardMiddleModule { }
