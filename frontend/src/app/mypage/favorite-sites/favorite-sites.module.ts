import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FavoriteSitesComponent } from './favorite-sites.component';



@NgModule({
  declarations: [FavoriteSitesComponent],
  imports: [
    CommonModule
  ],
  exports:[
    FavoriteSitesComponent
  ]
})
export class FavoriteSitesModule { }
