import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import { SignupComponent } from './signup.component';
import {ReactiveFormsModule } from '@angular/forms';

const routes: Routes = [
  {path: 'signup', component: SignupComponent}
];

@NgModule({
  declarations: [SignupComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    ReactiveFormsModule 
  ],
  exports: [
    SignupComponent,
    RouterModule
  ]
})
export class SignupModule { }
