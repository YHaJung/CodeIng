import { Component, OnInit, Input } from '@angular/core';
import { faStar} from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-lecture-card',
  templateUrl: './lecture-card.component.html',
  styleUrls: ['./lecture-card.component.css']
})
export class LectureCardComponent implements OnInit {
  star = faStar;
  @Input() lecture;


  constructor() {

  }

  ngOnInit(): void {

  }

}
