import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LectureCardComponent } from './lecture-card.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';


@NgModule({
  declarations: [LectureCardComponent],
  imports: [
    CommonModule,
    FontAwesomeModule
  ],
  exports:[
    LectureCardComponent
  ]
})
export class LectureCardModule { }
