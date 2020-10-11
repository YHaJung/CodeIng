import { NgModule} from '@angular/core';
import { CommonModule } from '@angular/common';
import { QnaCardComponent } from './qna-card.component';

@NgModule({
  declarations: [QnaCardComponent],
  imports: [
    CommonModule
  ],
  exports:[
    QnaCardComponent
  ]
})
export class QnaCardModule { }
