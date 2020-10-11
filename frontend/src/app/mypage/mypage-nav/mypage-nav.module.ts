import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MypageNavComponent } from './mypage-nav.component';



@NgModule({
  declarations: [MypageNavComponent],
  imports: [
    CommonModule
  ],
  exports:[
    MypageNavComponent 
  ]
})
export class MypageNavModule { }
