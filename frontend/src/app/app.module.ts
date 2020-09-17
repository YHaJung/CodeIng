import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import {RouterModule, Routes} from '@angular/router';
import {AuthModule} from './auth/auth.module';
import {HomeModule} from './home/home.module';
import {LectureReviewModule} from './lecture-review/lecture-review.module';

import {LectureRecommendDetailModule} from './lecture-recommend-detail/lecture-recommend-detail.module';
import {LectureRankDetailModule} from './lecture-rank-detail/lecture-rank-detail.module';



const appRoutes: Routes = [
  {path: '', pathMatch: 'full', redirectTo: ''},
  {path: 'lecturereview/:id', redirectTo: 'lecturereview/'},
  {path: 'lectureqa/:id', redirectTo: 'lectureqa/'},
  // {path: 'lecturerankdetail', component: LectureRankDetailComponent},
  // {path: 'lecturerecommenddetail', component: LectureRecommendDetailComponent},
  // {path: 'mainnavbar', component: MainNavBarComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    // LectureRankDetailComponent,
    // LectureRecommendDetailComponent,
    // LectureReviewNavBarComponent,
    // MainNavBarComponent,
    // LectureRankComponent,
    // LectureRecommendComponent,
  ],
  imports: [
    BrowserModule,
    // AppRoutingModule,
    AuthModule,
    HomeModule,
    LectureReviewModule,
    LectureRecommendDetailModule,
    LectureRankDetailModule,
    HttpClientModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [RouterModule],
  exports: [
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
