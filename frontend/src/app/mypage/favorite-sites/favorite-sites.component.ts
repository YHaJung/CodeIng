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
  /*
  //page
  pages = [1, 2, 3 ,4, 5];
  currentPage = 1;
  maxPage=0;
*/
  ngOnInit(): void {
    this.loadSites();
  }

  loadSites(){
    this.apiService.getFavoriteSites().subscribe(
      data => {
        this.sites = data['result'];
        console.log('favorite-sites');
        console.log(this.sites);
        /*
        //maxpage 불러오기
        this.maxPage = data['maxPage'];
        console.log('maxPage :');
        console.log( this.maxPage );
        */
      },
      error => console.log(error)
    );
  }
/*
  //page 선택
  selectPage(page){
    if(page<=this.maxPage){
      this.currentPage = page;
      this.loadSites();
    }
  }
  pageMinusJump(){
    if(this.pages[0]!=1){
      this.pages[0] -= 5;
      this.pages[1] -= 5;
      this.pages[2] -= 5;
      this.pages[3] -= 5;
      this.pages[4] -= 5;
    }
  }
  pagePlusJump(){
    this.pages[0] += 5;
    this.pages[1] += 5;
    this.pages[2] += 5;
    this.pages[3] += 5;
    this.pages[4] += 5;
  }
  */

}
