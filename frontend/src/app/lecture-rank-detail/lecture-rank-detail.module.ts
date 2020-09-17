import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import {ApiService} from '../api.service';
import {HomeComponent} from '../home/home.component';
import {LectureRankDetailComponent} from './lecture-rank-detail.component';
import {LectureRankComponent} from './lecture-rank/lecture-rank.component';
import {AppModule} from '../app.module';

const routes: Routes = [
  {path: 'lecturerankdetail', component: LectureRankDetailComponent},
  // {path: 'homenavbar', component: HomeNavBarComponent},
];

@NgModule({
  declarations: [
    LectureRankDetailComponent,
    LectureRankComponent
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
export class LectureRankDetailModule { }
