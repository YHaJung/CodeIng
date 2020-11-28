import { Component, OnInit, Input } from '@angular/core';
import { faHeart } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-lecture-card-middle',
  templateUrl: './lecture-card-middle.component.html',
  styleUrls: ['./lecture-card-middle.component.css']
})
export class LectureCardMiddleComponent implements OnInit {
  @Input() lecture;
  heart=faHeart;
  constructor() { }

  ngOnInit(): void {
  }

}
