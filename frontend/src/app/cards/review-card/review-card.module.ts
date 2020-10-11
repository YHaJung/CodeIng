import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReviewCardComponent } from './review-card.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';



@NgModule({
  declarations: [ReviewCardComponent],
  imports: [
    CommonModule,
    FontAwesomeModule 
  ],
  exports:[
    ReviewCardComponent
  ]
})
export class ReviewCardModule { }
