import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';
import { faStar} from '@fortawesome/free-solid-svg-icons';
import {ApiService} from '../../api.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-write-review',
  templateUrl: './write-review.component.html',
  styleUrls: ['./write-review.component.css']
})
export class WriteReviewComponent implements OnInit {
  @Output() finish = new EventEmitter();
  //보내야 하는 값
  /*
  totalrating : number;
  teachingpowerrating : number;
  pricerating : number;
  recommend : CharacterData;
  improvement : string;
  pros = [];
  cons = [];
  */ 
  constructor( private apiService: ApiService, private route: ActivatedRoute) { }
  lectureIdx : number;
  ngOnInit(): void {
    this.lectureIdx = +this.route.snapshot.paramMap.get('lectureIdx');
  }
  star = faStar;
  clickedRate = 0;
  clickedLevel = 0;
  clickedPrice = 0;
  rateHovered = 0;
  levelHovered = 0;
  priceHovered = 0;
  rateHover(rate){
    this.rateHovered = rate;   //마우스 가져가면 별 바뀜
  }
  levelHover(level){
    this.levelHovered = level;   //마우스 가져가면 별 바뀜
  }
  priceHover(price){
    this.priceHovered = price;   //마우스 가져가면 별 바뀜
  }
  rateClicked(rate){
    this.clickedRate= rate;
  }
  levelClicked(level){
    this.clickedLevel = level;
  }
  priceClicked(price){
    this.clickedPrice = price;
  }

  wirteReviewForm = new FormGroup({
    satisfy : new FormControl(''),
    recommend : new FormControl(''),
    improvement : new FormControl(''),
    pros : new FormControl(''),
    cons: new FormControl('')
  })

  cancealWriting(){
    this.clickedRate = 0;
    this.clickedLevel = 0;
    this.clickedPrice = 0;
    this.wirteReviewForm.value.recommend = '';
    this.wirteReviewForm.value.improvement = '';
    this.wirteReviewForm.value.pros = '';
    this.wirteReviewForm.value.cons = '';
    this.finish.emit();
  }
  creatReview(){
    this.apiService.createLectureReviews(
      this.lectureIdx,this.clickedRate, this.clickedLevel, this.clickedPrice, this.wirteReviewForm.value.satisfy,
      this.wirteReviewForm.value.improvement, this.wirteReviewForm.value.pros, this.wirteReviewForm.value.cons
    ).subscribe(
      result => console.log(result),
      error => console.log(error)
    );
    this.finish.emit();
  }
}
