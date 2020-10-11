import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {Routes, RouterModule} from '@angular/router';
import {ApiService} from '../api.service';
import { HomeComponent } from './home.component';
import {SigninComponent } from '../auth/signin/signin.component';
// import {HomeNavBarComponent} from '../home-nav-bar/home-nav-bar.component';
import { LectureRankListComponent } from './lecture-rank-list/lecture-rank-list.component';
import { LectureRecommendListComponent } from './lecture-recommend-list/lecture-recommend-list.component';
import {HomeNavBarComponent} from './home-nav-bar/home-nav-bar.component';
import {FormsModule} from '@angular/forms';

import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MainModule} from "../main/main.module";


const routes: Routes = [
  {path: 'home', component: HomeComponent},
  {path: 'signin', component: SigninComponent}
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
    FormsModule,
    HttpClientModule,
    MainModule
  ],
  exports: [
    RouterModule
  ],
  providers: [
    ApiService
  ]
})
export class HomeModule { }
