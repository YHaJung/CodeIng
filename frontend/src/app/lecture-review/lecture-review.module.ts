import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LectureReviewComponent } from './lecture-review.component';
import {RouterModule, Routes} from '@angular/router';
import {TabsModule} from '../../tabs/tabs.module';
import {LectureReivewListComponent} from './lecture-reivew-list/lecture-reivew-list.component';
import {LectureQaListComponent} from './lecture-qa-list/lecture-qa-list.component';
import {LectureReviewNavBarComponent} from './lecture-review-nav-bar/lecture-review-nav-bar.component';



const routes: Routes = [
  {path: 'lecturereview/:id', component: LectureReviewComponent},
];

@NgModule({
  declarations: [
    LectureReviewComponent,
    LectureReivewListComponent,
    LectureQaListComponent,
    LectureReviewNavBarComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    TabsModule
  ],
  exports: [
    RouterModule
  ]
})
export class LectureReviewModule { }
