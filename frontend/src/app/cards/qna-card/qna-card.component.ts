import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-qna-card',
  templateUrl: './qna-card.component.html',
  styleUrls: ['./qna-card.component.css']
})
export class QnaCardComponent implements OnInit {
  @Input() qna;
  constructor() { }

  ngOnInit(): void {
  }

}
