import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import {ApiService} from '../api.service';
import {LectureRecommendDetailComponent} from './lecture-recommend-detail.component';

import {LectureCardModule} from '../lecture-card/lecture-card.module';
import {MainModule} from '../main/main.module';

const routes: Routes = [
  {path: 'lecturerecommenddetail', component: LectureRecommendDetailComponent},
  // {path: 'homenavbar', component: HomeNavBarComponent},
];

@NgModule({
  declarations: [
    LectureRecommendDetailComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    LectureCardModule,
    MainModule
  ],
  exports: [
    RouterModule
  ],
  providers: [
    ApiService
  ]
})
export class LectureRecommendDetailModule { }
