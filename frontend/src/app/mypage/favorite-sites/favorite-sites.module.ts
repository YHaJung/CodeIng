import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FavoriteSitesComponent } from './favorite-sites.component';
import {SiteCardModule} from '../../cards/site-card/site-card.module';



@NgModule({
  declarations: [FavoriteSitesComponent],
  imports: [
    CommonModule,
    SiteCardModule
  ],
  exports:[
    FavoriteSitesComponent
  ]
})
export class FavoriteSitesModule { }
