import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LectureDetailComponent } from './lecture-detail.component';
import { LectureReviewComponent } from './lecture-review/lecture-review.component';
import { LectureQnaComponent } from './lecture-qna/lecture-qna.component';
import { WriteLectureQnaComponent } from './write-lecture-qna/write-lecture-qna.component';

import {MainModule} from '../main/main.module';
import {ReviewCardModule} from '../cards/review-card/review-card.module';
import {QnaCardModule} from "../cards/qna-card/qna-card.module";

import {RouterModule, Routes} from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {ReactiveFormsModule} from '@angular/forms';
import { NgxSliderModule } from '@angular-slider/ngx-slider';

import { WriteReviewComponent } from './write-review/write-review.component';
import { LectureQnaCommentsComponent } from './lecture-qna-comments/lecture-qna-comments.component';

import {LectureCardSmallModule} from '../cards/lecture-card-small/lecture-card-small.module';

const routes: Routes = [
  {path: 'lecturedetail/:lectureIdx/:page/:subpage', component: LectureDetailComponent },
  // {path: 'homenavbar', component: HomeNavBarComponent},
];

@NgModule({
  declarations: [
    LectureDetailComponent,
    LectureReviewComponent,
    LectureQnaComponent,
    WriteLectureQnaComponent,
    WriteReviewComponent,
    LectureQnaCommentsComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FontAwesomeModule,
    MainModule,
    ReviewCardModule,
    QnaCardModule,
    ReactiveFormsModule,
    NgxSliderModule,
    LectureCardSmallModule
  ],
  exports: [
    RouterModule
  ],
})
export class LectureDetailModule { }
