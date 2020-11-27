import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-lecture-card-small',
  templateUrl: './lecture-card-small.component.html',
  styleUrls: ['./lecture-card-small.component.css']
})
export class LectureCardSmallComponent implements OnInit {
  @Input() lecture;
  constructor() { }

  ngOnInit(): void {
  }

}
