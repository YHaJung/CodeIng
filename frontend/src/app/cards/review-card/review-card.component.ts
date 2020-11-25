import { Component, OnInit, Input } from '@angular/core';
import { faStar, faEdit, faTrashAlt } from '@fortawesome/free-solid-svg-icons';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-review-card',
  templateUrl: './review-card.component.html',
  styleUrls: ['./review-card.component.css']
})
export class ReviewCardComponent implements OnInit {
  star=faStar;
  edit=faEdit;
  delete=faTrashAlt;
  @Input() review;

  constructor(
    private apiService: ApiService) { }

  ngOnInit(): void {
  }
  editReview(){
    console.log('edit');
  }
  deleteReview(){
    this.apiService.deleteMyReview(this.review.lectureIdx, this.review.reviewIdx).subscribe(
      result => {
        console.log(result);
        window.location.reload();
      },
      error => console.log(error)
    );
  }

}
