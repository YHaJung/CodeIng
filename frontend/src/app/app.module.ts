import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import {ReactiveFormsModule} from '@angular/forms';

import { AppComponent } from './app.component';

import {RouterModule, Routes} from '@angular/router';

import {HomeModule} from './home/home.module';

import {MypageModule} from './mypage/mypage.module';
import {ReviseUserinfoModule} from './revise-userinfo/revise-userinfo.module';
import {BasketModule} from './basket/basket.module';
import {MypageNavModule} from './mypage/mypage-nav/mypage-nav.module';
import {MypageSpecificModule} from './mypage/mypage-specific/mypage-specific.module';
import {FavoriteLecturesModule} from './mypage/favorite-lectures/favorite-lectures.module';
import {FavoriteSitesModule} from './mypage/favorite-sites/favorite-sites.module';
import {MyreviewsModule} from './mypage/myreviews/myreviews.module';

import {MainModule} from './main/main.module';
import {LectureRecommendDetailModule} from './lecture-recommend-detail/lecture-recommend-detail.module';
import {LectureRankDetailModule} from './lecture-rank-detail/lecture-rank-detail.module';
import {LectureSearchModule} from './lecture-search/lecture-search.module';
import {LectureDetailModule} from './lecture-detail/lecture-detail.module';
import {LectureCardModule} from './lecture-card/lecture-card.module';


import {SigninModule} from './auth/signin/signin.module';
import {SignupModule} from './auth/signup/signup.module';
import { CookieService } from 'ngx-cookie-service';

import {ReviewCardModule} from './cards/review-card/review-card.module';
import {QnaCardModule} from './cards/qna-card/qna-card.module';
import {LectureCardSmallModule} from './cards/lecture-card-small/lecture-card-small.module';

import { AvatarModule } from 'ngx-avatar';

const appRoutes: Routes = [
  {path: '', pathMatch: 'full', redirectTo: 'home'},
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
    ReactiveFormsModule,
    // AppRoutingModule,
    HomeModule,
    MypageModule,
    BasketModule,
    ReviseUserinfoModule,
    MypageNavModule,
    MypageSpecificModule,
    FavoriteLecturesModule,
    FavoriteSitesModule,
    MyreviewsModule,
    MainModule,
    LectureRecommendDetailModule,
    LectureRankDetailModule,
    LectureSearchModule,
    LectureDetailModule,
    LectureCardModule,
    ReviewCardModule,
    QnaCardModule,
    LectureCardSmallModule,
    AvatarModule,
    SigninModule,
    SignupModule,
    HttpClientModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [RouterModule, CookieService ],
  exports: [
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
