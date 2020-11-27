import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SiteCardComponent } from './site-card.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';



@NgModule({
  declarations: [SiteCardComponent],
  imports: [
    CommonModule,
    FontAwesomeModule 
  ],
  exports:[
    SiteCardComponent
  ]
})
export class SiteCardModule { }
