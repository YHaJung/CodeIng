import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MypageComponent } from './mypage.component';
import {Routes, RouterModule} from '@angular/router';
import {MainModule} from "../main/main.module";
import {MypageNavModule} from "../mypage/mypage-nav/mypage-nav.module";

const routes: Routes = [
  {path: 'mypage', component: MypageComponent}
];

@NgModule({
  declarations: [MypageComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    MainModule,
    MypageNavModule
  ],
  exports: [
    RouterModule
  ],
})
export class MypageModule { }
