import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-lecture-review',
  templateUrl: './lecture-review.component.html',
  styleUrls: ['./lecture-review.component.css']
})
export class LectureReviewComponent implements OnInit {

  paramId: string;

  constructor(route: ActivatedRoute) {
    this.paramId = route.snapshot.params.id;
  }

  ngOnInit(): void {
  }

}
