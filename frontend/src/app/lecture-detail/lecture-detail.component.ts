import { Component, OnInit } from '@angular/core';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import {ActivatedRoute} from '@angular/router';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-lecture-detail',
  templateUrl: './lecture-detail.component.html',
  styleUrls: ['./lecture-detail.component.css']
})
export class LectureDetailComponent implements OnInit {
  star = faStar;

  reviews: any = [];
  avg_rating = 0;
  level = 0;
  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService
  ) { }
  ngOnInit(): void {
    
    this.avg_rating = 3;//this.reviews;
    this.level = 3;
  }


  /*navigation */
  reviewChecked = 1;
  qnaChecked = 0;
  viewReviews(){
    this.reviewChecked = 1;
    this.qnaChecked = 0;
  }
  viewQna(){
    this.qnaChecked = 1;
    this.reviewChecked = 0;
  }

}
