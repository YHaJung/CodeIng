import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MypageSpecificComponent } from './mypage-specific.component';
import { RouterModule, Routes } from '@angular/router';
import {MainModule} from "../../main/main.module";
import {MypageNavModule} from "../mypage-nav/mypage-nav.module";

const routes: Routes = [
  {path: 'mypage-specific/:mypagekey', component: MypageSpecificComponent}
];

@NgModule({
  declarations: [MypageSpecificComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    MainModule,
    MypageNavModule
  ]
})
export class MypageSpecificModule { }
