import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import {ApiService} from '../api.service';
import {HomeComponent} from '../home/home.component';
import {LectureRankDetailComponent} from '../lecture-rank-detail/lecture-rank-detail.component';
import {LectureRecommendDetailComponent} from './lecture-recommend-detail.component';
import {LectureRecommendComponent} from './lecture-recommend/lecture-recommend.component';
import {AppModule} from '../app.module';

const routes: Routes = [
  {path: 'lecturerecommenddetail', component: LectureRecommendDetailComponent},
  // {path: 'homenavbar', component: HomeNavBarComponent},
];

@NgModule({
  declarations: [
    LectureRecommendDetailComponent,
    LectureRecommendComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    // AppModule
  ],
  exports: [
    RouterModule
  ],
  providers: [
    ApiService
  ]
})
export class LectureRecommendDetailModule { }
