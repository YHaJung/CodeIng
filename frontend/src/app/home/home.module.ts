import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {Routes, RouterModule} from '@angular/router';
import {ApiService} from '../api.service';
import { HomeComponent } from './home.component';
import {SigninComponent } from '../auth/signin/signin.component';
// import {HomeNavBarComponent} from '../home-nav-bar/home-nav-bar.component';
import {FormsModule} from '@angular/forms';

import {HttpClientModule} from "@angular/common/http";
import {MainModule} from "../main/main.module";
import {LectureCardSmallModule} from '../cards/lecture-card-small/lecture-card-small.module';
import {MainNavModule} from '../nav/main-nav/main-nav.module';

const routes: Routes = [
  {path: 'home', component: HomeComponent},
  {path: 'signin', component: SigninComponent},
  {path: 'home/:auth', pathMatch: 'full', redirectTo: 'home'} 
  // {path: 'homenavbar', component: HomeNavBarComponent},
];

@NgModule({
  declarations: [
    HomeComponent,
    // LectureRankDetailComponent
    // LectureRecommendDetailComponent,
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FormsModule,
    HttpClientModule,
    MainModule,
    MainNavModule,
    LectureCardSmallModule
  ],
  exports: [
    RouterModule
  ],
  providers: [
    ApiService
  ]
})
export class HomeModule { }
