import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../api.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-lecture-review',
  templateUrl: './lecture-review.component.html',
  styleUrls: ['./lecture-review.component.css']
})
export class LectureReviewComponent implements OnInit {

  reviews: any = [];
  selectedReview = null;

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit(): void {
    let thisLectureIdx = +this.route.snapshot.paramMap.get('lectureIdx');

    this.apiService.getLectureReviews(thisLectureIdx).subscribe(
      data => {
        this.reviews = data['result'];
        console.log(this.reviews);
      },
      error => console.log(error)
    );
  }

  write = false;
  goWriteReviewPage(){
    this.write = true;
  }
  writeFinished(){
    this.write = false;
  }
}
