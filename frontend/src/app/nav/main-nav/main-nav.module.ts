import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MainNavComponent } from './main-nav.component';



@NgModule({
  declarations: [MainNavComponent],
  imports: [
    CommonModule
  ],
  exports:[
    MainNavComponent
  ]
})
export class MainNavModule { }
