import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReviewCardComponent } from './review-card.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { AvatarModule } from 'ngx-avatar';


@NgModule({
  declarations: [ReviewCardComponent],
  imports: [
    CommonModule,
    FontAwesomeModule,
    AvatarModule
  ],
  exports: [
    ReviewCardComponent,
  ],
})
export class ReviewCardModule { }
