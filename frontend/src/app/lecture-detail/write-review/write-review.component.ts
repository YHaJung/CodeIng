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
  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    ) { }
  lectureIdx : number;
  user :any =[];
  ngOnInit(): void {
    this.lectureIdx = +this.route.snapshot.paramMap.get('lectureIdx');
 
    this.apiService.getPersonalInfo().subscribe(
      data => {
        this.user = data['result'];
        console.log(this.user);
      },
      error => console.log(error)
    );
  }
  star = faStar;
  clickedRate :number;
  clickedLevel :number;
  clickedPrice :number;
  rateClicked(rate){
    this.clickedRate= rate;
  }
  levelClicked(level){
    this.clickedLevel = level;
  }
  priceClicked(price){
    this.clickedPrice = price;
  }
  
  pros : Array<number> =[];
  cons : Array<number>=[];
  wirteReviewForm = new FormGroup({
    satisfy : new FormControl(''),
    recommend : new FormControl(''),
    improvement : new FormControl(''),
    pro1 : new FormControl(''),
    pro2 : new FormControl(''),
    pro3 : new FormControl(''),
    pro4 : new FormControl(''),
    pro5 : new FormControl(''),
    pro6 : new FormControl(''),

    con1: new FormControl(''),
    con2: new FormControl(''),
    con3: new FormControl(''),
    con4: new FormControl(''),
    con5: new FormControl(''),
    con6: new FormControl(''),
    con7: new FormControl(''),
    con8: new FormControl(''),
  })

  cancealWriting(){
    window.location.href="/lecturedetail/"+this.lectureIdx+"/review/view";
  }
  creatReview(){
    if(this.wirteReviewForm.value.pro1) this.pros.push(1);
    if(this.wirteReviewForm.value.pro2) this.pros.push(2);
    if(this.wirteReviewForm.value.pro3) this.pros.push(3);
    if(this.wirteReviewForm.value.pro4) this.pros.push(4);
    if(this.wirteReviewForm.value.pro5) this.pros.push(5);
    if(this.wirteReviewForm.value.pro6) this.pros.push(6);

    if(this.wirteReviewForm.value.con1) this.cons.push(1);
    if(this.wirteReviewForm.value.con2) this.cons.push(2);
    if(this.wirteReviewForm.value.con3) this.cons.push(3);
    if(this.wirteReviewForm.value.con4) this.cons.push(4);
    if(this.wirteReviewForm.value.con5) this.cons.push(5);
    if(this.wirteReviewForm.value.con6) this.cons.push(6);
    if(this.wirteReviewForm.value.con7) this.cons.push(7);
    if(this.wirteReviewForm.value.con8) this.cons.push(8);

    this.apiService.createLectureReviews(
      this.lectureIdx,this.clickedRate, this.clickedLevel, this.clickedPrice, this.wirteReviewForm.value.satisfy,
      this.wirteReviewForm.value.improvement, this.pros, this.cons
    ).subscribe(
      result => {
        window.location.href="/lecturedetail/"+this.lectureIdx+"/review/view";
      },
      error => {
        console.log(error);
        alert(error.error.message);
        this.pros = [];
        this.cons = [];
      }
    );
    
  }
}
