import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
// import { HomeComponent } from './home/home.component';
import { HomeNavBarComponent } from './home-nav-bar/home-nav-bar.component';
import {RouterModule, Routes} from '@angular/router';
import { RecommendationComponent } from './recommendation/recommendation.component';
import {AuthModule} from './auth/auth.module';
import {HomeModule} from './home/home.module';

const appRoutes: Routes = [
  // {path: '', component: HomeComponent},
  {path: 'homenavbar', component: HomeNavBarComponent},
  {path: 'recommendation', component: RecommendationComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    HomeNavBarComponent,
    RecommendationComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AuthModule,
    HomeModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [RouterModule],
  bootstrap: [AppComponent]
})
export class AppModule { }
