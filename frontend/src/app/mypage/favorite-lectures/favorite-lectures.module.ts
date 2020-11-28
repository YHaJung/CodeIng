import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FavoriteLecturesComponent } from './favorite-lectures.component';
import {LectureCardModule} from '../../lecture-card/lecture-card.module';
import {RouterModule, Routes} from '@angular/router';
import {LectureCardMiddleModule} from '../../cards/lecture-card-middle/lecture-card-middle.module';

const routes: Routes = [];

@NgModule({
  declarations: [FavoriteLecturesComponent],
  imports: [
    CommonModule,
    LectureCardModule,
    RouterModule.forChild(routes),
    LectureCardMiddleModule
  ],
  exports:[
    FavoriteLecturesComponent ,
    RouterModule,
  ]
})
export class FavoriteLecturesModule { }
