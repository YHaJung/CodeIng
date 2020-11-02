import { NgModule} from '@angular/core';
import { CommonModule } from '@angular/common';
import { QnaCardComponent } from './qna-card.component';
import { AvatarModule } from 'ngx-avatar';

@NgModule({
  declarations: [QnaCardComponent],
  imports: [
    CommonModule,
    AvatarModule
  ],
  exports:[
    QnaCardComponent
  ]
})
export class QnaCardModule { }
