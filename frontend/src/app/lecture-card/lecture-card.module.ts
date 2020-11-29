import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LectureCardComponent } from './lecture-card.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {RouterModule} from '@angular/router';



@NgModule({
  declarations: [LectureCardComponent],
  imports: [
    CommonModule,
    FontAwesomeModule,
    RouterModule
  ],
  exports:[
    LectureCardComponent
  ]
})
export class LectureCardModule { }
