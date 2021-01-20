import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MypageSpecificComponent } from './mypage-specific.component';
import { RouterModule, Routes } from '@angular/router';
import {MainModule} from "../../main/main.module";
import {MainNavModule} from "../../nav/main-nav/main-nav.module";
import {MypageNavModule} from "../mypage-nav/mypage-nav.module";
import {FavoriteLecturesModule} from '../favorite-lectures/favorite-lectures.module';
import {FavoriteSitesModule} from '../favorite-sites/favorite-sites.module';
import {MyreviewsModule} from '../myreviews/myreviews.module';
import {ReviseUserinfoModule} from '../../revise-userinfo/revise-userinfo.module';

const routes: Routes = [
  {path: 'mypage-specific/:mypagekey', component: MypageSpecificComponent}
];

@NgModule({
  declarations: [MypageSpecificComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    MainModule,
    MainNavModule,
    MypageNavModule,
    FavoriteLecturesModule,
    FavoriteSitesModule,
    MyreviewsModule,
    ReviseUserinfoModule
  ]
})
export class MypageSpecificModule { }
