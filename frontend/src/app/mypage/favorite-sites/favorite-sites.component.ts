import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../api.service';

@Component({
  selector: 'app-favorite-sites',
  templateUrl: './favorite-sites.component.html',
  styleUrls: ['./favorite-sites.component.css']
})
export class FavoriteSitesComponent implements OnInit {

  constructor(private apiService: ApiService) { }
  sites = [];
  ngOnInit(): void {
    //getFavoriteSites()
    this.apiService.getFavoriteSites().subscribe(
      data => {
        this.sites = data['result'];
        console.log('favorite-sites');
        console.log(this.sites);
      },
      error => console.log(error)
    );
  }

}
