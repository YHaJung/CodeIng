import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MyreviewsComponent } from './myreviews.component';
import {ReviewCardModule} from '../../cards/review-card/review-card.module';



@NgModule({
  declarations: [MyreviewsComponent],
  imports: [
    CommonModule,
    ReviewCardModule
  ],
  exports:[
    MyreviewsComponent
  ]
})
export class MyreviewsModule { }
