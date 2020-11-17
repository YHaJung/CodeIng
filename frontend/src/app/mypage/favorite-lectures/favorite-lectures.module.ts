import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FavoriteLecturesComponent } from './favorite-lectures.component';



@NgModule({
  declarations: [FavoriteLecturesComponent],
  imports: [
    CommonModule
  ],
  exports:[
    FavoriteLecturesComponent  
  ]
})
export class FavoriteLecturesModule { }
