import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import { SigninComponent } from './signin.component';
import {ReactiveFormsModule } from '@angular/forms';


const routes: Routes = [
  {path: 'signin', component: SigninComponent}
];

@NgModule({
  declarations: [SigninComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    ReactiveFormsModule 
  ],
  exports: [
    SigninComponent,
    RouterModule
  ]
})
export class SigninModule { }
