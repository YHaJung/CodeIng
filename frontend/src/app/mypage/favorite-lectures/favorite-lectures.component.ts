import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-favorite-lectures',
  templateUrl: './favorite-lectures.component.html',
  styleUrls: ['./favorite-lectures.component.css']
})
export class FavoriteLecturesComponent implements OnInit {

  constructor(private apiService: ApiService) { }

  lectures = [];
  ngOnInit(): void {
    this.apiService.getFavoriteLectures().subscribe(
      data => {
        this.lectures = data['result'];
        console.log(this.lectures);
      },
      error => console.log(error)
    );
  }

}
