import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import { SignupComponent } from './signup.component';


const routes: Routes = [
  {path: 'signup', component: SignupComponent}
];

@NgModule({
  declarations: [SignupComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes)
  ],
  exports: [
    SignupComponent,
    RouterModule
  ]
})
export class SignupModule { }
