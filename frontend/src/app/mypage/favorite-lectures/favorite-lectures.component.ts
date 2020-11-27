import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../api.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-favorite-lectures',
  templateUrl: './favorite-lectures.component.html',
  styleUrls: ['./favorite-lectures.component.css']
})
export class FavoriteLecturesComponent implements OnInit {

  constructor(private apiService: ApiService, private route: ActivatedRoute) { }

  lectures = [];
  ngOnInit(): void {
    this.apiService.getFavoriteLectures().subscribe(
      data => {
        this.lectures = data['result'];
        console.log('favorite-lecture');
        console.log(this.lectures);
      },
      error => console.log(error)
    );
  }

}
