import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-myreviews',
  templateUrl: './myreviews.component.html',
  styleUrls: ['./myreviews.component.css']
})
export class MyreviewsComponent implements OnInit {

  constructor(private apiService: ApiService,) { }
  reviews : [];
  ngOnInit(): void {
    this.apiService.getMyReviews().subscribe(
      data => {
        this.reviews = data['result'];
        console.log(this.reviews);
      },
      error => console.log(error)
    );
  }

}
