import { Component, OnInit, Input } from '@angular/core';
import { faStar, faEdit, faTrashAlt, faHeart } from '@fortawesome/free-solid-svg-icons';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-review-card',
  templateUrl: './review-card.component.html',
  styleUrls: ['./review-card.component.css']
})
export class ReviewCardComponent implements OnInit {
  constructor(private apiService: ApiService) { }
  
  star=faStar;
  edit=faEdit;
  delete=faTrashAlt;
  heart=faHeart;

  @Input() review;
  jobString :string;


  ngOnInit(): void {
    switch(this.review.job){
      case 'S' : {
        this.jobString = '초등학생';
        break;
      }
      case 'T' : {
        this.jobString = '중고등학생';
        break;
      }
      case 'D' : {
        this.jobString = '개발자/전공생';
        break;
      }
      case 'N' : {
        this.jobString = '비개발자/비전공생';
        break;
      }

    }
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
