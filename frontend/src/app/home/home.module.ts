import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {Routes, RouterModule} from '@angular/router';
import {ApiService} from '../api.service';
import { HomeComponent } from './home.component';
// import {HomeNavBarComponent} from '../home-nav-bar/home-nav-bar.component';
import { LectureRankListComponent } from './lecture-rank-list/lecture-rank-list.component';
import { LectureRecommendListComponent } from './lecture-recommend-list/lecture-recommend-list.component';
import { LectureRecommendDetailComponent } from '../lecture-recommend-detail/lecture-recommend-detail.component';
import { LectureRankDetailComponent } from '../lecture-rank-detail/lecture-rank-detail.component';
import {HomeNavBarComponent} from './home-nav-bar/home-nav-bar.component';
import {FormsModule} from '@angular/forms';

const routes: Routes = [
  {path: '', component: HomeComponent},
  // {path: 'homenavbar', component: HomeNavBarComponent},
];

@NgModule({
  declarations: [
    HomeComponent,
    HomeNavBarComponent,
    // LectureRankDetailComponent,
    LectureRankListComponent,
    // LectureRecommendDetailComponent,
    LectureRecommendListComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FormsModule
  ],
  exports: [
    RouterModule
  ],
  providers: [
    ApiService
  ]
})
export class HomeModule { }
