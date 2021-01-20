import { Component, OnInit, Input } from '@angular/core';
import { faStar, faCircle} from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-lecture-card',
  templateUrl: './lecture-card.component.html',
  styleUrls: ['./lecture-card.component.css']
})
export class LectureCardComponent implements OnInit {
  star = faStar;
  circle = faCircle;
  @Input() lecture;


  constructor() {

  }

  ngOnInit(): void {
  }

}
