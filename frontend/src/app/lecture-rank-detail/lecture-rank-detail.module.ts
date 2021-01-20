import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import {ApiService} from '../api.service';
import {LectureRankDetailComponent} from './lecture-rank-detail.component';
import {LectureCardModule} from '../lecture-card/lecture-card.module';
import {MainModule} from '../main/main.module';
import {MainNavModule} from '../nav/main-nav/main-nav.module';


const routes: Routes = [
  {path: 'lecturerankdetail', component: LectureRankDetailComponent},
  // {path: 'homenavbar', component: HomeNavBarComponent},
];

@NgModule({
  declarations: [
    LectureRankDetailComponent,

  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    LectureCardModule,
    MainModule,
    MainNavModule
    // AppModule
  ],
  exports: [
    RouterModule,
  ],
  providers: [
    ApiService
  ]
})
export class LectureRankDetailModule { }
