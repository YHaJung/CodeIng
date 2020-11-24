import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LectureSearchComponent } from './lecture-search.component';
import {LectureCardModule} from '../lecture-card/lecture-card.module';
import {MainModule} from '../main/main.module';

import {RouterModule, Routes} from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { NgxSliderModule } from '@angular-slider/ngx-slider';

const routes: Routes = [
  {path: 'lecturesearch/:keyword', component: LectureSearchComponent },
  // {path: 'homenavbar', component: HomeNavBarComponent},
];

@NgModule({
  declarations: [LectureSearchComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FontAwesomeModule,
    LectureCardModule,
    MainModule,
    NgxSliderModule
  ],
  exports: [
    RouterModule
  ],
})
export class LectureSearchModule { }
