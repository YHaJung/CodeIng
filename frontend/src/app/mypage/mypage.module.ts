import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MypageComponent } from './mypage.component';
import {Routes, RouterModule} from '@angular/router';
import {MainModule} from "../main/main.module";
import {MypageNavModule} from "../mypage/mypage-nav/mypage-nav.module";
import {FavoriteLecturesModule} from '../mypage/favorite-lectures/favorite-lectures.module';

const routes: Routes = [
  {path: 'mypage', component: MypageComponent}
];

@NgModule({
  declarations: [MypageComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    MainModule,
    MypageNavModule,
    FavoriteLecturesModule
  ],
  exports: [
    MypageComponent
  ],
})
export class MypageModule { }
